---
layout: page
title: Jawaninja
tagline: Puts the Ninja in the Jawa
---
{% include JB/setup %}

<ul class="posts">
  {% for post in site.posts %}
  <li>
    <span>{{ post.date | date_to_string }}</span>&raquo;
    <a href="{{ BASE_PATH }}{{ post.url }}">{{ post.title }}</a>
    <span class="tagline">{{ post.tagline }}</span>
    {{ post.content | split: '<!-- more -->' | first }}
  </li>
  {% endfor %}
</ul>
