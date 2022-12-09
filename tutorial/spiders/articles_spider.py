import scrapy


class ArticleItem(scrapy.Item):
    article_title = scrapy.Field()
    article_content = scrapy.Field()


class ArticleSpider(scrapy.Spider):
    name = "articles"
    start_urls = [
        "https://news.bg/world",
        "https://news.bg/economics"
    ]

    def parse(self, response):
        links = response.css('ul.secondary-articles li div.topic a.title::attr(href)').extract()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_attr)

        next_page = response.css("ul.pagination li:nth-child(3) a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_attr(self, response):
        item = ArticleItem()
        item["article_title"] = "".join(response.xpath("//h1[@itemprop='headline']//text()").extract()).replace(":", " ")
        item["article_content"] = "".join(response.css("div.article-text p ::text").extract()).strip()
        f = open(f"{item['article_title']}.txt", "w")
        f.write(item["article_content"])
        return item