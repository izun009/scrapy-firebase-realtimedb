import scrapy
import pyrebase
from ..items import ExScrapyToFirebaseItem

class FirebaseQuotesSpider(scrapy.Spider):
    name = 'firebase_quotes'
    #allowed_domains = ['http://quotes.toscrape.com/']
    start_urls = ['http://quotes.toscrape.com/page/1/']

    def __init__(self):
        firebaseConfig = {
            "apiKey": "apikey",
            "authDomain": "your-domain.firebaseapp.com",
            "databaseURL": "https://yourdatabase.firebaseio.com",
            "projectId": "your-project-ID",
            "storageBucket": "your-storagebucket.appspot.com",
            "messagingSenderId": "your-messaging",
            "appId": "your-app-ID"
        }

        firebase = pyrebase.initialize_app(firebaseConfig)
        self.db = firebase.database()

    def parse(self, response):

        quotes = []
        
        for quote in response.css('div.quote'):
            title = quote.css('span.text::text').get()
            author = quote.css('small.author::text').get()
            tags = quote.css('div.tags a.tag::text').getall()

            quotes.append({
                "title": title,
                "author": author,
                "tags": tags,
            })

        for next_page in response.css('li.next a::attr(href)'):
            yield response.follow(next_page, callback=self.parse)

        
        for i in range(0, len(quotes)):
            results = self.db.child("firebase-quotes").child(i).push(quotes[i])
            print(results)

    # def parse(self, response):
    #     quoteItem = ExScrapyToFirebaseItem()
    #     for quote in response.css('div.quote'):
    #         quoteItem['title'] = quote.css('span.text::text').get()
    #         quoteItem['author'] = quote.css('small.author::text').get()
    #         quoteItem['tags'] = quote.css('div.tags a.tag::text').getall()

    #         db.child('quotes').push(quoteItem)

    #         yield quoteItem

    #     for next_page in response.css('li.next a::attr(href)'):
    #         yield response.follow(next_page, callback=self.parse)