# News Agreggator

## Functional requirements:
### news feed
- feed: get latest articles from all sources
- subscription/categories: user should be able to subscribeto sources and categories have a page with articles from subscribed sources and categories

### news crawller:
- parse: system should be able to get title, subtitle, and summary at least from the rss source url
- no-duplicity: system should not create two of the same article from the same source, it has to check if the article exists on database before creating

## entity relationship
users [icon: user, color: blue] {
    id string pk
    username string
    date_created timestamp
}

sources [icon: data, color: yellow] {
  id int pk
  title string
  subtitle
  url string
  language string
}

articles [icon: newspaper, color: purple] {
  id int pk
  source_id int fk
  title string
  publish_date timestamp
  summary string
  image_url string
}

subscriptions [icon: bookmark, color: orange] {
  id int pk
  user_id int fk
  source_id int fk
}

categories [icon: bookmark, color: orange] {
  id int pk
  name
  user_id int fk
  source_id int fk
}

articles.source_id > sources.id

subscriptions.user_id > users.id
subscriptions.article_id > articles.id
