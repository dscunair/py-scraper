import JatimnetScraper

if __name__ == '__main__':

    base_url = 'https://api.jatimnet.com/jinetapi/news'
    scraper = JatimnetScraper.Scraper(base_url)
    scraper.start()    