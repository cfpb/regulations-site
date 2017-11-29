import os
import unittest
from base_test import BaseTest
from selenium import webdriver
from selenium.webdriver.support.color import Color
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

class DiffTest(BaseTest, unittest.TestCase):

    def job_name(self):
        return 'Diff test'

    def get_drawer_button(self):
        return self.driver.find_element_by_xpath('//*[@id="timeline-link"]')

    def test_diffs(self):
        self.driver.get(self.test_url + '/1005-2/2011-11111')
        html = self.driver.find_element_by_tag_name('html')
        WebDriverWait(self.driver, 60).until(
            lambda driver: 'selenium-start' in html.get_attribute('class'))

        WebDriverWait(self.driver, 60)
        drawer_button = self.get_drawer_button()
        drawer_button.click()

        WebDriverWait(self.driver, 60).until(
            lambda driver: driver.find_element_by_css_selector('#timeline:not(.hidden)'))

        # drawer button should be active
        self.assertTrue('current' in drawer_button.get_attribute('class'))

        # drawer should display regulation history
        timeline_list_items = self.driver.find_elements_by_css_selector('#history-toc-list .status-list')
        expected_timeline_versions = [
            '2011-11111',
            '2012-12121'
        ]
        for index, expected_version in enumerate(expected_timeline_versions):
            self.assertEqual(timeline_list_items[index].get_attribute('data-base-version'), expected_version)

        # each timeline entry is a link to the rule effective on that date
        timeline_links = self.driver.find_elements_by_class_name('version-link')
        expected_timeline_urls = [
            self.test_url + '/1005-2/2011-11111',
            self.test_url + '/1005-2/2012-12121'
        ]
        for index, expected_url in enumerate(expected_timeline_urls):
            self.assertEqual(timeline_links[index].get_attribute('href'), expected_url)

        diff_field = Select(self.driver.find_element_by_xpath('//*[@id="timeline"]/div[2]/ul/li[1]/div/div/div/form/select'))
        # select version to compare to
        diff_field.select_by_value('2012-12121')

        # wait until diff view has loaded
        html = self.driver.find_element_by_tag_name('html')
        WebDriverWait(self.driver, 90).until(
             lambda driver: 'selenium-start' in html.get_attribute('class'))

        WebDriverWait(self.driver, 60)
        # make sure the url is right
        self.assertTrue(self.driver.current_url == self.test_url + '/diff/1005-2/2012-12121/2011-11111?from_version=2011-11111')

        WebDriverWait(self.driver, 60)

        # open diff pane in drawer
        active_drawer_button = self.get_drawer_button()
        active_drawer_button.click()
        WebDriverWait(self.driver, 60).until(
            lambda driver: 'current' in active_drawer_button.get_attribute('class'))

        # diff pane drawer button should be red
        diff_button_hex_color = Color.from_string(active_drawer_button.value_of_css_property('color')).hex
        self.assertEqual(diff_button_hex_color, '#d14124')

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
            lambda driver: driver.current_url == self.test_url + '/diff/1005-3/2012-12121/2011-11111?from_version=2011-11111')

        # added text should be italicized and highlighted in green
        new_section = self.driver.find_element_by_xpath('//*[@id="1005-3-b-1-vi"]')
        new_section_insertion = new_section.find_element_by_tag_name('ins')
        insertion_hex_color = Color.from_string(new_section_insertion.value_of_css_property('background-color')).hex
        self.assertEqual(new_section_insertion.value_of_css_property('font-style'), 'italic')
        self.assertEqual(insertion_hex_color, '#e2efd8')

        # make sure changed paragraph has insertions and deletions
        changed_section = self.driver.find_element_by_xpath('//*[@id="1005-3-b-2-ii"]')
        changed_section_insertions = changed_section.find_elements_by_tag_name('ins')
        changed_section_deletion = changed_section.find_elements_by_tag_name('del')
        self.assertTrue(len(changed_section_insertions) == 2)
        self.assertTrue(len(changed_section_deletion))

        # deleted text should be struck through and gray
        deletion_hex_color = Color.from_string(changed_section_deletion[0].value_of_css_property('color')).hex
        self.assertEqual(deletion_hex_color, '#b4b5b6')
        self.assertEqual(changed_section_deletion[0].value_of_css_property('text-decoration'), 'line-through')

        # go back into diff pane in drawer, stop comparing
        self.get_drawer_button().click()
        stop_button = self.driver.find_element_by_xpath('//*[@id="timeline"]/div[2]/ul/li[2]/div/a')
        stop_button.click()

        # make sure it goes back to the right place
        WebDriverWait(self.driver, 30).until(
            lambda driver: driver.current_url == self.test_url + '/1005-3/2011-11111')

        # "find the regulation effective on this date" takes you to the proper version
        self.get_drawer_button().click()
        month_input = self.driver.find_element_by_class_name('month-input')
        day_input = self.driver.find_element_by_class_name('day-input')
        year_input = self.driver.find_element_by_class_name('year-input')
        find_button = self.driver.find_element_by_class_name('find-button')
        month_input.clear()
        day_input.clear()
        year_input.clear()
        month_input.send_keys('3')
        day_input.send_keys('10')
        year_input.send_keys('2012')
        find_button.click()
        WebDriverWait(self.driver, 30).until(
            lambda driver: driver.current_url == self.test_url + '/1005-3/2012-12121')

if __name__ == '__main__':
    unittest.main()
