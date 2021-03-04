import sys
import os
import shutil
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

PATH = "C:\Program Files (x86)\chromedriver.exe"
OPTIONS = webdriver.ChromeOptions()
OPTIONS.headless = True

no_output = True

def scrape_problems(contest, page, initial_cwd):
    print("called")
    
    driver = webdriver.Chrome(PATH, options=OPTIONS)
    driver.implicitly_wait(10)

    prevtitle = "Codeforces"
    driver.get("https://codeforces.com/problemset/problem/"+contest+"/"+chr(page+65))

    while driver.title != prevtitle:

        problem = driver.find_element_by_class_name("problem-statement")
        
        if initial_cwd is None: cwd = os.getcwd()
        else: cwd = initial_cwd
        path = os.path.join(cwd, contest, chr(page+65))
        shutil.rmtree(path, ignore_errors=True)
        os.makedirs(path)

        height = driver.execute_script("return document.body.scrollHeight")
        width = driver.execute_script("return document.body.scrollWidth")
        driver.set_window_size(width, height)
        problem.screenshot(os.path.join(path,"problem.png"))

        input_texts = driver.find_elements_by_class_name("input")
        output_texts = driver.find_elements_by_class_name("output")

        for i in range(len(input_texts)):
            input_list = input_texts[i].text.split("\n")[2:]
            output_list = output_texts[i].text.split("\n")[2:]
            input_file = open(os.path.join(path,"input"+str(i+1)+".txt"), "w+")
            output_file = open(os.path.join(path,"output"+str(i+1)+".txt"), "w+")
            for line in input_list:
                print(line, file = input_file)
            for line in output_list:
                print(line, file = output_file)
            input_file.close()
            output_file.close()

        prevtitle = driver.title
        page += 1
        driver.get("https://codeforces.com/problemset/problem/"+contest+"/"+chr(page+65))
        global no_output
        no_output = False
        if initial_cwd is not None: break

    driver.close()


contest = sys.argv[1]      #enter 0 to use the function under bonus 2 (searching by difficulty)
if contest != "0":
    scrape_problems(contest, 0, None)
    if no_output: print("Error: Contest not started.")
else:
    driver = webdriver.Chrome(PATH, options=OPTIONS)
    driver.implicitly_wait(10)

    driver.get("https://codeforces.com/problemset")
    n1, n2 = tuple(map(int, input("Enter difficulty range, space separated. (like 1500 1600): ").split()))
    mindiff = driver.find_element_by_name("minDifficulty")
    maxdiff = driver.find_element_by_name("maxDifficulty")
    div = driver.find_element_by_class_name("_FilterByTagsFrame_button")
    submit_button = div.find_element_by_tag_name("input")

    mindiff.send_keys(str(n1))
    maxdiff.send_keys(str(n2))
    submit_button.click()

    number_of_pages = 1
    pages_list = driver.find_elements_by_class_name("pagination")
    if len(pages_list) != 0: 
        pages = pages_list[0]
        last_page = pages.find_elements_by_tag_name("li")[-2]
        number_of_pages = int(last_page.text)
        last_page.click()

    table = driver.find_element_by_tag_name("table")
    entries = table.find_elements_by_tag_name("tr")

    total_questions = (number_of_pages-1)*100 + len(entries)-1
    if entries[1].text == "No items": total_questions = 0
    print("Total number of questions found in the given difficulty range: ", total_questions)
    if total_questions != 0: num_questions = int(input("How many do you want to practice? "))

    questions_per_page = num_questions//number_of_pages + 1

    while num_questions>0:
        table = driver.find_element_by_tag_name("table")
        entries = table.find_elements_by_tag_name("tr")

        used = []
        num = 0
        while len(used) != questions_per_page:
            if questions_per_page < len(entries)//5: num = random.randint(1, len(entries)-1)
            if num in used: continue
            used.append(num)
            
            if num>len(entries): break
            question = entries[num].find_element_by_tag_name("td")
            contest = question.text[:-1]
            contestq = ord(question.text[-1]) - 65
            cwd = os.getcwd()
            cwd = os.path.join(cwd, "Practice Questions")
            
            scrape_problems(contest, contestq, cwd)
            num_questions -= 1
            if num_questions == 0: break
            num += 1

        number_of_pages -= 1
        if questions_per_page - len(entries) <= 0: leftover = 0
        else: 
            leftover = questions_per_page - len(entries)
            questions_per_page = (questions_per_page*number_of_pages + leftover)//number_of_pages + 1

        pages_list = driver.find_elements_by_class_name("pagination")
        if len(pages_list) != 0:
            pages = pages_list[0]
            left_arrow = pages.find_elements_by_tag_name("li")[0]
            if left_arrow.text == "1": break
            left_arrow.click()

    print("You will find the requested questions in the 'Practice Questions' folder. Enjoy!")