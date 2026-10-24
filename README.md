# reify.se

The Reify AB website, built with [Jekyll](https://jekyllrb.com) and published by GitHub Pages from `main`.

## Setup

Uses Ruby 3.3 (see `.ruby-version`), the same version GitHub Pages builds with.

```sh
bundle install
bundle exec rake serve   # http://localhost:4000, with live reload
```

## Adding content

```sh
bundle exec rake page title="Services" nav=3   # new page; nav=N adds it to the header menu
bundle exec rake post title="My Post" tags=talks,programming
```

- **Pages** are Markdown files at the top level (or in a folder as `index.md`). They use the `page` layout by default.
  Set `nav_order` to show a page in the header menu (lower numbers come first), and `sidebar: false` to hide the profile card.
- **Posts** live in `_posts/` as `YYYY-MM-DD-slug.md`, served at `/blog/YYYY-MM-DD-slug`.
  Everything above `<!-- more -->` is the excerpt shown on the blog index.
- Site-wide details (name, links, company info) are in `_config.yml`.

## Layout

- `_layouts/`: `default` (shell), `home`, `page`, `post`
- `_includes/`: header, footer, profile card, post list
- `assets/css/site.css`: all styles, with light and dark themes

## License

[MIT](http://opensource.org/licenses/MIT)
