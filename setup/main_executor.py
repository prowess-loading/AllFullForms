import sys
from setup.browser_setup import BrowserSetup
from pages.homePage import Page
import random
from setup import utils
from setup.ad_clicker import AdClicker
import time


class MainExecutor:
    def __init__(
            self, device_type="both",
            proxy_active=True,
            device_name="random",
            browser_name="random",
            region="na",                    # rd, us, na, au, as, eu
            add_utm=True,
            enable_ad_click=False,
            ad_click_frequency=1
    ):
        self.device_type = device_type
        self.proxy_active = proxy_active
        self.device_name = device_name
        self.browser_name = browser_name
        self.region = region
        self.add_utm = add_utm
        self.enable_ad_click = enable_ad_click
        self.ad_click_frequency = ad_click_frequency

    def setup_driver(self):
        browser_setup = BrowserSetup()
        return browser_setup.setup_browser(
            self.device_type,
            self.proxy_active,
            device_name=self.device_name,
            browser_name=self.browser_name,
            region=self.region,
        )

    def process_run(self, driver, click_ad, ad_log_file):
        target_url = utils.target_url(self.add_utm)
        utils.open_url_with_retry(driver, target_url)

        page = Page(driver)
        ad_clicker = AdClicker(driver)

        page_actions = {
            "genderPage": ["genderPage"],
            "agePage": ["genderPage", "agePage"],
            "loanAmountPage": ["genderPage", "agePage", "loanAmountPage"]
        }
        weights = {
            "loanAmountPage": 0.5,
            "agePage": 0.3,
            "genderPage": 0.2
        }
        target_page = random.choices(
            list(weights.keys()), weights=list(weights.values()), k=1)[0]

        # target_page = "agePage"

        print(f"Final page - {target_page} - Ad Click - {click_ad}")

        if click_ad:
            if target_page == "genderPage":
                print("Visiting genderPage")
                ad_clicker.select_random_ad(ad_log_file)

            elif target_page == "agePage":
                print("Visiting agePage")
                page.click_random_element("genderPage")
                ad_clicker.select_random_ad(ad_log_file)

            elif target_page == "loanAmountPage":
                print("Visiting loanAmountPage")
                page.click_random_element("genderPage")
                page.click_random_element("agePage")
                ad_clicker.select_random_ad(ad_log_file)

            else:
                print("Visiting loanTypePage")
                page.click_random_element("genderPage")
                page.click_random_element("agePage")
                page.click_random_element("loanAmountPage")
                ad_clicker.select_random_ad(ad_log_file)

        else:
            for action in page_actions[target_page]:
                page.click_random_element(action)
