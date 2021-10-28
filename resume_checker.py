import os
import re
import sys
from time import sleep
from termcolor import cprint, colored
from sklearn.metrics.pairwise import cosine_similarity
from configs import file_net_path as saved_net_res, job_net_path as testjob
# Custom imports from secrets (configs) and defs
from setup_defs import compile_patterns, screen_clear, make_menu, format_main_menu, read_local_res, read_local_job,\
    create_vectorized_obj

print_red = lambda x: cprint(x, 'red')  # Simplified Lamda initializations..
welcome_txt = "Kyle\'s Resume Checker"
opts_lst = ['Compare Resume Against Saved Job Description', 'Browse For Job Description Online', 'Quit']
loc_res = os.getcwd() + '/res_files/local_res.txt'
loc_job_desc = os.getcwd() + '/res_files/loc_job_desc.txt'
farewell = "Thank you for using the app. Good-bye!"
reg_patterns = {
    'menu_sel_pattern': '^[1-3]{1}',
}
valid_int = False
raw_reg_dict = compile_patterns(reg_patterns)
# for pattern in raw_reg_dict:
#     print(f"Pattern is {pattern} and type is {raw_reg_dict[pattern]}")
opts_dict = make_menu(opts_lst[0], opts_lst[1], opts_lst[2])

while not valid_int:
    screen_clear()
    format_main_menu(welcome_txt, opts_dict)
    choice = input("=> ").strip()
    if re.fullmatch(raw_reg_dict.get('menu_sel_pattern', 'Empty'), choice):
        valid_int = True
        choice = int(choice)
        if choice == 1:
            dump_res = read_local_res(saved_net_res, loc_res)
            dump_job_desc = read_local_job(testjob, loc_job_desc)
            c_matrix = create_vectorized_obj(dump_res, dump_job_desc)
            print(f"Similarity Scores:\n{cosine_similarity(c_matrix)}")
            # Now, covert that data to percentage for friendly viewing, pull col value ..
            match_percentage = cosine_similarity(c_matrix)[0][1] * 100
            match_percentage = round(match_percentage, 2) # 2 decimal places
            if match_percentage < 50:
                match_percentage = colored(str(match_percentage) + '%', 'red')
            else:
                match_percentage = colored(str(match_percentage) + '%', 'green')
            print(f"\nKyle's resume matches approximately {(match_percentage)}"
                  f" of the job description.")
        elif choice == 2:
            pass
        elif choice == 3:
            screen_clear()
            print(farewell)
            sys.exit(0)
    else:
        print_red(f"Input {choice.strip()} is invalid. Please enter an option number.")
        sleep(1)  # will give user time to read error before infinite menu loop repeats
