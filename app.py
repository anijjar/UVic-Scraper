#!/usr/bin/env python
import tkinter as tk
import subprocess
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
    
class Main:
    def __init__ (self, root):
        self.root = root
        self.root.title("LIM-scrapper")
        self.root.iconbitmap(r"./assets/logo.ico")
        self.root.geometry("250x150")
        self.root.resizable(width=False, height=False)
        frm_input = tk.Frame(master=self.root)
        self.root.lbl_netlinkID = tk.Label(
            master=frm_input, 
            text="Netlink ID:"
        )
        self.root.ent_netlinkID = tk.Entry(
            master=frm_input
        )
        self.root.lbl_password = tk.Label(
            master=frm_input, 
            text="Password:"
        )
        self.root.ent_password = tk.Entry(
            master=frm_input, 
            show="*"
        )

        frm_btns = tk.Frame(master=self.root)
        self.root.btn_quit = tk.Button(
            master=frm_btns,
            text="QUIT",
            fg="red",
            command=quit
        )       
        self.root.btn_getAllPDFs = tk.Button(
            master=frm_btns,
            text="Download All PDFs",
            fg="green",
            command=self.execute
        )
        self.root.lbl_netlinkID.pack()
        self.root.ent_netlinkID.pack()
        self.root.lbl_password.pack()
        self.root.ent_password.pack()
        frm_input.grid(row=0,column=0,padx=10)

        self.root.btn_quit.grid(row=0,column=0,padx=5)
        self.root.btn_getAllPDFs.grid(row=0,column=1,padx=5)
        frm_btns.grid(row=1,column=0,padx=10)
        
    def execute (self):
        global netlinkID = self.root.ent_netlinkID.get()
        global password = self.root.ent_password.get()
        #######################################
        #  UVic - Student Login Screen
        #######################################
        #Create a webdriver instance
        driver = webdriver.Chrome('./driver/chromedriver.exe')
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
        elem_NetlinkID.send_keys(netlinkID)
        elem_Password.send_keys(password)
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
        
    def get_driver(self,driver="chrome"):
        pass
        
    def start_batch(): 
       subprocess.call([r'C:\Users\Ron\Desktop\Run Batch\Matrix.bat'])
       
if __name__ == '__main__':
    root = tk.Tk()
    obj = Main(root)
    root.mainloop()