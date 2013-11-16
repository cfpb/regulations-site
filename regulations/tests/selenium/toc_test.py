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
        if os.environ.get('TRAVIS') and os.environ.get('TRAVIS_SECURE_ENV_VARS'):
            self.capabilities['tunnel-identifier'] = os.environ['TRAVIS_JOB_NUMBER']
            self.capabilities['build'] = os.environ['TRAVIS_BUILD_NUMBER']
            self.username = os.environ['SAUCE_USERNAME']
            self.key = os.environ['SAUCE_ACCESS_KEY']

        self.capabilities['platform'] = 'LINUX'
        self.capabilities['version'] = ''
        self.capabilities['name'] = 'TOC'
        hub_url = "%s:%s" % (self.username, self.key)
        self.driver = webdriver.Remote(desired_capabilities=self.capabilities,
                                       command_executor = ("http://%s@ondemand.saucelabs.com:80/wd/hub" % hub_url))
        self.jobid = self.driver.session_id
        print("Sauce Labs job: https://saucelabs.com/jobs/%s" % self.jobid)
        self.driver.implicitly_wait(30)

    def test_toc(self):
        self.driver.get('http://localhost:8000/1005')
        drawer_toggle = self.driver.find_element_by_id('panel-link')
        drawer_toggle.click()

        # toggle arrow should switch
        self.assertTrue(drawer_toggle.get_attribute('class').find('open'))

        toc_link_1005_1 = self.driver.find_element_by_xpath('//*[@id="toc"]/ol/li[1]/a')
        # toc link should have the proper section id attr
        self.assertEquals(toc_link_1005_1.get_attribute('data-section-id'), '1005-1')
        toc_link_1005_1.click()

        # reg section should load in content area
        self.assertIn('catharine and myriads', self.driver.find_element_by_class_name('section-title').text)

        # toc link should be highlighted
        self.assertIn('current', toc_link_1005_1.get_attribute('class'))

        # test another section
        toc_link_1005_7 = self.driver.find_element_by_xpath('//*[@id="toc"]/ol/li[7]/a')
        self.assertEquals(toc_link_1005_7.get_attribute('data-section-id'), '1005-7')
        toc_link_1005_7.click()

        self.assertIn('roentgenologist zest', self.driver.find_element_by_class_name('section-title').text)
        self.assertIn('current', toc_link_1005_7.get_attribute('class'))

        # make sure that the current class has been removed from the prev section
        self.assertNotIn('current', toc_link_1005_1.get_attribute('class'))

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
