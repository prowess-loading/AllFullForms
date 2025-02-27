import random
import time
from setup.smooth_scroll import SmoothScroll


class Page:
    def __init__(self, driver):
        self.driver = driver
        self.navigator = SmoothScroll(driver)

    def click_random_element(self, action):
        actions = {
            "genderPage": self.navigator.scroll_bottom_up_button_click,
            "agePage": self.navigator.button_click,
            "loanTypePage": self.navigator.button_click,
            "loanAmountPage": self.navigator.scroll_bottom_up_button_click,
        }

        if action in actions:
            print(f"Clicking on {action}")
            actions[action]()
