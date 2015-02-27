from django.core.management.base import BaseCommand
from BeautifulSoup import BeautifulSoup
import urllib2
from urlparse import urlparse
from threading import Thread
import sys
import time


class Command(BaseCommand):
    args = "<url where eregulations is located> <optional- comma seperated list of regulation locations to be parsed >  "
    help = 'call every page in eregulations allowing the pages to be cached'

    def access_url(obj,*args):

        try:
            without_anchor = args[0].split("#")[0]
            temp = urllib2.urlopen(without_anchor)
            temp.read()
            temp.close()
            print "Cached: " + without_anchor
        except Exception, errtxt:
            print "    Failed: " + without_anchor
            print "    " + str(errtxt)

        try:
            without_anchor = args[1].split("#")[0]
            temp = urllib2.urlopen(without_anchor)
            temp.read()
            temp.close()
            print "Cached: " + without_anchor
        except Exception, errtxt:
            print "    Failed: " +  without_anchor
            print "    " + str(errtxt)


    def get_main_reg_list(self):
        try:
            regulations_links = []
            html = urllib2.urlopen( self.full_url ).read()
            soup = BeautifulSoup(html)
            reg_list = soup.find( "ul", { "class" : "reg-list" } )

            for link in reg_list.findAll("li"):
                regulations_links.append(link.find("a")["href"])

            print "Got List of Regulations "
            return regulations_links

        except Exception, errtxt:
            print "main page failed to load"
            print "    " + str(errtxt)


    def get_partial_url(self,  href):

        href = href.split("/")

        if self.full_url != self.base_url:
            href[1] = href[1] + "/partial"
        else:
            href[0] = href[0] + "/partial"

        href = '/'.join(href)

        return self.base_url  + href


    def handle(self, *args, **options):

        url = urlparse(sys.argv[2])
        self.base_url = url.scheme + "://" + url.netloc
        self.full_url = sys.argv[2]

        #TODO: make this an argument
        wait_in_seconds = 2

        print self.base_url
        print self.full_url
        self.regulations = None

        if len(sys.argv) > 3:
            self.regulations = sys.argv[3]



        try:
            if not self.regulations:
                regulations_links = self.get_main_reg_list()
            else:
                regulations_links = self.regulations.split(",")

            counter = 0

            for link in regulations_links:
                print "Getting NAV links from " + self.base_url + link

                reg_nav = urllib2.urlopen(self.base_url+link)
                soup = BeautifulSoup(reg_nav)
                reg_soup = soup.findAll("a")



                for a in reg_soup:
                    if a.has_key('data-section-id'):
                        counter = counter + 2
                        partial = self.get_partial_url( a["href"])
                        Thread(target=self.access_url, args=(self.base_url + a["href"],partial ) ).start()

                        if counter >= 10 and ((counter % 10) == 0):

                            print "Total URLs so far: " + str(counter)
                            print "Waiting..."
                            time.sleep(wait_in_seconds)


                print "Waiting..."
                time.sleep(30)

        except Exception, errtxt:
            print "    " + str(errtxt)






