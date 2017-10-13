import os
import unittest
from base_test import BaseTest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

class ResponsiveTest(BaseTest, unittest.TestCase):

    def job_name(self):
        return 'Responsive test'

    def test_responsive(self):
        # make window the same size as the viewport of iPhone 6/7/8
        self.driver.set_window_size(375, 667)

        active_subsection_id = '1005-3-b'
        self.driver.get(self.test_url + '/1005-3/2012-12121#' + active_subsection_id)
        html = self.driver.find_element_by_tag_name('html')
        WebDriverWait(self.driver, 30).until(
            lambda driver: 'selenium-start' in html.get_attribute('class'))

        # interface is formatted for small screens
        site_title = self.driver.find_element_by_class_name('site-title')
        mobile_nav_trigger = self.driver.find_element_by_class_name('mobile-nav-trigger')
        menu_drawer = self.driver.find_element_by_id('menu')
        wayfinding_header = self.driver.find_element_by_class_name('wayfinding')
        sidebar = self.driver.find_element_by_id('sidebar')
        sample_paragraph = self.driver.find_element_by_xpath('//*[@id="' + active_subsection_id + '"]/p')
        definition_link = self.driver.find_element_by_xpath('//*[@id="1005-3-a"]/p/a[@class="citation definition"]')
        window_y_offset = self.driver.execute_script('return window.pageYOffset;')
        active_subsection_offset = self.driver.execute_script('return document.getElementById("' + active_subsection_id + '").offsetTop;')
        # site title should be hidden on page load
        self.assertFalse(site_title.is_displayed())
        # mobile navigation trigger should be visible on page load
        self.assertTrue(mobile_nav_trigger.is_displayed())
        # menu drawer should be closed on page load
        self.assertIn('close', menu_drawer.get_attribute('class'))
        # wayfinding header should not be floated
        self.assertEqual(wayfinding_header.value_of_css_property('float'), 'none')
        # sidebar shoud not be fixed
        self.assertNotEqual(sidebar.value_of_css_property('position'), 'fixed')
        """ active subsection that the URL points to should be at the top of the
        viewport when the page loads; the window offset minus the subsection
        offset should be zero, but we use "less than 10" to allow for wiggle
        room in how different browsers render the page """
        self.assertTrue(window_y_offset - active_subsection_offset < 10)
        # wayfinding should update on scroll
        self.driver.execute_script('window.scrollTo(0, 0);')
        self.assertEqual(wayfinding_header.text, u'\xa71005.3(a)')
        # definition panel should be fixed
        definition_link.click()
        definition_panel = self.driver.find_element_by_class_name('open-definition')
        self.assertEqual(definition_panel.value_of_css_property('position'), 'fixed')

        # clicking the ">" icon opens the drawer on top of the main content
        drawer_toggle = self.driver.find_element_by_id('panel-link')
        content_body = self.driver.find_element_by_id('content-body')
        drawer_toggle.click()
        # menu drawer should open when the draw toggle is clicked
        self.assertIn('open', menu_drawer.get_attribute('class'))
        # drawer should open on top of the main content
        self.assertEqual(content_body.value_of_css_property('margin-left'), '0px')

        # global navigation works on small screens
        main_navigation = self.driver.find_element_by_class_name('app-nav-list')
        # main navigation should be hidden on page load
        self.assertFalse(main_navigation.is_displayed())
        # main navigation should appear when nav trigger is clicked
        mobile_nav_trigger.click()
        self.assertTrue(main_navigation.is_displayed())
        # landing page should load
        nav_landing_link = self.driver.find_element_by_link_text('Regulations')
        nav_landing_link.click()
        WebDriverWait(self.driver, 30).until(
            lambda driver: driver.find_element_by_class_name('landing-content'))
        landing_page_content = self.driver.find_element_by_class_name('landing-content')
        self.assertTrue(landing_page_content)

if __name__ == '__main__':
    unittest.main()
