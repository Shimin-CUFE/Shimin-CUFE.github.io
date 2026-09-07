# Scripts

Personal showcase site for small Python utility tools, built with Jekyll and hosted on GitHub Pages.

Visit [Shimin-CUFE.github.io](https://Shimin-CUFE.github.io).

## Tools

- **ExcelTools** — Batch search and merge for Excel spreadsheets.
- **img2pdf** — Convert and arrange images into an A4 PDF.
- **Blackjack** — A 21-point card game with graphical and console interfaces.

The Python packages listed on the website belong to these tools. They are not dependencies of this website.

## Development

Use Ruby **3.4.10** (also recorded in `.ruby-version`) and Bundler **2.6.9**.
On Windows, RubyInstaller with its MSYS2 Devkit is needed to compile native gem extensions.
Python **3.10+** is only needed for the generated-site checks; no Python packages or Node.js packages are required.

```sh
gem install bundler -v 2.6.9 --no-document
bundle config set --local path vendor/bundle
bundle install
bundle exec jekyll serve --host 127.0.0.1
```

Open [localhost:4000](http://127.0.0.1:4000). Use `bundle exec` so the commands use the committed lockfile.
Restart the server after changing `_config.yml`.

## Structure

```text
_config.yml             Site settings and build exclusions
_data/
  navigation.yml        Optional navigation links
  tools.yml             Tool descriptions, requirements and optional links
_pages/
  index.html            Home page; loops over the tool data
  404.md                Error page
  sitemap.md            Human-readable site map
_layouts/
  default.html          HTML document and masthead
  single.html           Page title and main content
_includes/
  head.html             Stylesheet and favicon references
  seo.html              Title, description, canonical URL and Open Graph tags
  masthead.html         Logo and responsive navigation
  tool.html             Reusable tool entry
_sass/                  Five small style partials; no vendor framework
assets/css/main.scss    Stylesheet entry point compiled by Jekyll
images/                 Logo and fallback favicon
scripts/check_site.py   Generated-page, link, asset and redirect checks
.github/workflows/      Build validation for root and subpath hosting
```

Edit `_data/tools.yml` to add or update a tool. Each entry needs a unique URL-safe `id`, `title`, Markdown `description`, and `requirements`.
Optional `repository_url` and `download_url` fields accept full URLs; leave them empty to hide the buttons.
The listed requirements are display text, not an installation manifest.

Add navigation links in `_data/navigation.yml`. Internal paths start with `/`; templates add the configured `baseurl`.
Use `relative_url` for local links and assets, and `absolute_url` for canonical URLs.
The old `/about/` and `/about.html` addresses redirect to the home page.

The page uses system fonts and CSS navigation. It does not load jQuery, MathJax, analytics or icon fonts.
If a new feature needs a script, keep its source and loading conditions explicit.

## Validation

Run a production build, then inspect its generated output:

```sh
bundle exec jekyll build --strict_front_matter
python scripts/check_site.py
```

Also check a nonempty base path to catch hardcoded root URLs:

```sh
bundle exec jekyll build --strict_front_matter --baseurl /preview
python scripts/check_site.py --baseurl /preview
```

Rebuild without `--baseurl /preview` before serving the root site again.
On PowerShell, set `$env:JEKYLL_ENV = "production"` before these commands;
on Bash, use `export JEKYLL_ENV=production`.

The check script verifies required pages, both legacy redirects, internal links and anchors, CSS asset URLs, XML sitemap entries, and accidental publication of development files.
It does not fetch external websites or replace visual browser checks.
GitHub Actions runs these checks for both base paths on pushes and pull requests.

## Docker

```sh
docker build -t scripts-site .
docker run --rm -p 4000:4000 scripts-site
```

The image includes the site, so the second command works without a volume mount.
For live editing, add a bind mount in PowerShell:

```powershell
docker run --rm -p 4000:4000 --mount "type=bind,source=$($PWD.Path),target=/usr/src/app" scripts-site
```

Or in Bash:

```sh
docker run --rm -p 4000:4000 --mount "type=bind,source=$(pwd),target=/usr/src/app" scripts-site
```

## Dependencies and hosting

`Gemfile` declares Jekyll 3.10, the GFM Markdown parser, sitemap and redirect plugins, and WEBrick.
`Gemfile.lock` records the resolved versions for Windows UCRT and Linux.
Commit dependency changes and the resulting lockfile together. Keep Ruby and Bundler versions in this README, `.ruby-version`, and `Dockerfile` in sync when upgrading.

The project keeps the Jekyll 3.10 series used by the GitHub Pages build service.
The local dependency set omits the `github-pages` umbrella gem and unused themes/plugins.
GitHub's branch-based build service manages its own dependency versions; the lockfile governs local, Docker and the check workflow.
The workflow validates the site; it does not deploy or change the repository's Pages publishing settings.

The site originated from Academic Pages / Minimal Mistakes. The original MIT notice is retained in `LICENSE`.
