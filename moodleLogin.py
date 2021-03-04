from selenium import webdriver
from selenium.webdriver.common.keys import Keys

PATH = "C:\Program Files (x86)\chromedriver.exe"

driver = webdriver.Chrome(PATH)

driver.get("https://moodle.iitd.ac.in/login/index.php")

driver.implicitly_wait(5)

username = driver.find_element_by_id("username")
password = driver.find_element_by_id("password")

username.send_keys("me1200917")
password.send_keys(input("Enter password"))

form = driver.find_element_by_id("login")
captcha_text = form.text.split("\n")[3]
captcha_list = captcha_text.split()
captcha = driver.find_element_by_id("valuepkg3")
captcha.clear()

a = captcha_list[-4]
b = captcha_list[-2]

if captcha_list[-3] == "+": captcha.send_keys(str(a+b))
elif captcha_list[-3] == "-": captcha.send_keys(str(a-b))
else:
    if captcha_list[2] == "first": captcha.send_keys(str(a))
    else: captcha.send_keys(str(b))

button = driver.find_element_by_id("loginbtn")
button.click()