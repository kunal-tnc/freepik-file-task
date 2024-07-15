from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from configs import CHROME_DRIVE_PATH, FREEPIK_LOGIN, FREEPIK_LOGO, download_directory


class FreepikDownloader:
    def __init__(self, chrome_driver_path, download_directory):
        self.chrome_driver_path = chrome_driver_path
        self.download_directory = download_directory
        self.driver = None

    def setup_driver(self):
        service = ChromeService(executable_path=self.chrome_driver_path)
        options = webdriver.ChromeOptions()
        options.add_experimental_option('prefs', {
            'download.default_directory': self.download_directory
        })
        self.driver = webdriver.Chrome(service=service, options=options)

    def login_to_freepik(self):
        try:
            self.driver.get(FREEPIK_LOGIN)


            iframe = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//iframe[@title='Sign in with Google Button']"))
            )
            self.driver.switch_to.frame(iframe)


            google_login_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and @aria-labelledby='button-label']"))
            )
            google_login_button.click()

            self.driver.switch_to.default_content()


            WebDriverWait(self.driver, 20).until(EC.number_of_windows_to_be(2))


            self.driver.switch_to.window(self.driver.window_handles[1])


            email_field = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='email']"))
            )
            email_field.send_keys("kunalgj06@gmail.com")
            email_field.send_keys(Keys.ENTER)


            password_field = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
            )


            WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='password']"))
            )


            self.driver.execute_script("arguments[0].scrollIntoView(true);", password_field)
            password_field.send_keys("kunal@tnc")
            password_field.send_keys(Keys.ENTER)


            self.driver.switch_to.window(self.driver.window_handles[0])

        except TimeoutException as e:
            print(f"TimeoutException during login: {e}")
        except Exception as e:
            print(f"Exception during login: {e}")

    def download_logo(self):
        try:
            self.driver.get(FREEPIK_LOGO)

            download_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-cy='wrapper-download-free']"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView();", download_button)
            self.driver.execute_script("arguments[0].click();", download_button)

            try:
                free_download_link = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//a[@data-cy='download-button' and contains(text(), 'Free download')]"))
                )
                free_download_link.click()

            except TimeoutException:
                print("Timeout waiting for the free download link to be clickable.")

            WebDriverWait(self.driver, 50).until(EC.url_changes(self.driver.current_url))
            print("File download initiated. Check your download directory.")

        except TimeoutException as e:
            print(f"TimeoutException during download: {e}")

    def quit_driver(self):
        if self.driver:
            self.driver.quit()



if __name__ == "__main__":
    chrome_driver_path = CHROME_DRIVE_PATH
    download_directory = download_directory

    downloader = FreepikDownloader(chrome_driver_path, download_directory)
    downloader.setup_driver()
    downloader.login_to_freepik()
    downloader.download_logo()
    downloader.quit_driver()
