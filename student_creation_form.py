#Documentation:
#https://media.readthedocs.org/pdf/ipywidgets/latest/ipywidgets.pdf
from __future__ import print_function
from IPython.display import display
from ipywidgets import *

class student_creation_form(object):
   
    def __init__(self):
        #Instantiate master lists of all students info
        self.info = {'first' : [], 'last' : [], 'ONID' : [], 'email' : []}

        #Create slider widgets
        self.button = widgets.Button(description="Submit Number")
        self.students = widgets.IntSlider(min=1, max=50, step=1)

        #Define dictionary to hold the widgets necessary for each student
        self.first = {}
        self.last = {}
        self.ONID = {}
        self.email = {}
        self.HTML = {}
        self.submit = {}
        self.n = 0

        #draw the table
        self.draw_initial_slider();
        
    def draw_form(self, i):
        #Create the text box widgets
        self.first[i] = widgets.Text(description='First:')
        self.last[i] = widgets.Text(description='Last:')
        self.ONID[i] = widgets.Text(description='ONID:')
        self.email[i] = widgets.Text(description='Email:')
        self.submit[i] = widgets.Button(description="Create Student")
        self.HTML[i] = widgets.HTML(value="<b>Student "+str(i+1)+":</b>")

        #Combine widgets into lists for formatting
        name = [self.first[i] , self.last[i]]
        login = [self.ONID[i], self.email[i], self.submit[i]]

        #orient the boxes horizontally
        subcontainers = [self.HTML[i], widgets.HBox(children=name), 
                         widgets.HBox(children=login)]

        #Contain all of these widgets into one box and format
        student_info = widgets.Box(children = subcontainers)
        student_info.layout.border = '2px grey solid'
        display(student_info)
        self.submit[i].on_click(self.on_submit_clicked)


    #add all of the student's info to the student info dictionary
    def append_info(self, first, last, ONID, email):
        self.info['first'].append(first)
        self.info['last'].append(last)
        self.info['ONID'].append(ONID.lower())
        self.info['email'].append(email)

    #Draw first form when num_students submitted
    def on_button_clicked(self, b):
        self.draw_form(self.n)
        
    #close all of the widgets associated with taking input for student i
    def close_form(self, i):
        self.first[i].close()
        self.last[i].close()
        self.ONID[i].close()
        self.email[i].close()
        self.submit[i].close()
        self.HTML[i].value = "<b>Student "+str(i+1)+": "+self.info['first'][i]+" "+self.info['last'][i]+"</b>"
    
    #Draw the initial slider that gets number of students    
    def draw_initial_slider(self):
        #Display the initial slider
        display(widgets.HTML(value="<b>Number of Students:</b>"))
        display(self.students)
        display(self.button)
        
        #Listen for button clicks
        self.button.on_click(self.on_button_clicked)

    #Define the button's functionality
    def on_submit_clicked(self, b):
        #append student info with text boxes
        self.append_info(self.first[self.n].value, self.last[self.n].value, 
                    self.ONID[self.n].value, self.email[self.n].value)
        #close the current form
        self.close_form(self.n)
        #if student number is less than number of students
        if(self.n<self.students.value-1):
            #draw the next student's form
            self.n+=1
            self.draw_form(self.n)
        else:
            self.button.close()
            self.students.close()
            print("Form correctly submitted")
