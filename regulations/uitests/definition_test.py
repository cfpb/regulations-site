import os
import unittest
from base_test import BaseTest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

class DefinitionTest(BaseTest, unittest.TestCase):

    def job_name(self):
        return 'Definitions test'


    def test_definition(self):
        self.driver.get('http://localhost:8000/1005-1/2012-12121')
        html = self.driver.find_element_by_tag_name('html')
        WebDriverWait(self.driver, 30).until(
            lambda driver: 'selenium-start' in html.get_attribute('class'))
        definition_link = self.driver.find_element_by_xpath('//*[@id="1005-1-a"]/p/a')
        # term link should have correct data attr
        self.assertTrue('1005-2-a-1' in  definition_link.get_attribute('data-definition'))

        definition_link.click()

        # term link should get active class
        self.assertTrue('active' in definition_link.get_attribute('class'))

        definition = self.driver.find_element_by_xpath('//*[@id="1005-2-a-1"]')
        definition_close_button = self.driver.find_element_by_xpath('//*[@id="1005-2-a-1"]/div[1]/h4/a')

        # definition should appear in sidebar
        self.assertTrue(len(definition.text) > 20)
        definition_term = self.driver.find_element_by_xpath('//*[@id="1005-2-a-1"]/div[2]/p/dfn')
        self.assertEquals(u'\u201cvoided tosser\u201d', 
                          definition_term.text)

        definition_close_button.click()
        # definition should close
        self.assertFalse('active' in definition_link.get_attribute('class'))

        definition_link.click()

        # continue link should load full def
        definition_cont_link = self.driver.find_element_by_xpath('//*[@id="1005-2-a-1"]/div[2]/a[1]')
        definition_cont_link.click()
        WebDriverWait(self.driver, 30).until(
            lambda driver: driver.find_element_by_xpath('//*[@id="1005-2"]'))
        

if __name__ == '__main__':
    unittest.main()
