import requests as req
from bs4 import BeautifulSoup
import re
from multiprocessing import Pool
import pandas as pd

class Scraper:    

    DEFAULT_POOLSIZE = 50

    def __init__(self, url) -> None:
        self.url = url
        self.poolsize = self.DEFAULT_POOLSIZE
        
        print('Requesting to {}...'.format(url))

    def set_url(self, url):
        self.url = url

        print('Changed url to {}.'.format(url))

    def get_url(self):
        return self.url

    def set_poolsize(self, poolsize):
        self.poolsize = poolsize

    def get_poolsize(self):
        return self.poolsize

    def __get_urls(self):
        
        print('Inspecting available url(s)...')

        # list url
        url_list = [self.url]

        url = self.url

        while True:
            # request API
            res = req.get(url)

            if res.status_code == 200:        
                result = res.json()

                # get next page url
                if result['next'] != None:
                    url = result['next']
                    
                    # append next page url to list
                    url_list.append(url)

                    # debug only
                    # if len(url_list) == 50:
                    #     break
                
                # stop requesting
                else:
                    break
        
        print('Got {} available url(s)'.format(len(url_list)))

        return url_list

    def __generate_pool(self, poolsize):
        return Pool(poolsize)

    def start(self):        

        # check if default poolsize has been changed
        if self.poolsize == self.DEFAULT_POOLSIZE:
            print('Using default poolsize -> {}'.format(self.DEFAULT_POOLSIZE))
        
        # fetch available url(s)
        url_list = self.__get_urls()
        url_list = list(zip(range(0, len(url_list)), url_list))
        
        # create Pooling object(s)    
        pool = self.__generate_pool(self.poolsize)

        # assign function into pool
        df_pool = pool.map(self.scrap, url_list)

        # close pool
        pool.close()

        # collect output
        full_df = pd.concat(df_pool)

        # save DataFrame into csv
        full_df.to_csv('outputs/jatimnet-news.csv', index=False)

    def scrap(self, attr):

        pid = attr[0]
        url = attr[1]
        
        print('PID {} starting...'.format(pid))

        # list of news
        news_list = []        

        # get requests response
        res = req.get(url)

        # if status is OK
        if res.status_code == 200:
            result = res.json()
            
            print('Got {} record(s)'.format(len(result['results'])))
            
            for item in result['results']:
                
                # item news
                news = {}

                # select data from response
                news['id'] = item['id']
                news['url'] = url
                news['slug'] = item['slug']
                news['category'] = item['category']['slug']
                news['published'] = item['published']
                news['keywords'] = item['keyword']
                news['title'] = item['translations']['id']['title']
                news['headline'] = item['translations']['id']['description']
                news['text'] = self.__clean_text(BeautifulSoup(item['translations']['id']['content'], 'html.parser').text)
                try:
                    if item['tags'] != None and len(item['tags']['slug']) > 0:
                        news['tags_slug'] = ','.join(item['tags']['slug'])
                except:
                    item['tags_slug'] = None

                try:
                    if item['tags'] != None and len(item['tags']['name']) > 0:
                        news['tags_name'] = ','.join(item['tags']['name'])                
                except:
                    item['tags_name'] = None

                # append to list of news
                news_list.append(news)                            
        
        return pd.DataFrame(news_list)

    def __clean_text(self, text):
        # remove \n, \xa026, \xa0, etc.
        pattern = r'(\\x[A-z][0-9]*)|(\\n)'
        clean = re.sub(pattern, ' ', text)
        return clean