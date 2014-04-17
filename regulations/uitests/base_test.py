import os
from selenium import webdriver
from testconfig import config

class BaseTest():

    def config_map(self, browser):
        browser_configs = {
            'chrome': {
                'driver': webdriver.DesiredCapabilities.CHROME,
                'platform': 'LINUX',
                'version': ''
            },
            'ie10': {
                'driver': webdriver.DesiredCapabilities.INTERNETEXPLORER,
                'platform': 'Windows 8',
                'version': '10'
            }
        }
        return browser_configs[browser]

    def setUp(self):
        selenium_config = self.config_map(config['webdriver']['browser'])
        self.test_url = config['testUrl']
        self.capabilities = selenium_config['driver']
        if os.environ.get('TRAVIS') and os.environ.get('TRAVIS_SECURE_ENV_VARS'):
            self.capabilities['tunnel-identifier'] = os.environ['TRAVIS_JOB_NUMBER']
            self.capabilities['build'] = os.environ['TRAVIS_BUILD_NUMBER']

        self.username = os.environ['SAUCE_USERNAME']
        self.key = os.environ['SAUCE_ACCESS_KEY']
        self.capabilities['name'] = self.job_name()
        self.capabilities['platform'] = selenium_config['platform']
        self.capabilities['version'] = selenium_config['version']
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
