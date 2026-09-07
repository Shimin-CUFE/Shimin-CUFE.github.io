"""Check generated pages, local links, assets and redirects using only Python's stdlib."""

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.duplicates = []
        self.links = []
        self.canonical = None
        self.redirect = None
        self.main = False
        self.h1_count = 0
        self.feed(text)
        self.close()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        identifier = attrs.get("id")
        if identifier:
            if identifier in self.ids:
                self.duplicates.append(identifier)
            self.ids.add(identifier)
        self.main |= tag == "main"
        self.h1_count += tag == "h1"
        for attribute in ("href", "src", "poster"):
            if attrs.get(attribute):
                self.links.append(attrs[attribute])
        if tag == "link" and "canonical" in attrs.get("rel", "").split():
            self.canonical = attrs.get("href")
        if tag == "meta" and attrs.get("http-equiv", "").lower() == "refresh":
            match = re.search(r"url\s*=\s*(.+)", attrs.get("content", ""), re.I)
            if match:
                self.redirect = match[1].strip(" \"'")
                self.links.append(self.redirect)

    handle_startendtag = handle_starttag


def check_site(site, baseurl):
    site = site.resolve()
    errors = []
    required = ["index.html", "404.html", "sitemap/index.html", "sitemap.xml",
                "about/index.html", "about.html", "assets/css/main.css"]
    for name in required:
        if not (site / name).is_file():
            errors.append(f"Missing required output: {name}")
    if errors:
        return errors, 0, 0

    pages = {p: Page(p.read_text(encoding="utf-8")) for p in site.rglob("*.html")}
    home_url = pages[site / "index.html"].canonical
    if not home_url or urlsplit(home_url).scheme not in {"http", "https"}:
        return ["Home page must have an absolute canonical URL"], 0, 0
    origin_parts = urlsplit(home_url)
    origin = f"{origin_parts.scheme}://{origin_parts.netloc}"
    baseurl = "/" + baseurl.strip("/") if baseurl.strip("/") else ""
    if origin_parts.path != baseurl + "/":
        errors.append(f"Home canonical URL does not match baseurl: {home_url}")

    checked = 0

    def check_link(source, reference):
        nonlocal checked
        source_path = "/" + source.relative_to(site).as_posix()
        absolute = urlsplit(urljoin(origin + baseurl + source_path, reference))
        if absolute.scheme not in {"http", "https"} or absolute.netloc.lower() != origin_parts.netloc.lower():
            return
        checked += 1
        path = unquote(absolute.path)
        if baseurl and not (path == baseurl or path.startswith(baseurl + "/")):
            errors.append(f"{source.relative_to(site)}: link escapes baseurl: {reference}")
            return
        relative = path[len(baseurl):].lstrip("/")
        target = (site / relative).resolve()
        if not target.is_relative_to(site):
            errors.append(f"{source.relative_to(site)}: link escapes site: {reference}")
            return
        if target.is_dir():
            target /= "index.html"
        if not target.is_file():
            errors.append(f"{source.relative_to(site)}: missing target: {reference}")
        elif absolute.fragment and target in pages:
            fragment = unquote(absolute.fragment)
            if not fragment.startswith(":~:text=") and fragment not in pages[target].ids:
                errors.append(f"{source.relative_to(site)}: missing anchor: {reference}")

    for path, page in pages.items():
        if page.duplicates:
            errors.append(f"{path.relative_to(site)}: duplicate IDs: {page.duplicates}")
        if not page.redirect and (not page.main or page.h1_count != 1):
            errors.append(f"{path.relative_to(site)}: expected main and one h1")
        for reference in page.links:
            check_link(path, reference)

    for path in site.rglob("*.css"):
        for match in re.finditer(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)", path.read_text(encoding="utf-8")):
            check_link(path, match[1].strip())

    for name in ("about/index.html", "about.html"):
        if pages[site / name].redirect != home_url:
            errors.append(f"{name}: expected redirect to {home_url}")

    sitemap = site / "sitemap.xml"
    try:
        locations = [node.text for node in ET.parse(sitemap).iter()
                     if node.tag.rsplit("}", 1)[-1] == "loc" and node.text]
        if home_url not in locations:
            errors.append("XML sitemap is missing the home page")
        for location in locations:
            check_link(sitemap, location)
            if urlsplit(location).path in {baseurl + "/404.html", baseurl + "/about/", baseurl + "/about.html"}:
                errors.append(f"XML sitemap contains an excluded page: {location}")
    except ET.ParseError as error:
        errors.append(f"Invalid XML sitemap: {error}")

    for name in ("Gemfile", "Gemfile.lock", "Dockerfile", "CLAUDE.md", "README.md",
                 "scripts", "local", "vendor", ".github", "bash.exe.stackdump"):
        if (site / name).exists():
            errors.append(f"Development file was published: {name}")
    return errors, len(pages), checked


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", type=Path, default=Path("_site"))
    parser.add_argument("--baseurl", default="")
    args = parser.parse_args()
    errors, pages, links = check_site(args.site, args.baseurl)
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1
    print(f"Checked {pages} HTML pages and {links} local references; no errors.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
