---
layout: page
title: Reify
tagline: Value-Oriented Development
---
{% include JB/setup %}

<h3>What's up?</h3>

<ul class="posts">
  {% for post in site.posts %}
  <li>
    {% include post_listing.html %}
    <div class="brief">
      {{ post.content | split: '<!-- more -->' | first }}
    </div>
    <a href="{{ BASE_PATH }}{{ post.url }}" class="read-on pull-right">Read on →</a>
  </li>
  {% endfor %}
</ul>
