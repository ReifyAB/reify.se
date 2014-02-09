---
layout: page
title: Jawaninja
tagline: Puts the Ninja in the Jawa
---
{% include JB/setup %}

You have now entered the realm of Jawaninja.

**Do not panic!**

Only friendly geekiness around here. Mostly about Clojure, music and
other interests of mine.

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
