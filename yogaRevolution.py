import re
import os

import scrapy
from scrapy.crawler import CrawlerProcess

import pandas as pd
import matplotlib.pyplot as plt


class YogaSpider(scrapy.Spider):
    name = "yoga"
    start_urls = [ 'https://www.youtube.com/user/yogawithadriene/videos' ]
    scrapes = 0
    videos = []


    def parse(self, response):
        for lockup in response.css('.yt-lockup'):
            title = lockup.css('a.yt-uix-tile-link::text').re(r'^(Revolution - Day)(.)*')
            if len(title) > 0:
                self.scrapes = self.scrapes + 1
                href = lockup.css('a.yt-uix-tile-link::attr(href)').extract_first()
                if href is not None:
                    video_url = response.urljoin(href)
                    yield scrapy.Request(video_url, callback=self.parse_video)


    def parse_video(self, response):
        day = response.css('.watch-title::text').re(r'(Day )(\d+)')[1]
        views = response.css('.watch-view-count::text').extract_first()
        likes = response.css('.like-button-renderer-like-button .yt-uix-button-content::text').extract_first()
        dislikes = response.css('.like-button-renderer-dislike-button .yt-uix-button-content::text').extract_first()

        views = re.sub(r'\D+', '', views)
        likes = re.sub(r'\D+', '', likes)
        dislikes = re.sub(r'\D+', '', dislikes)

        yield {
            'day': day,
            'views': views,
            'likes': likes,
            'dislikes': dislikes,
        }


FILE_NAME = 'yoga_data.json'
process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'FEED_FORMAT': 'json',
    'FEED_URI': FILE_NAME,
})

if os.path.isfile('./' + FILE_NAME):
    os.remove('./' + FILE_NAME)

process.crawl(YogaSpider)
process.start()

data = pd.read_json('./' + FILE_NAME)
data = data.sort_values(by=['day'])
print(data)

plt.plot(data.day, data.dislikes * (data.views.max() / data.dislikes.max()), 'b-', linewidth=2, label='dislikes')
plt.plot(data.day, data.likes * (data.views.max() / data.likes.max()), 'g-', linewidth=2, label='likes')
plt.plot(data.day, data.views, 'r-', linewidth=2, label='views')
plt.legend(loc='upper right')
plt.show()


