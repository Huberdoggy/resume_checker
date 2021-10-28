import os
import sys, re
from time import sleep
from termcolor import cprint, colored
from os import system, name
from sklearn.feature_extraction.text import CountVectorizer
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By  # for find_element args
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import docx2txt
from pyfiglet import Figlet
# Custom imports from secrets (configs)
from configs import phone_input as p_i, pass_input as p_word

print_red = lambda x: cprint(x, 'red')  # Simplified Lamda initializations..
print_green = lambda x: cprint(x, 'green')


def compile_patterns(pattern_dict):  # Modified this to pass dic and
    # follow proper method of compiling raw regex - stored in new returned dict
    new_dict = {}
    for str_pattern in pattern_dict:
        try:
            raw_reg = re.compile(fr'{pattern_dict[str_pattern]}')
            new_dict[str_pattern] = raw_reg
        except re.error:
            print(f"Invalid regex expression {pattern_dict[str_pattern]}")
    return new_dict


def screen_clear():
    # Function to accomplish the same thing as running term clear command to prevent clutter in prog
    if name == 'nt':  # In the rarer circumstance I'm running on Windows
        _ = system('cls')  # Store in underscore as variable to align with the fact a Py shell always stores
        # its last output in an underscore
    else:  # For 'Nix
        _ = system('clear')


def make_menu(opts1, opts2, opts3):
    """Make a numeric option menu for the user
    Run as an infinite loop in main.py until 'quit' is chosen"""
    my_dict = {1: opts1,
               2: opts2,
               3: opts3,
               }
    return my_dict


def format_main_menu(render_str, m_dict):
    f = Figlet(font='standard', justify='center')
    print(f"{colored(f.renderText(render_str), 'blue')}\n")
    print_green(f"\tPlease enter a number corresponding to one of the following:\n")
    print("\t" * 3 + ("*" * 30))
    for key in m_dict:
        print_green("\t" * 3 + str(key) + ' - ' + m_dict[key])
    print("\t" * 3 + ("*" * 30))


def read_local_res(src_resume, dest_resume):
    if os.path.exists(src_resume):
        os.system(f'cp -u {src_resume} {dest_resume}') # only --update after the first test succeeded
        loc_resume = docx2txt.process(dest_resume)
        return loc_resume
    else:
        print("The specified file %s does NOT exist.." % src_resume)
    return None


def read_local_job(src_job, dest_job):
    if os.path.exists(src_job):
        os.system(f'cp {src_job} {dest_job}') # only --update after the first test succeeded
        loc_job = docx2txt.process(dest_job)
        return loc_job
    else:
        print("The specified file %s does NOT exist.." % src_job)
    return None


def create_vectorized_obj(res_file, job_desc_file):
    text_lst = [res_file, job_desc_file] # store the passed res file and job desc
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(text_lst)
    return count_matrix


def selenium_scrape():
    opts = Options()
    opts.add_argument("--no-sandbox")  # For running headless with no defined user to avoid errors

    term_ = input("Enter the phrase you want to use in the job search query => ")
    if term_ == "q":
        sys.exit(0)
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
        driver.find_element(By.CLASS_NAME, "sign-in-form__submit-button").click()
        sleep(5)  # Longer delay to ensure page elements completely load
        # From homepage, search a job
        driver.find_element(By.LINK_TEXT, "Jobs").click()
        sleep(2)
        driver.find_element(By.TAG_NAME, "input").send_keys(term_)
        driver.find_element(By.TAG_NAME, "input").send_keys(Keys.RETURN)
        # For simplicity instead of targeting 'Search' btn
        sleep(10)

        #  # Pass a tuple to expected conditions...
        # element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "job-details")))
        # description_select = driver.find_element(By.ID, "job-details").send_keys(Keys.CONTROL+"a")
        # sleep(5)

        # resume = docx2txt.process(fp)
        # print(resume)
