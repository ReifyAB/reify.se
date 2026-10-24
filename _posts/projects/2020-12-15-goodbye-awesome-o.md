---
title: "Goodbye, awesome-o"
tagline: "Our Slack bot, 2014–2020"
description: "Our Slack bot at PugglePay, then Zimpler, is offline. A look back at what it did over six years."
tags: [clojure, slack, zimpler]
---

awesome-o, the Slack bot I started at PugglePay in June 2014, is now offline. It was one of our
first Clojure apps in production, and for six years it lived in our Slack, in every channel, answering to
`bot:`.

<!-- more -->

You talked to it in plain English, parsed with an Instaparse grammar, and it kept what it learned in
Redis:

```
bot: Maria is a puggle
bot: Maria is in Göteborg
bot: Maria was born on 1980-01-01
bot: Maria is away from monday to friday
bot: who is Maria?
```

Over the years, with help from a lot of colleagues, it learned to do more:

- every working day, it wished a happy birthday to whoever had one;
- it picked who was "slackmaster" or "meeting master" each week, and passed the role on when someone
  was away;
- it set up random meetings between people in different offices, later in trios, as we grew from
  Göteborg and Stockholm to Berlin;
- it posted announcements to #general for you;
- asked for a movie idea, it would pitch one: Adam Sandler, a cousin, a deserted island, and
  sometimes Rob Schneider.

It started on Heroku, and in 2019 moved to AWS Lambda behind API Gateway, as three functions: one
for mentions, one for announcements and one scheduled ping.

Asked about the meaning of life, it always answered "forty-two".

Source on GitHub: [Zimpler/awesome-o](https://github.com/Zimpler/awesome-o)
