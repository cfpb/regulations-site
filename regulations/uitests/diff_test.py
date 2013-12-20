import os
import unittest
from base_test import BaseTest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select

class DiffTest(BaseTest, unittest.TestCase):

    def job_name(self):
        return 'Diff test'

    def get_drawer_button(self):
        return self.driver.find_element_by_xpath('//*[@id="timeline-link"]')

    def test_diffs(self):
        self.driver.get('http://localhost:8000/1005-2/2011-11111')
        html = self.driver.find_element_by_tag_name('html')
        WebDriverWait(self.driver, 30).until(
            lambda driver: 'selenium-start' in html.get_attribute('class'))

        WebDriverWait(self.driver, 50)
        drawer_button = self.get_drawer_button()
        drawer_button.click()

        WebDriverWait(self.driver, 60).until(
            lambda driver: driver.find_element_by_css_selector('#timeline:not(.hidden)'))

        # drawer button should be active
        self.assertTrue('current' in drawer_button.get_attribute('class'))

        diff_field = Select(self.driver.find_element_by_xpath('//*[@id="timeline"]/div[2]/ul/li[1]/div/div/div/form/select'))
        # select version to compare to
        diff_field.select_by_value('2012-12121')

        # wait until diff view has loaded w/ JS
        WebDriverWait(self.driver, 30).until(
             lambda driver: driver.find_element_by_css_selector('html.js'))

        WebDriverWait(self.driver, 60)
        # make sure the url is right
        self.assertTrue(self.driver.current_url == 'http://localhost:8000/diff/1005-2/2012-12121/2011-11111?from_version=2011-11111')

        # open diff pane in drawer
        active_drawer_button = self.get_drawer_button()
        active_drawer_button.click()
        WebDriverWait(self.driver, 30).until(
            lambda driver: 'current' in active_drawer_button.get_attribute('class'))

        # navigate to 1005.3
        self.driver.find_element_by_id('menu-link').click()
        WebDriverWait(self.driver, 10).until(
            lambda driver: 'current' in driver.find_element_by_id('table-of-contents').get_attribute('class'))
        toc_link_1005_3 = self.driver.find_element_by_xpath('//*[@id="toc"]/ol/li[3]')
        # drawer should have green bar
        self.assertTrue('modified' in toc_link_1005_3.get_attribute('class'))
        toc_link_1005_3.click()

        # wait until 1005.3 diff loads
        WebDriverWait(self.driver, 30).until(
            lambda driver: driver.current_url == 'http://localhost:8000/diff/1005-3/2012-12121/2011-11111?from_version=2011-11111')

        # make sure new section is greened
        new_section = self.driver.find_element_by_xpath('//*[@id="1005-3-b-1-vi"]')
        self.assertTrue(new_section.find_element_by_tag_name('ins'))

        # make sure changed paragraph has insertions and deletions
        changed_section = self.driver.find_element_by_xpath('//*[@id="1005-3-b-2-ii"]')
        self.assertTrue(len(changed_section.find_elements_by_tag_name('ins')) == 2)
        self.assertTrue(len(changed_section.find_elements_by_tag_name('del')))

        # go back into diff pane in drawer, stop comparing
        self.get_drawer_button().click()
        stop_button = self.driver.find_element_by_xpath('//*[@id="timeline"]/div[2]/ul/li[2]/div/a')
        stop_button.click()

        # make sure it goes back to the right place
        WebDriverWait(self.driver, 30).until(
            lambda driver: driver.current_url == 'http://localhost:8000/1005-3/2011-11111')

if __name__ == '__main__':
    unittest.main()
