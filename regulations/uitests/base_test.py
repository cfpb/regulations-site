import os
from selenium import webdriver

class BaseTest():

    def setUp(self):
        self.capabilities = webdriver.DesiredCapabilities.CHROME
        if os.environ.get('TRAVIS') and os.environ.get('TRAVIS_SECURE_ENV_VARS'):
            self.capabilities['tunnel-identifier'] = os.environ['TRAVIS_JOB_NUMBER']
            self.capabilities['build'] = os.environ['TRAVIS_BUILD_NUMBER']

        self.username = os.environ['SAUCE_USERNAME']
        self.key = os.environ['SAUCE_ACCESS_KEY']
        self.capabilities['name'] = self.job_name()
        self.capabilities['platform'] = 'LINUX'
        self.capabilities['version'] = ''
        hub_url = "%s:%s" % (self.username, self.key)
        self.driver = webdriver.Remote(desired_capabilities=self.capabilities,
                                       command_executor = ("http://%s@ondemand.saucelabs.com:80/wd/hub" % hub_url))
        self.jobid = self.driver.session_id
        print("Sauce Labs job: https://saucelabs.com/jobs/%s" % self.jobid)
        self.driver.implicitly_wait(30)

    def job_name(self):
        return 'eRegs UI Test'

    def tearDown(self):
        self.driver.quit()
