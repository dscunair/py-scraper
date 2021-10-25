# Jatimnet News Scraper
This is a scraper service to request into [https://api.jatimnet.com/jinetapi/news](https://api.jatimnet.com/jinetapi/news). With `multiprocessing` package implementation to enable request parallelly.
<br>

For full documentation regarding the API please visit [https://api.jatimnet.com/jinetapi/](https://api.jatimnet.com/jinetapi/)

## List of Packages
#### Requests
```
pip install requests
```
#### Pandas
```
pip install pandas
```
#### BeautifulSoup
```
pip install beautifulsoup4
```
#### Regex (python standard library, usually no need to install)
```
pip install regex
```
#### Multiprocessing (python standard library, usually no need to install)
```
pip install multiprocessing
```

# How to run
```
git clone https://github.com/affand20/jatimnet-news-scraper.git
cd jatimnet-scraper/scraper
python main.py
```

### Examples
For the full sample code please click [here]('https://github.com/affand20/jatimnet-news-scraper.git/scraper/examples/')

<br>

Configure pool size / batch scraper.
```
import JatimnetScraper

scraper = JatimnetScraper.Scraper('https://api.jatimnet.com/jinetapi/news')
scraper.set_poolsize(100)
scraper.start()    
```