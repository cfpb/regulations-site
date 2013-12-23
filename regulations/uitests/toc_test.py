import os
import unittest
from base_test import BaseTest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

class TOCTest(BaseTest, unittest.TestCase):

    def job_name(self):
        return 'TOC test'

    def test_toc(self):
        self.driver.get('http://localhost:8000/1005')
        html = self.driver.find_element_by_tag_name('html')
        WebDriverWait(self.driver, 30).until(
            lambda driver: 'selenium-start' in html.get_attribute('class'))

        drawer_toggle = self.driver.find_element_by_id('panel-link')

        # toggle arrow should switch
        self.assertTrue(drawer_toggle.get_attribute('class').find('open'))

        toc_link_1005_1 = self.driver.find_element_by_xpath('//*[@id="toc"]/ol/li[1]/a')
        # toc link should have the proper section id attr
        self.assertEquals(toc_link_1005_1.get_attribute('data-section-id'), '1005-1')
        toc_link_1005_1.click()

        # reg section should load in content area
        self.assertTrue('catharine and myriads' in self.driver.find_element_by_class_name('section-title').text)

        # toc link should be highlighted
        self.assertTrue('current' in toc_link_1005_1.get_attribute('class'))

        # test another section
        toc_link_1005_7 = self.driver.find_element_by_xpath('//*[@id="toc"]/ol/li[7]/a')
        self.assertEquals(toc_link_1005_7.get_attribute('data-section-id'), '1005-7')
        toc_link_1005_7.click()

        self.assertTrue('roentgenologist zest' in self.driver.find_element_by_class_name('section-title').text)
        self.assertTrue('current' in toc_link_1005_7.get_attribute('class'))

        # make sure that the current class has been removed from the prev section
        self.assertFalse('current' in toc_link_1005_1.get_attribute('class'))

if __name__ == '__main__':
    unittest.main()
