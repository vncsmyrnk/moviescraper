![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

# Movie Scraper

This is a project based on python and scrapy that scrapes the pages of the [Metacritic](https://www.metacritic.com/) website to colect data about movies and critics.

## Example output

```json
[
  {...},
  {
    "title": "Fanny and Alexander (re-release)",
    "avg_score": "100",
    "year": "2004",
    "description": "Set in Sweden in the early 20th century, this film focuses on the young children of a wealthy, theatrical family.",
    "movie_uri": "/movie/fanny-and-alexander-re-release/",
    "scores": [
      {
        "reviewer_name": "Chicago Tribune",
        "score": "100"
      },
      {
        "reviewer_name": "Chicago Sun-Times",
        "score": "100"
      },
      {
        "reviewer_name": "Boston Globe",
        "score": "100"
      },
      {
        "reviewer_name": "Variety",
        "score": "100"
      },
      {
        "reviewer_name": "Chicago Reader",
        "score": "100"
      },
      {
        "reviewer_name": "Village Voice",
        "score": "90"
      },
      {
        "reviewer_name": "TV Guide Magazine",
        "score": "90"
      }
    ],
    "platform": "metacritic"
  },
  {...},
]
```

The complete scraped data is at [reviews_formatted.json](https://raw.githubusercontent.com/vncsmyrnk/moviescraper/main/reviews_formatted.json).

## Run with docker

```bash
git clone moviescraper && cd moviescraper
docker run -it --rm -v "$(pwd)":/var/app -w /var/app python:3.9 bash
pip install requirements.txt -r # On container
scrapy crawl metacritic -O reviews.json # On container
```
