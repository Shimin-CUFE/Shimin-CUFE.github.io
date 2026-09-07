# Project guidance

This is the Scripts utility showcase, a small Jekyll site derived from Academic Pages / Minimal Mistakes.

Use README.md for environment setup, commands and the current directory structure.

- Tool content belongs in `_data/tools.yml`; `_pages/index.html` and `_includes/tool.html` render it.
- Keep the home page, 404 page, HTML/XML sitemaps, and the two legacy about redirects working.
- Layouts are `single.html` and `default.html`. There are no blog collections, author sidebar, comments, analytics, content generators or frontend package build.
- Preserve the masthead logo and the navigation configuration.
- Use Jekyll URL filters for internal links and assets so subpath hosting works.
- Keep the five Sass partials independent of third-party grid and icon libraries.
- Do not edit generated `_site/` output. Development tools and caches belong in ignored directories.
- Commit Gemfile.lock when dependencies change. Match the Ruby/Bundler versions documented in README.md.
- After changing templates or assets, run the production build and `python scripts/check_site.py` for both the empty baseurl and `/preview`, as documented in README.md.
- Preserve the original MIT license notice.
