Amazing-Python
==============

My Python Programming Goes Here

1)Crawler:A crawler is a program that starts with a url on the web (ex: http://python.org),
fetches the web-page corresponding to that url, and parses all the links on that page into
 a repository of links. Next,it fetches the contents of any of the url from the repository just created,
parses the links from this new content into the repository and continues this process for all links 
in the repository until stopped or after a given number of links are fetched.

	1)  Prerequists:BeautifulSoup4
		link: https://pypi.python.org/pypi/beautifulsoup4

	2)  Usage:Crawler.py -u python.org -r 1 -m 100 -c text/html,application/xhtml+xml

	Status:
	image:https://travis-ci.org/puneethrai/Amazing-Python.png?branch=master["Build Status", link="https://travis-ci.org/puneethrai/Amazing-Python"]