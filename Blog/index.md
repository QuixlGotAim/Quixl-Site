---
layout: default
title: Home
---

# My Blog Posts

<ul>
  {% for post in site.posts %}
    <li>
      <h2><a href="{{ post.url }}">{{ post.title }}</a></h2>
      <p>{{ post.excerpt }}</p>
      <span>Posted on: {{ post.date | date_to_string }}</span>
    </li>
  {% endfor %}
</ul>
