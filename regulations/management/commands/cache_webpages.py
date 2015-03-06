from django.core.management.base import BaseCommand
from BeautifulSoup import BeautifulSoup
import requests
from urlparse import urlparse
import threading
import sys
import time


class Command(BaseCommand):
    args = "<url where eregulations is located> <optional- comma seperated list of regulation locations to be parsed >"
    help = 'call every page in eregulations allowing the pages to be cached'

    def access_url(self, *args):

        try:
            req = requests.get(args[0])

            status_txt = "Cached"
            if req.status_code != 200:
                status_txt = "Failed"

            msg = "{0} (status {1}): {2}".format(status_txt, str(req.status_code), req.url)
            self.stdout.write(msg)
        except Exception, errtxt:
            self.stderr.write("    Failed: " + args[0])
            self.stderr.write("    " + str(errtxt))

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
            self.stderr.write("main page failed to load")
            self.stderr.write("    " + str(errtxt))

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

    def handle(self, *args, **options):

        url = urlparse(sys.argv[2])
        self.base_url = url.scheme + "://" + url.netloc
        self.full_url = sys.argv[2]

        self.stdout.write("Base Url:" + self.base_url)
        self.stdout.write("eRegs location:" + self.full_url)

        self.regulations = None

        if len(sys.argv) > 3:
            self.regulations = sys.argv[3]

        try:
            if not self.regulations:
                regulations_links = self.get_main_reg_list()
            else:
                regulations_links = self.regulations.split(",")

            for link in regulations_links:
                self.stdout.write("Getting NAV links from " + self.base_url + link)

                reg_nav = requests.get(self.base_url+link).text
                soup = BeautifulSoup(reg_nav)
                reg_soup = soup.findAll("a")

                for a in reg_soup:
                    if a.has_key('data-section-id'):
                        partial = self.get_partial_url(a["href"])

                        thread_count = len(threading.enumerate())

                        #process 5 web pages at time. Some servers hate a lot of requests at once.
                        #slow it down so the threads can catch up
                        if thread_count <= 5:
                            threading.Thread(target=self.access_url, args=(partial, )).start()
                        else:
                            self.stdout.write("Currently Processing " + str(thread_count) + " Urls")
                            self.stdout.write("Waiting...")
                            time.sleep(thread_count * 2)

                #let the threads catch up before doing the next batch
                if len(threading.enumerate()) > 1:
                    time.sleep(len(threading.enumerate()) * 2)

        except Exception, errtxt:
            self.stderr.write("    " + str(errtxt))






