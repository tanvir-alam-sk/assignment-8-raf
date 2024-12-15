BOT_NAME = "trip_crawler"

SPIDER_MODULES = ["trip_crawler.spiders"]
NEWSPIDER_MODULE = "trip_crawler.spiders"



# PostgreSQL Connection String
SQLALCHEMY_CONNECTION_STRING = 'postgresql+psycopg2://postgres:postgres@localhost:5432/scrapingdb'
# Enable the PostgreSQL Pipeline
ITEM_PIPELINES = {
   'trip_crawler.pipelines.PostgreSQLPipeline': 300,
}


ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 32
DOWNLOAD_DELAY = 3
COOKIES_ENABLED = False


TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"