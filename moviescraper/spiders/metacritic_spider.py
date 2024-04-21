import scrapy
from scrapy.http import Request
import re


# Define o spider que fara a coleta as informacoes no site Meta Critic
class MetacriticSpider(scrapy.Spider):
    name = 'metacritic'
    allowed_domains = ['metacritic.com']
    start_urls = ['https://www.metacritic.com/browse/movie']
    BASE_URL = 'https://www.metacritic.com'  # Non-scrapy
    max_pages = 1  # Non-scrapy; Limite de quantidade de paginas
    download_delay = 2  # Atraso de 2 segundos entre as requisições
    custom_settings = {
        'FEED_FORMAT': 'json',  # Formato do arquivo de saída
        'FEED_URI': 'reviews.json',  # Nome do arquivo de saída
        'USER_AGENT': 'MovieWebCrawler/1.0'  # Indica a plataforma que
                                             # trata-se de um crawler
    }

    def __init__(self, *args, **kwargs):
        super(MetacriticSpider, self).__init__(*args, **kwargs)
        self.page_count = 0

    def parse(self, response):
        """
        Interpreta as requisicoes de cada pagina de listagem de filmes
        """
        # Encontrar os elementos que contêm as avaliações dos filmes
        movies = response.xpath('//div[@class="c-finderProductCard"]')

        # Itera sobre os elementos encontrados e extrair
        # informações relevantes
        for movie in movies:
            # Obtem o título do filme
            title = movie.xpath(
                './/h3[contains(@class, "c-finderProductCard_titleHeading")]'
                '/span[2]/text()').get()

            # Obtem a pontuação do filme
            score = movie.xpath(
                './/div[contains(@class, "c-siteReviewScore")]/span/text()'
            ).get()

            # Obtem o ano de lancamento do filme
            year = ""
            year_matches = re.findall(
                r'\b\d{4}\b', movie.xpath(
                    './/div[contains(@class, "c-finderProductCard_meta")]/span'
                    '/text()').get())

            if year_matches:
                year = year_matches[0]

            # Obtem o descrição do filme
            description = movie.xpath(
                './/div[contains(@class, "c-finderProductCard_description")]/'
                'span/text()').get()

            # Obtem o descrição do filme
            movie_uri = movie.xpath('.//a/@href').get()
            movie_url = self.BASE_URL + movie_uri

            movie_data = {
                'title': title,
                'avg_score': score,
                'year': year,
                'description': description,
                'movie_uri': movie_uri,
                'scores': [],
                'platform': 'metacritic'
            }

            if movie_uri:
                # Se houver a URL de um filme adiciona as avaliacoes
                yield Request(
                        url=movie_url, callback=self.parse_movie_and_scores,
                        errback=self.parse_movie,
                        meta={'movie_data': movie_data})
            else:
                # Caso contrario apenas retorna os dados obtidos
                yield movie_data

        # Incrementar o contador de páginas
        self.page_count += 1

        # Seguir para a próxima página de resultados, se houver
        next_page = 'https://www.metacritic.com/browse/movie/' \
            f'?page={self.page_count+1}'

        if next_page and self.page_count < self.max_pages:
            yield response.follow(next_page, callback=self.parse)
        else:
            return

    def parse_movie_and_scores(self, response):
        """
        Interpreta as avaliacoes da pagina especifica do filme junto
        as informacoes ja coletadas
        """
        movie = response.meta['movie_data']

        # Busca a secao de avaliacoes
        reviews = response.xpath(
                '//div[@data-cy="critic-reviews"]'
                '//div[contains(@class, "c-reviewsSection_carousel_item")]')
        scores = []

        for review in reviews:
            # Obtem o valor da avaliacao
            reviewer_score = review.xpath(
                './/div[contains(@class, "c-siteReviewHeader_reviewScore")]'
                '/a//span/text()').get()

            # Obtem o nome da organizacao avaliadora
            reviewer_name = review.xpath(
                './/div[contains(@class, "c-siteReviewHeader_publisherLogo")]'
                '/a/text()'
            ).get().strip()

            scores.append({
                'reviewer_name': reviewer_name,
                'score': reviewer_score
            })

        movie['scores'] = scores
        yield movie

    def parse_movie(self, response):
        """
        Apenas retorna as informacoes obtidas ate entao
        """
        movie = response.meta['movie_data']
        yield movie
