import os
import unittest
import base64
import json
import httplib
import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

class ExampleTest(unittest.TestCase):

    def setUp(self):
        if (os.environ.get('TRAVIS')):
            self.capabilities['tunnel-identifier'] = os.environ['TRAVIS_JOB_NUMBER']
            self.capabilities['build'] = os.environ['TRAVIS_BUILD_NUMBER']
            self.capabilities['browserName'] = 'chrome'
            self.capabilities['platform'] = 'LINUX'

        self.name = 'Example test'
        self.url = 'http://localhost:8000'
        self.username = os.environ['SAUCE_USERNAME']
        self.key = os.environ['SAUCE_ACCESS_KEY']
        hub_url = "%s:%s" % (self.username, self.key)
        self.driver = webdriver.Remote(desired_capabilities=self.capabilities,
                                       command_executor = "http://%s@ondemand.saucelabs.com:80/wd/hub" % hub_url)
        self.jobid = self.driver.session_id
        print "Sauce Labs job: https://saucelabs.com/jobs/%s" % self.jobid
        self.driver.implicitly_wait(30)

    def report_test_result(self):
        base64string = base64.encodestring('%s:%s'
                                           % (self.username, self.key))[:-1]
        result = json.dumps({'passed': sys.exc_info() == (None, None, None)})
        connection = httplib.HTTPConnection("saucelabs.com")
        connection.request('PUT',
                           '/rest/v1/%s/jobs/%s' % (self.username, self.jobid),
                           result,
                           headers={"Authorization": "Basic %s" % base64string})
        result = connection.getresponse()
        return result.status == 200

    def example_test(self):
        self.driver.get(self.url)
        toc_link_1005_1 = self.driver.find_element_by_xpath('//*[@id="toc"]/ol/li[1]/a')
        self.assertEquals(toc_link_1005_1.get_attribute('data-section-id'), '1005-1')

    def tearDown(self):
        self.driver.quit()
        self.report_test_result()
