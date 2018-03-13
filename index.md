---
layout: page
title: Jawaninja
tagline: Puts the Ninja in the Jawa
---
{% include JB/setup %}

On a journey to understanding the nature of programming. In love with
Clojure and Idris.

<h3>What's up?</h3>

<ul class="posts">
  {% for post in site.posts %}
  <li>
    {% include post_listing.html %}
    <div class="brief">
      {{ post.content | split: '<!-- more -->' | first }}
    </div>
    <a href="{{ BASE_PATH }}{{ post.url }}" class="read-on">Read on →</a>
  </li>
  {% endfor %}
</ul>
