# Movie Scraper

This is a project of an application that scrapes the pages of the [Metacritic](https://www.metacritic.com/) website to colect data about movies and critics.

## Run with docker

```bash
git clone moviescraper && cd moviescraper
docker run -it --rm -v "$(pwd)":/var/app -w /var/app python:3.9 bash
pip install requirements.txt -r # On container
scrapy crawl metacritic -O reviews.json # On container
```
