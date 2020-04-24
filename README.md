# Scopus_crawler
> Crawl information of papers (and citing articles) searched byadvancedqueryonScopus (www.scopus.com) via Selenium.

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Introduction](#introduction)
- [Installation](#installation)
- [Usage example](#usage-example)
- [Release History](#release-history)
- [Acknowledgements](#acknowledgements)

## Introduction

Crawl information (citation, bibliography, abstract, fund and other information) of `papers` & `citing articles` searched by advanced query on Scopus (www.scopus.com) via Selenium.

Specially, this program subdivides YEARS into subyear(s), then combines your QUERY and a subyear repeatedly for advanced search, given that we can only manually download at most 2000 results per batch on Scopus.

Workflow of this program:
```python
try: 
    # Main workflow
except: #(i.e. If failed)
    # Try main workflow again
```
![Main_workflow.png](https://i.loli.net/2020/04/24/uhw6rTJCDQ1kNXO.png)

Crawling process shown by the console:
![articles_citingArticles.png](https://i.loli.net/2020/04/24/f3ckbvrABJdF1o6.png)

## Installation

1. Clone via GitHub Desktop or Download .zip
![CloneOrDownload.png](https://i.loli.net/2020/04/24/DbiXzVSs42GZ6Cc.png)

2. Clone from git
```sh
git clone https://github.com/matrixChimera/Scopus_crawler.git
```


## Tutorial
1. Before executing this program, please manually log in Scopus (you have to be able to manually log in, or rather, this program cannnot help you escape the access requirement on Scopus).

2. Before executing this program, please install packages within your python environment:
* prettytable
* selenium
* [webdriver](https://chromedriver.chromium.org/downloads)

3. Before executing this program, please define/modify parameters in settings.py: 

3.1 Define the way you log in:
```python
ACCESS = 'institution'  # or 'cookies'
```

3.2 Define information about logging in:

* If you log in Scopus via your institution (ACCESS = 'institution'), please define your username, password, and institution name:
```python
# ★★★Define your username:
USERNAME = ''
# ★★★Define your password:
PASSWORD = ''
# ★★★Define your institution:
INSTITUTION = ''
```
* If you log in Scopus via cookies (ACCESS = 'cookies'), please define Chrome cookies of the URL with Scopus' access:
```python
chrome_cookies = 'scopusSessionUUID=9461fa86-9c06-4f0c-b;screenInfo="640:1024";SCSessionID=9D8BCB4DD7A64A57C24BFAE9B43FF959.wsnAw8kcdt7IPYLO0V48gA;# ... #;xmlHttpRequest=true'
```
(You can extract cookies via [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg) (an extension of Chrome) after you manually logged in Scopus.)

3.3 Define the permissible query (without PUBYEAR) for advanced search:
```python
QUERY = 'TITLE-ABS-KEY(neurofibroma) AND LANGUAGE(english) AND DOCTYPE(ar)'
```
3.4 Define start_year & end_year for advanced search:
```python
start_year = 2018
end_year = 2019
```
3.5 If necessary (especially when your network is slowed down by the Great Firewall in Mainland China), modify time limits according to your aims and the performance of this program (after you tried this program):
```python
# Define the longest time (second) of implicitly wait of Selenium' execution:
WAIT_TIME = 30
# Define the time limit to downloading:
DOWNLOAD_TIMEOUT = 90
# Define the sleep time for waiting for the rendering (of HTML/JavaScript):
# (If necessary, please prolong the sleep time,
# especially when your network is slowed down by the Great Firewall in Mainland China)
SLEEPTIME_LONG = 10  # Generally for waiting for redirecting/loading of the search page of Scopus
SLEEPTIME_MEDIUM = 5  # Generally for waiting for interacting with elements shown via rendering of JavaScript
SLEEPTIME_SHORT = 2  # Generally for waiting for interacting with elements shown via rendering of HTML
# Times limit to trying (to download) again:
TRY_AGAIN_TIMES = 5
```

4. Run advanced_query_articles.py to crawl information of papers.
Output: one folder, named articles, including .ris files will appear.

5. Run advanced_query_citingArticles.py to crawl information of citing articles.
Output: one folder, named citingArticles, including .ris files will appear.

6. If neccesary (after you crawled .ris files), you can run merge_ris.py to merge all .ris files in the articles/citingArticles folder into one .ris file.


## Release History

* 1.0
    * 2020/04/24
    * Create: settings.py, advanced_query_articles.py, advanced_query_citingArticles.py, and merge_ris.py

## Acknowledgements
Thanks for inspiration from @tomleung1996 (https://github.com/tomleung1996/wos_crawler)

