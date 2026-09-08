source 'https://rubygems.org'

ruby '~> 3.4.0'

# Match the Jekyll series used by GitHub Pages without installing unused themes.
gem 'jekyll', '~> 3.10.0'
gem 'kramdown-parser-gfm', '~> 1.1'

# Ruby 3.4 moved base64 out of the default gems; jekyll 3.10's dependency
# tree requires it at runtime without declaring it (fixed upstream in 4.4.0).
gem 'base64', '~> 0.2'

group :jekyll_plugins do
  gem 'jekyll-redirect-from', '~> 0.16.0'
  gem 'jekyll-sitemap', '~> 1.4.0'
end

# Local preview server; not a Jekyll plugin.
gem 'webrick', '~> 1.9'
