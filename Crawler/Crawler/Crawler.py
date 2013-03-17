"""
Developer : Puneeth Rai
contact   : npuneethrai@yahoo.co.in

Crawler:A crawler is a program that starts with a url on the web (ex: http://python.org),
fetches the web-page corresponding to that url, and parses all the links on that page into
a repository of links. Next,it fetches the contents of any of the url from the repository 
just created,parses the links from this new content into the repository and continues this 
process for all links in the repository until stopped or after a given number of links are fetched.

Usage:Crawler.py -u python.org -r 1 -m 100 -c text/html,application/xhtml+xml
"""
import os
import sys
import urllib
import httplib
import urllib2


from optparse import OptionParser
from bs4 import BeautifulSoup

class Crawler:
    NOTVALID = -1
    INFINITE = -1
    def __init__(self,URL,maxLinks = INFINITE,retries = 1,validContentTypes = ("text/html", "application/xhtml+xml")):
        """
        Objective   :   Constructor
        Takes       :   "URL"- URL to fetch,"maxLinks" - maxLinks to be added to repo,
                        "retries" - No of retries to connect to the server ,"validContentTypes" -Content type filter
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
        if len(self.repo) == self.curIndex:
            self.terminate = True           #We have reached end of POP operation so terminate
            return None
        link = self.repo[self.curIndex]
        self.curIndex +=1
        return link

    def GetRootURL(self, url):
        """
        Objective   :   Gets the root link i.e., https://www.python.org/download to www.python.org 
        Takes       :   None
        Returns     :   URL
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
        links = BeautifulSoup(html) #parses HTML page to tag
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
                #Conects to webServer & retreives the page content
                req = urllib2.Request(URL)
                reqContent = urllib2.urlopen(req)
                contentType = reqContent.headers.get('content-type')
                #Applying Content Type filter
                if self.IsValidContentType(contentType):
                    return reqContent
                else:
                    return None
            except (urllib2.URLError, urllib2.HTTPError, httplib.InvalidURL), e:
                reqCount += 1
                if(reqCount >= self.retries):
                    print "Max retries received for URL:%s closing connection"%(URL)
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

    def __exit__(self):
        """
        Objective   :   Destructor
        Takes       :   None
        Returns     :   length of repo of type int
        """
        this.__del__()
    def __del__(self):
        """
        Objective   :   Destructor
        Takes       :   None
        Returns     :   None
        """
        del self.repo
        del self.URL
        del self.maxLinks
        del self.retries
        self.terminate = True
        del self.curIndex
        del self.validContentTypes
        


def main(args):
    """
    Objective   :   Main execution of program
    Takes       :   None
    Returns     :   None
    """
    CrawlingObj = Crawler(args.url,args.maxCount,args.retries,args.validContentTypes)
    try:
        CrawlingObj.Crawl()
    except (KeyboardInterrupt, SystemExit):
        print "KeyBoard Interupt/System ShutDown recevied"
        CrawlingObj.StopCrawling()
    finally:
        print "Total Repo generated:%d"  %(CrawlingObj.TotalRepo())
        print "Do you want to print the repo?[y/n]"
        choice = raw_input()
        choice.lower()
        if(choice == "y"):
            repo =  CrawlingObj.GetRepo()
            count = 1
            for link in repo:
                print "%d>\t%s"%(count, link)
                count += 1
        del CrawlingObj
        print "Press any key to exit"
        raw_input()


if __name__ == '__main__':
    """
    Objective   :   Program execution starts here ,for command line provide:
                    python Crawler.py -u www.facebook.com -r 1 -m 100 -c text/html,application/xhtml+xml
    Takes       :   sys.args
    Returns     :   None
    """
    parser = OptionParser()
    parser.add_option("-u", "--url",action="store", dest="url",
                  help="URL to crawl")
    parser.add_option("-m", "--max", action="store", dest="maxCount", default=10,
                  help="Max crawl to be erformed",type = 'int')
    parser.add_option("-r", "--retries",
                  action="store", dest="retries", default=1,
                  help="Max retries to be performed before tearing down the connection", type = 'int')
    parser.add_option("-c", "--contenttype",
                  action="store", dest="validContentTypes", default="'text/html,application/xhtml+xml'",
                  help="filter to be applied on ContentType put ',' to append multiple filters")
    options, args = parser.parse_args(sys.argv)
    if not options.url:
        print "Please provide a URL eg:http://www.python.org"
        options.url = raw_input()
        if not options.url:
            print "No URL provided , Crawling using default URL:%s"%("http://www.python.org")
            options.url = "http://www.python.org"
    if not options.url.startswith("http://") :
        if options.url.startswith("https://"):
            pass
        options.url = "http://" + options.url;
    filter = options.validContentTypes 
    filter = filter.split(',')
    options.validContentTypes = filter
    print "Crawling the site:%s with filter:%s"%(options.url,options.validContentTypes)
    main(options)
