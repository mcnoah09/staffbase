import os

import pytest
import selenium.webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


APPLICANT_DATA = {
    "first_name": "Noah",
    "last_name": "Afolabi",
    "email": "mcnoah2012@gmail.com",
    "phone": "+491752943463",
    "resume": "Noah_Afolabi_Resume_2022.pdf",
    "github_link": "https://github.com/mcnoah09/staffbase",
}


class TestStaffBaseApplication:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        options = selenium.webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--kiosk")
        options.add_experimental_option("prefs", {"profile.block_third_party_cookies": True})
        options.add_argument("--window-size=2500,1600")

        self.driver = selenium.webdriver.Chrome(service=Service("/usr/local/bin/chromedriver"), options=options)
        self.wait = WebDriverWait(self.driver, 20)
        yield
        self.driver.close()

    def test_qa_engineer_application(self):
        self.driver.get("https://staffbase.com/jobs/quality-assurance-engineer-2021_1730")
        # Reject cookies
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#onetrust-reject-all-handler"))).click()

        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Apply']"))).click()
        self.wait.until(EC.url_contains("apply"))
        self.wait.until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.CSS_SELECTOR, "iframe[id='grnhse_iframe'][title='Greenhouse Job Board']")
            )
        )
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#application_form")))

        # Enter required information in the application form
        f_name = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#first_name")))
        f_name.click()
        f_name.send_keys(APPLICANT_DATA["first_name"])

        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#last_name"))).send_keys(
            APPLICANT_DATA["last_name"]
        )
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#email"))).send_keys(
            APPLICANT_DATA["email"]
        )
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#phone"))).send_keys(
            APPLICANT_DATA["phone"]
        )
        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "form[id='s3_upload_for_resume'] input[type='file']"))
        ).send_keys(os.path.abspath(APPLICANT_DATA["resume"]))
        assert self.wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#resume_filename"), APPLICANT_DATA["resume"])
        )

        elm = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".select2-container")))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", elm)
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".select2-container"))).click()
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#select2-result-label-3"))).click()

        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#job_application_answers_attributes_2_text_value"))
        ).send_keys(APPLICANT_DATA["github_link"])

        # Submit application
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#submit_app"))).click()

        assert self.wait.until(EC.visibility_of_element_located((By.XPATH, "//*[text()='Thank you for applying.']")))
