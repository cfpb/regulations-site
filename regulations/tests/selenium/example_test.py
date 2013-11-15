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
        self.capabilities = webdriver.DesiredCapabilities.CHROME
        self.capabilities['tunnel-identifier'] = os.environ['TRAVIS_JOB_NUMBER']
        self.capabilities['build'] = os.environ['TRAVIS_BUILD_NUMBER']
        self.capabilities['platform'] = 'LINUX'
        self.capabilities['version'] = ''
        self.capabilities.name = 'Example test'
        self.username = os.environ['SAUCE_USERNAME']
        self.key = os.environ['SAUCE_ACCESS_KEY']
        hub_url = "%s:%s" % (self.username, self.key)
        self.driver = webdriver.Remote(desired_capabilities=self.capabilities,
                                       command_executor = ("http://%s@ondemand.saucelabs.com:80/wd/hub" % hub_url))
        self.jobid = self.driver.session_id
        print("Sauce Labs job: https://saucelabs.com/jobs/%s" % self.jobid)
        self.driver.implicitly_wait(30)

    def test_sauce(self):
        self.driver.get('http://localhost:8000')
        toc_link_1005_1 = self.driver.find_element_by_xpath('//*[@id="toc"]/ol/li[1]/a')
        self.assertEquals(toc_link_1005_1.get_attribute('data-section-id'), '1005-1')

    def tearDown(self):
        print("https://saucelabs.com/jobs/%s" % self.driver.session_id)
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
