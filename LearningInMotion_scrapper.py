#!/usr/bin/env python
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
import pyderman as dr
from getpass import getpass
from os import system, name 
from time import sleep

def DEBUG_clear_console(): 
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear')
#end def


# install required driver for chrome
## TODO: generalize this for other browsers
path = dr.install(browser=dr.chrome)
print('Installed chrome driver to path: %s' % path)

#######################################
#  Metadata - Get data required
#######################################
NetlinkID = input("Enter NetlinkID: ")
Password = getpass("Enter Password: ")

#######################################
#  UVic - Student Login Screen
#######################################
#Create a webdriver instance
driver = webdriver.Chrome(path)
DEBUG_clear_console()
# Starting point - login as a student
URL = 'https://learninginmotion.uvic.ca/students/NetlinkID/student-login.htm'
#Go to page in URL
driver.get(URL)
# Wait until page loads
driver.implicitly_wait(1.5)
#Assert that this is the login page
assert "University of Victoria - Sign in Service" in driver.title
#Get the elements for username and password
elem_NetlinkID = driver.find_element_by_id('username')
elem_Password = driver.find_element_by_id('password')
elem_submit = driver.find_element_by_id('form-submit')
#Send the keys - clear existing text, enter data, press 'enter'
elem_NetlinkID.clear()
elem_Password.clear()
elem_NetlinkID.send_keys(NetlinkID)
elem_Password.send_keys(Password)
elem_submit.click()
# TODO: put error control incase this either id or password is wrong

#######################################
#  Learning in Motion (LIM)
#######################################
# wait 2 seconds for page to load
driver.implicitly_wait(3)
# Get new URL
URL = driver.current_url

# click on search postings
elem_SearchPostings = driver.find_element_by_link_text("Search Postings").click()
driver.implicitly_wait(0.5)

# click on co-op postings
elem_SearchPostings_CoopPostings = driver.find_element_by_link_text("Co-op postings").click()
driver.implicitly_wait(1.5)

# click on "all postings" button
elem_Postings = driver.find_element_by_xpath("//input[@type='submit']").click()
driver.implicitly_wait(0.5)

# Make a list of all job listings
elem_JobList = driver.find_elements_by_css_selector("tr.searchResult")

# go to each job posting and download the pdf of the posting
p = driver.current_window_handle
numOfListings = len(elem_JobList)
for n in range(0, numOfListings):
    # open the job listing
    listing = elem_JobList[n]
    # find the title of the posting
    ## on the 4th tr tag on a job entry
    tdTagList = listing.find_elements_by_tag_name("td")[3]
    title = tdTagList.get_attribute("data-totitle")
    # find the span element that contains the link to the posting via "title"
    link = listing.find_element_by_xpath("//span[@title='"+title+"']")
    link.click()
    driver.switch_to.window(driver.window_handles[1])

    # click print
    driver.implicitly_wait(0.5)
    elem_PrintPDF = driver.find_element_by_link_text("Print").click()
    #close tab
    driver.close()
    driver.switch_to.window(p)
    driver.implicitly_wait(0.8)



#close session
driver.close()