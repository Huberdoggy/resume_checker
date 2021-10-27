from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By # for find_element args
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import docx2txt
from time import sleep
# Custom imports from secrets (configs)
from configs import file_net_path as fp, phone_input as p_i, pass_input as p_word

opts = Options()
opts.add_argument("--no-sandbox") # For running headless with no defined user to avoid errors


while True:
    term_ = input("Enter the phrase you want to use in the job search query => ")
    if term_ == "q":
        break
    else:
        # Store chrome driver methods
        # This will bypass the need to install/point the code to a chrome driver executable
        s = Service(ChromeDriverManager().install())  # we create/pass an object to bypass deprecation warning
        driver = webdriver.Chrome(service=s)
        # Open target URL
        driver.get("https://www.linkedin.com")
        sleep(2)
        u_name_input = driver.find_element(By.XPATH, "//*[@id='session_key']")
        u_name_input.send_keys(p_i)  # send phone number cred
        sleep(2)
        p_word_input = driver.find_element(By.XPATH, "//*[@id='session_password']")
        p_word_input.send_keys(p_word)  # send pass cred
        click_login = driver.find_element(By.CLASS_NAME, "sign-in-form__submit-button").click()
        sleep(5)  # Longer delay to ensure page elements completely load
        # From homepage, search a job
        job_button = driver.find_element(By.LINK_TEXT, "Jobs").click()
        sleep(2)
        job_search = driver.find_element(By.TAG_NAME, "input")
        job_search.send_keys(term_)
        # For simplicity instead of targeting 'Search' btn
        press_enter = driver.find_element(By.TAG_NAME, "input").send_keys(Keys.RETURN)
        #  # Pass a tuple to expected conditions...
        # element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "job-details")))
        # description_select = driver.find_element(By.ID, "job-details").send_keys(Keys.CONTROL+"a")
        # sleep(5)

        # resume = docx2txt.process(fp)
        # print(resume)



