from selenium import webdriver
from facebookbot import FacebookBot

usr = input('Username: ')
pwd = input('Password: ')

# Initiate webdriver - PhantomJS
print("Iniatiating PhantomJS")
driver = webdriver.PhantomJS()

myBot = FacebookBot(driver)
myBot.login(usr, pwd)

groups = myBot.collect_groups()

post = """ Sample Post """ # change this to what you will post to each group
myBot.post_to_groups(post, 500, groups)
