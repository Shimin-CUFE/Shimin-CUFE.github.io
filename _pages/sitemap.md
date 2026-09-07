---
title: Sitemap
lang: en
permalink: /sitemap/
---

All pages on this site. An [XML sitemap]({{ '/sitemap.xml' | relative_url }}) is also available.

<ul class="sitemap-list">
{% assign pages = site.pages | sort: 'url' %}
{% for item in pages %}
  {% if item.title and item.sitemap != false and item.layout != 'redirect' %}
  <li><a href="{{ item.url | relative_url }}">{{ item.title | escape }}</a></li>
  {% endif %}
{% endfor %}
</ul>
