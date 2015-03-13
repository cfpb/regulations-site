from BeautifulSoup import BeautifulSoup
import requests
from urlparse import urlparse
import threading
import sys
import time


class EregsCache():

    @staticmethod
    def write(msg):
        sys.stdout.write(msg + "\n")

    @staticmethod
    def write_error(msg):
        sys.stderr.write(msg + "\n")

    def access_url(self, *args):

        try:
            req = requests.get(args[0])

            status_txt = "Cached"
            if req.status_code != 200:
                status_txt = "Failed"

            msg = "{0} (status {1}): {2}".format(status_txt, str(req.status_code), req.url)
            self.write(msg)
        except Exception, errtxt:
            self.write_error("Failed: " + args[0])
            self.write_error(str(errtxt))

    def get_main_reg_list(self):
        try:
            regulations_links = []
            html = requests.get(self.full_url).text
            soup = BeautifulSoup(html)
            reg_list = soup.find("ul", {"class": "reg-list"})

            for link in reg_list.findAll("li"):
                regulations_links.append(link.find("a")["href"])

            return regulations_links

        except Exception, errtxt:
            self.write_error("Main Page Failed To Load")
            self.write_error(str(errtxt))

    #figure out the partial path depending on root location of eregs
    def get_partial_url(self,  href):

        href = href.split("/")

        if self.full_url != self.base_url:
            href[1] += "/partial"
        else:
            href[0] += "/partial"

        href = '/'.join(href)

        href = href.split("#")[0]

        return self.base_url + href

    def __init__(self, eregs_url, regulations=None):
        """ kick off calling regulations website for caching purposes

            Keyword arguments:
            eregs_url -- full web url to main regulations page
            regulations -- (optional) list of regulation paths to be processed
        """

        url = urlparse(eregs_url)
        self.base_url = url.scheme + "://" + url.netloc
        self.full_url = eregs_url

        self.write("Base Url:" + self.base_url)
        self.write("eRegs location:" + self.full_url)

        try:
            if not regulations:
                regulations_links = self.get_main_reg_list()
            else:
                regulations_links = regulations.split(",")

            for link in regulations_links:
                self.write("Getting NAV links from " + self.base_url + link)

                reg_nav = requests.get(self.base_url+link).text
                soup = BeautifulSoup(reg_nav)
                reg_soup = soup.findAll("a")

                for a in reg_soup:
                    if a.has_key('data-section-id'):
                        partial = self.get_partial_url(a["href"])

                        thread_count = len(threading.enumerate())

                        #process 5 web pages at time. Some servers hate a lot of requests at once.
                        #slow it down so the threads can catch up
                        #if there are too many threads being processed, end process and exit out
                        if thread_count <= 5:
                            threading.Thread(target=self.access_url, args=(partial, )).start()
                        elif thread_count >= 12:
                            self.write("URLs currently at " + str(thread_count) + ". Server too slow")
                            self.write("Shutting down")
                            raise Exception("Thread Count Too High")
                        else:
                            self.write("Currently Processing " + str(thread_count) + " Urls")
                            self.write("Waiting...")
                            time.sleep(thread_count * 2)

                #let the threads catch up before doing the next batch
                if len(threading.enumerate()) > 1:
                    time.sleep(len(threading.enumerate()) * 2)

        except Exception, errtxt:
            self.write_error(str(errtxt))


if __name__ == "__main__":
    regulations_arg = None
    if len(sys.argv) > 3:
        regulations_arg = sys.argv[3]

    EregsCache(sys.argv[1],regulations_arg)