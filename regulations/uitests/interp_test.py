import os
import unittest
from base_test import BaseTest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

class InterpTest(BaseTest, unittest.TestCase):

    def job_name(self):
        return 'Interp test'

    def test_interps(self):
        self.driver.get(self.test_url + '/1005-2/2012-12121')
        html = self.driver.find_element_by_tag_name('html')
        WebDriverWait(self.driver, 30).until(
            lambda driver: 'selenium-start' in html.get_attribute('class'))

        interp_dropdown = self.driver.find_element_by_xpath('//*[@id="1005-2-h"]/section')

        # interp should know who it belongs to
        self.assertEquals(interp_dropdown.get_attribute('data-interp-for'), '1005-2-h')

        # interp section should know what is in it
        self.assertEquals(interp_dropdown.get_attribute('data-interp-id'), '1005-18-a')

        # should have the appropriate header
        self.assertTrue('OFFICIAL INTERPRETATION TO 2(h)' in interp_dropdown.text)

        # should have the "SHOW" link
        self.assertIn('SHOW', interp_dropdown.text)

        self.driver.execute_script('p10052h = document.getElementById("1005-2-h").offsetTop')
        self.driver.execute_script('window.scrollTo(0, p10052h)')

        # body should be hidden
        interp_text = self.driver.find_element_by_xpath('//*[@id="1005-2-h"]/section/section')
        interp_dropdown.click()

        WebDriverWait(self.driver, 120).until(
            lambda driver: driver.find_element_by_css_selector('.inline-interpretation.open'))

        # header should update
        self.assertTrue('HIDE' in interp_dropdown.text)

        # should contain the appropriate reg section
        self.assertTrue('clicked. A finances centripetally curiousest stronghold cemeteries' in interp_text.text)

        # should contain a link to the appropriate reg section
        interp_link = self.driver.find_element_by_xpath('//*[@id="1005-2-h"]/section/section/p/a[@class="internal section-link"]')
        self.assertEqual(self.test_url + '/1005-Subpart-Interp/2012-12121#1005-18-a', interp_link.get_attribute('href'))
        self.assertEqual(u'See this interpretation in Supplement I', interp_link.text)

        self.driver.find_element_by_xpath('//*[@id="1005-2-h"]/section/header/a').click()

        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_element_by_css_selector('.inline-interpretation:not(.open)'))

        # header should reflect close
        self.assertTrue('SHOW' in interp_dropdown.text)

if __name__ == '__main__':
    unittest.main()
