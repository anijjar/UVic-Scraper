#!/usr/bin/env python
from tkinter import *
import sys
import os
import subprocess
import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

first_iteration = True
##
#       Known Bugs
# - Will skip the last posting always
# - Occasionally stop at a few postings
# - Cannot hide the browser using the headless command
# - 
#       Things to fix/add
# - join the secondary thread with the main one when the quit or x button is pressed
# - add some details to the toolbar to make it look legit
# - choose some color pallet
# - have it save to a different location
#    - run the organize script or print script or etc. 
##      
class Toolbar:
    def __init__ (self, _win):
        self.rt = _win
        self.menubar = Menu(self.rt)
        self.rt.config(menu=self.menubar)

        fileMenu = Menu(self.menubar, tearoff=False)
        editMenu = Menu(self.menubar, tearoff=False)
        viewMenu = Menu(self.menubar, tearoff=False)
        helpMenu = Menu(self.menubar, tearoff=False)
        fileMenu.add_command(label="Exit", command=quit)
        helpMenu.add_command(label="Info", command=self.modal_info)
        fileMenu.add_command(label="Print", command=quit)
        self.menubar.add_cascade(label="File", menu=fileMenu)
        self.menubar.add_cascade(label="Edit", menu=editMenu)
        self.menubar.add_cascade(label="View", menu=viewMenu)
        self.menubar.add_cascade(label="Help", menu=helpMenu)

    def modal_info(self):
        Win2 = Toplevel(self.rt)
        Win2.configure(bg='#bebebe')
        Win2.title("Info Menu")
        Win2.iconbitmap(r"./assets/logo.ico")
        Win2.greeting = Label(Win2, text="Motivation", bg='#bebebe',fg='#444444')
        Win2.message = Label(Win2, text="Hope this app helps you as it helped me. \nNot sure if UVic will get angry about something like \nthis being public knowledge, but if anyone has a problem, email me at \nanijjar@uvic.ca and I will take it down. If anyone wants to hang out, \nhmu or checkout AUVIC. All the best!", bg='#bebebe',fg='#444444')
        Win2.greeting.config(font=("Courier", 12, 'bold'))
        Win2.message.config(font=("courier", 11))
        Win2.greeting.pack(padx=10,pady=(5,0))
        Win2.message.pack(padx=10,pady=(5,0))
     
class Main:
    def __init__ (self, _win):
        self.rt = _win
        self.rt.configure(bg='#f4d476')
        self.rt.bind('<Return>', self.threadExecute)
        self.rt.bind('<Escape>', self.exit_app)

        self.rt.greeting = Label(self.rt, text="Enter your credentials", bg='#bebebe', fg='#444444')
        self.rt.greeting.config(font=("Courier", 12, 'bold'))
        self.rt.greeting.pack(padx=10,pady=(5,0))
        
        self.rt.netlinkID = Entry(self.rt)
        self.rt.netlinkID.insert(0,'--NetlinkID--')
        self.rt.netlinkID.pack(padx=10,pady=(5,0))
        self.rt.netlinkID.bind("<FocusIn>", lambda args: self.rt.netlinkID.delete('0', 'end'))
        
        self.rt.Password = Entry(self.rt,show="*")
        self.rt.Password.insert(0,'--Password--')
        self.rt.Password.pack(padx=10,pady=(5,0))
        self.rt.Password.bind("<FocusIn>", lambda args: self.rt.Password.delete('0', 'end'))

        self.rt.frm1 = Frame(self.rt, bg='#bebebe')
        self.rt.frm1.pack(padx=10,pady=(5,0))
        self.rt.btn_quit = Button(self.rt.frm1, text="   Quit   ", command=self.exit_app)
        self.rt.btn_go = Button(self.rt.frm1, text=" Execute  ", command=self.threadExecute)
        self.rt.btn_quit.grid(column=0, row=0,padx=8,pady=(5,5))
        self.rt.btn_go.grid(column=1, row=0,padx=8,pady=(5,5))
        
        self.rt.h1 = Label(self.rt, text="Job Postings Obtained", bg='#bebebe',fg='#444444')
        self.rt.h1.config(font=("Courier", 12))
        self.rt.h1.pack(padx=10,pady=(5,0))
        
        self.rt.frm2 = Frame(self.rt) #show job postings collected after execute
        self.rt.frm2.pack(padx=10,pady=(5,10))
        self.rt.scroll = Scrollbar(self.rt.frm2, orient=VERTICAL)
        self.rt.select = Listbox(self.rt.frm2, yscrollcommand=self.rt.scroll.set, height=8)
        self.rt.scroll.config(command=self.rt.select.yview)
        self.rt.scroll.pack(side=RIGHT, fill=Y)
        self.rt.select.pack(side=LEFT, fill=BOTH, expand=1)


    def threadExecute(self, event=None):
        t = threading.Thread(target=self.execute).start()
        #update list

   
    #get job postings from LIM
    def execute(self):
        print("Getting data from website")

        netlinkID = self.rt.netlinkID.get()
        password = self.rt.Password.get()

        #######################################
        #  UVic - Student Login Screen
        #######################################
        #Create a webdriver instance
        driver = webdriver.Chrome(executable_path='./driver/chromedriver.exe')
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
        driver.find_element_by_link_text("Search Postings").click()
        driver.implicitly_wait(0.5)

        # click on co-op postings
        driver.find_element_by_link_text("Co-op postings").click()
        driver.implicitly_wait(0.5)

        # click on "all postings" button
        driver.find_element_by_xpath("//input[@type='submit']").click()
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
            listing.find_element_by_xpath("//span[@title='"+title+"']").click()
            driver.switch_to.window(driver.window_handles[1])

            # click print
            driver.implicitly_wait(0.2)
            driver.find_element_by_link_text("Print").click()
            driver.implicitly_wait(5)

            # add the name of the file to a global list

            #close tab
            driver.close()
            driver.switch_to.window(p)
            driver.implicitly_wait(0.5)

        #close session
        driver.close()
            
    
    #delete selected job applications
    def delete(self):
        print("the delete button has been pressed")
    
    #modal of message
    def error_msg(self,msg):
        #make new window
        #add new label
        #add a close button
        pass
    
    def exit_app(self,event=None):
        sys.exit()

    #adds pdf found to listbox
    def add_to_listBox(self):    
        pass

def CENTER_DEBUG_SCREEN(argument):
    # Gets the requested values of the height and widht.
    windowWidth = argument.winfo_reqwidth()
    windowHeight = argument.winfo_reqheight()
    
    # Gets both half the screen width/height and window width/height
    positionRight = int(argument.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(argument.winfo_screenheight()/2 - windowHeight/2)
    
    # Positions the window in the center of the page.
    argument.geometry("+{}+{}".format(positionRight, positionDown))

class MainApplication:
    def __init__ (self, _win):
        self.rt = _win
        self.rt.title("LIM-scrapper")
        self.rt.iconbitmap(r"./assets/logo.ico")
        self.rt.resizable(width=False, height=False)
        #initialize toolbar
        Toolbar(self.rt)
        #initlaize Main screen
        Main(self.rt)
        #clear the console for debugging
        CENTER_DEBUG_SCREEN(self.rt)
        
    
if __name__ == '__main__':
    os.system('CLS')
    win = Tk()
    MainApplication(win)
    win.mainloop()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    