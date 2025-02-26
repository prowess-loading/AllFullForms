import random
from selenium.webdriver.common.by import By
from setup.smooth_scroll import SmoothScroll
from selenium.webdriver.support.ui import WebDriverWait
import time


class AdClicker:
    def __init__(self, driver):
        self.driver = driver

    def get_all_ads(self):
        elements = self.driver.find_elements(
            By.CSS_SELECTOR, "iframe[id^='aswift']")
        # By.CSS_SELECTOR, "div#ad_unit")

        primary_visible_ads = []

        for element in elements:
            height = self.driver.execute_script(
                "return arguments[0].offsetHeight;", element)

            if height > 0:
                primary_visible_ads.append(element)

        print(f"Total visible ads: {len(primary_visible_ads)}")
        # time.sleep(20000)
        return primary_visible_ads

    def select_random_ad(self, log_file):
        smooth_scroll = SmoothScroll(self.driver)
        primary_visible_ads = self.get_all_ads()

        if not primary_visible_ads:
            print("No visible ad found")
            return None

        selected_ad = random.choice(primary_visible_ads)
        ad_id = selected_ad.get_attribute("id")
        print(f"Selected ad: {ad_id}")

        # selected_ad_css = f"iframe[id='{ad_id}']"
        random_timeout = random.randint(1, 3)

        try:
            smooth_scroll.scroll_bottom_up_ad_click(
                # selected_ad_css, random_timeout, log_file)
                ad_id, random_timeout, log_file)

        except Exception as e:
            print(f"Error occurred while scrolling to ad and clicking: {e}")
