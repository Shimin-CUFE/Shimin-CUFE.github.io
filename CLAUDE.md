# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Jekyll-based GitHub Pages personal academic website, built on the [Academic Pages](https://academicpages.github.io/) template (a fork of Minimal Mistakes). It is served automatically by GitHub Pages when pushed to the `master` branch.

## Commands

### Local Development

```bash
# Install Ruby dependencies
bundle install

# Start local dev server with live reload
jekyll serve -l -H localhost
# Site available at http://localhost:4000
```

### Docker

```bash
docker build -t jekyll-site .
docker run -p 4000:4000 --rm -v $(pwd):/usr/src/app jekyll-site
```

## Architecture

### Central Configuration

`_config.yml` controls everything: site title/URL/description, author profile (avatar, social links, bio), collections, defaults for each page type, Markdown processing (kramdown + rouge), plugins, and archive settings. Most customizations start here.

### Content Organization

| Directory | Purpose |
|-----------|---------|
| `_pages/` | Standalone pages (about, cv, markdown guide, 404, archives) |
| `_posts/` | Blog posts — filename format `YYYY-MM-DD-title.md` |
| `_teaching/` | Teaching portfolio entries (collection) |
| `_publications/` | Publications list (collection) |
| `_talks/` | Conference talks and presentations (collection) |
| `_portfolio/` | Portfolio items (collection) |
| `_drafts/` | Unpublished draft posts |

### Data Files (`_data/`)

- `navigation.yml` — Site navigation menu structure
- `ui-text.yml` — Localized UI strings (English)
- `authors.yml` — Author profile data
- `comments/` — Staticman-powered comment data (YAML files keyed by post slug)

### Theme & Layout (`_layouts/`, `_includes/`, `_sass/`)

- `_layouts/` — Page layouts: `default.html`, `single.html`, `archive.html`, `splash.html`, `talk.html`, `compress.html`
- `_includes/` — Reusable partials: masthead, footer, sidebar, author profile, analytics, comments, SEO meta tags, social sharing, pagination, breadcrumbs
- `_sass/` — SCSS stylesheets (compiled to `assets/css/main.scss`)
- `assets/` — Static assets (CSS, JS, images)

### Content Generators (`markdown_generator/`)

Python scripts and Jupyter notebooks to generate markdown files for publications and talks from TSV data:

- `publications.py` / `.ipynb` — Generate `_publications/` entries from `publications.tsv`
- `talks.py` / `.ipynb` — Generate `_talks/` entries from `talks.tsv`
- `PubsFromBib.ipynb` / `pubsFromBib.py` — Generate publications from BibTeX files
- `OrcidToBib.ipynb` — Fetch ORCID publications and convert to BibTeX

### Plugins

jekyll-feed, jekyll-gist, jekyll-paginate, jekyll-sitemap, jemoji — all whitelisted for GitHub Pages compatibility.

## Customizing the Site

1. Edit `_config.yml` — update `title`, `name`, `description`, `url`, `repository`, and `author` fields with real information
2. Replace `images/profile.png` with an actual avatar
3. Edit `_data/navigation.yml` to update the site menu
4. Add/modify content files in `_pages/`, `_posts/`, and collection directories
5. Upload downloadable files (PDFs, etc.) to the `files/` directory
