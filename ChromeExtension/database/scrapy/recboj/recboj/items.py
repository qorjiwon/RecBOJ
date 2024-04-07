# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy

class User(scrapy.Item):
    user_id = scrapy.Field()
    level = scrapy.Field()
    pass

class Problem(scrapy.Item):
    user_id = scrapy.Field()
    problem_id = scrapy.Field()
    total_count = scrapy.Field()
    wrong_count = scrapy.Field()
    last_time = scrapy.Field()
    pass
