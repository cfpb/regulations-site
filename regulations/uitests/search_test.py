import os
import unittest
from base_test import BaseTest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

class SearchTest(BaseTest, unittest.TestCase):

    def job_name(self):
        return 'Search test'

    def test_search(self):
        # make window wide enough so that the left panel defaults to open
        self.driver.set_window_size(1366, 768)

        self.driver.get(self.test_url + '/1005')
        html = self.driver.find_element_by_tag_name('html')
        WebDriverWait(self.driver, 30).until(
            lambda driver: 'selenium-start' in html.get_attribute('class'))

        # clicking on the search icon shows the initially hidden search drawer
        search_icon = self.driver.find_element_by_id('search-link')
        search_drawer = self.driver.find_element_by_class_name('search-drawer')
        self.assertIn('hidden', search_drawer.get_attribute('class'))
        search_icon.click()
        self.assertNotIn('hidden', search_drawer.get_attribute('class'))

        # searching for a term displays the correct results
        search_input = self.driver.find_element_by_id('search-input')
        search_submit = self.driver.find_element_by_xpath('//*[@id="search"]//button[@type="submit"]')
        search_term = 'lorem ipsum'
        search_input.send_keys(search_term)
        search_submit.click()
        WebDriverWait(self.driver, 30).until(
            lambda driver: driver.find_element_by_class_name('result-list'))
        search_header = self.driver.find_element_by_xpath('//h2[@class="search-term"]')
        search_pager = self.driver.find_element_by_class_name('pager')
        search_results = self.driver.find_elements_by_xpath('//ul[@class="result-list"]/li/h3/a')
        expected_results = [
            u'1005.Subpart',
            u'1005.1 \xa7',
            u'1005.1(a)',
            u'1005.1(b)',
            u'1005.2 \xa7',
            u'1005.2(a)',
            u'1005.2(a)(1)',
            u'1005.2(a)(2)',
            u'1005.2(a)(2)(i)',
            u'1005.2(a)(2)(ii)'
        ]
        self.assertEqual(search_header.text, u'Searching for \u201c' + search_term + u'\u201d')
        self.assertEqual(search_pager.text, u'Page 1 of 124')
        for index, result in enumerate(search_results):
            self.assertEqual(result.text, expected_results[index])

        # clicking a serrch result loads the appropriate subsection
        search_result_link = search_results[7]
        search_result_link.click()
        WebDriverWait(self.driver, 30).until(
            lambda driver: driver.find_element_by_id('1005-2'))
        wayfinding_header = self.driver.find_element_by_xpath('//*[@id="active-title"]/*[@class="header-label"]')
        self.assertEqual(wayfinding_header.text, u'\xa71005.2(a)(2)')

if __name__ == '__main__':
    unittest.main()
