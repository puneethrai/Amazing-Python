import os
import sys
import Queue
import urllib
import httplib
import urllib2


from optparse import OptionParser, SUPPRESS_HELP
from bs4 import BeautifulSoup, SoupStrainer

class Crawler:
    NOTVALID = -1
    INFINITE = -1
    def __init__(self,URL,maxLinks = INFINITE,retries = 1,validContentTypes = ("text/html", "application/xhtml+xml")):
        """
        Objective   :   Constructor
        Takes       :   "URL"- URL to fetch,"maxLinks" - maxLinks to be added to repo,"retries" - No of retries to connect to the server
        Returns     :   None
        """
        self.URL = URL
        self.maxLinks = maxLinks
        self.retries = retries
        self.repo = []
        self.terminate = False
        self.curIndex = 0
        self.validContentTypes = validContentTypes
        self.__push__(URL)
    
    def __push__(self,link):
        """
        Objective   :   Adds links to repo & increments current index
        Takes       :   "link" - link to be added to repo
        Returns     :   None
        """
        if(self.terminate):
            pass
        else:
            if link not in self.repo:
                self.repo.append(link)
            
            if(len(self.repo) >= self.maxLinks and not(self.maxLinks == Crawler.INFINITE) ):
                self.terminate = True

    def __pop__(self):
        """
        Objective   :   Returns links from repo & decrements current index
        Takes       :   None
        Returns     :   link
        """
        if len(self.repo) == 0:
            return None
        link = self.repo[self.curIndex]
        self.curIndex +=1
        return link

    def GetRootURL(self, url):
        """
        Objective   :   Gets the root link i.e., https://www.python.org/download to www.python.org 
        Takes       :   None
        Returns     :   link
        """
        if url.startswith("http://"):
            return "http://" + url[7:].split("/")[0]
        elif url.startswith("https://"):
            return "https://" + url[8:].split("/")[0]
            
        return url

    def GetCompleteURL(self,baseURL,curURL):
        """
        Objective   :   Returns Complete URL address
        Takes       :   "baseURL" - base URL ,"curURL" - current URL to append to base URL 
        Returns     :   string with Entire URL 
        """
        completeURL = curURL
        
        if curURL.startswith("http://") or curURL.startswith("https://"):
            pass
        elif curURL.startswith("/"):
            completeURL =  self.GetRootURL(baseURL) + curURL
        elif curURL.startswith("#"):
            completeURL =  self.GetRootURL(baseURL) + '/' + curURL
        else:
            completeURL = baseURL + curURL

        return completeURL

    def DeriveSaveLinks(self,baseURL,html):
        """
        Objective   :   Decodes the HTML page , parses all link present in it & stores it in repo
        Takes       :   "baseURL" - base URL ,"html" - HTML pages
        Returns     :   None
        """
        if self.terminate:
            return
        links = BeautifulSoup(html) 
        for link in links.findAll("a"):
            if link.get("href"):
                self.__push__(self.GetCompleteURL(baseURL,link["href"]))

    def IsValidContentType(self,contentType):
        """
        Objective   :   Determines weather content type is valid or not 
        Takes       :   "contentType" - content type to checked
        Returns     :   Boolean
        """
        for contentTypes in self.validContentTypes:
            if contentType.find(contentTypes) > Crawler.NOTVALID:
                return True
        return False

    def GetHTMLPages(self,URL):
        """
        Objective   :   Returns HTML Page for the given URL
        Takes       :   "URL" - URL to fetch
        Returns     :   HTML Page 
        """
        reqCount = 0
        while True:
            try:
                req = urllib2.Request(URL)
                reqContent = urllib2.urlopen(req)
                contentType = reqContent.headers.get('content-type')
                if self.IsValidContentType(contentType):
                    return reqContent
                else:
                    return None
            except (urllib2.URLError, urllib2.HTTPError, httplib.InvalidURL), e:
                reqCount += 1
                if(reqCount >= self.retries):
                    return None
        

    def Crawl(self):
        """
        Objective   :   Starts crawling execution 
        Takes       :   None
        Returns     :   None
        """
        while not self.terminate:
            link = self.__pop__()
            if link == None:
                continue
            htmlPage = self.GetHTMLPages(link)
            
            if htmlPage:
                self.DeriveSaveLinks(link,htmlPage)
    def StopCrawling(self):
        """
        Objective   :   Stops execution 
        Takes       :   None
        Returns     :   None
        """
        self.terminate = True

    def GetRepo(self):
        """
        Objective   :   Returns Copy of repository
        Takes       :   None
        Returns     :   Repository of type List
        """

        return self.repo[:]
    def TotalRepo(self):
        """
        Objective   :   Returns length of repository
        Takes       :   None
        Returns     :   length of repo of type int
        """
        return len(self.repo)
            

def main():
    """
    Objective   :   Main execution of program
    Takes       :   None
    Returns     :   None
    """
    CrawlingObj = Crawler("http://blah")
    try:
        CrawlingObj.Crawl()
    except (KeyboardInterrupt, SystemExit):
        CrawlingObj.StopCrawling()
    finally:
        repo =  CrawlingObj.GetRepo()
        count = 1
        for link in repo:
            print "%d.\t%s"%(count, link)
            count += 1
        raw_input()


if __name__ == '__main__':
    main()
