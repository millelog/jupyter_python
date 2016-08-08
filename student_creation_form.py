#Documentation:
#https://media.readthedocs.org/pdf/ipywidgets/latest/ipywidgets.pdf
from __future__ import print_function
import manage_users as users
import create_users as create
from IPython.display import display
from ipywidgets import *
import ipywidgets as widgets

class student_creation_form(object):
   
    def __init__(self):
        #Instantiate master lists of all students info
        self.info = {'first' : [], 'last' : [], 'USER' : [], 'email' : []}
        self.rows = list()
        self.db = users.create_database()
        self.submit = widgets.Button(description = "Submit Students", button_style='success')
        self.header = widgets.HTML(value="<b>Add a new student to the class list</b>")
        self.header.layout.margin='6px 0px 0px 50px'
        self.draw_form()

    def logit(self, First, Last, User, Email):
            if not (self.valid_input(First) and self.valid_input(Last) and self.valid_input(User) and self.valid_input(Email)):
                for row in self.rows:
                    if(First == row.children[0].value and\
                      Last == row.children[1].value and\
                      User == row.children[2].value and\
                      Email == row.children[3].value):
                        row.layout.border='3px solid red'
                        self.header.value="<b><font color=\"red\">Invalid character on the highlighted row</font></b>"
                     if User in self.db.get_users():
                        row.layout.border='3px solid red'
                        self.header.value="<b><font color=\"red\">Highlighted user already exists in the database</font></b>"
            else:
                for row in self.rows:
                    if(First == row.children[0].value and\
                      Last == row.children[1].value and\
                      User == row.children[2].value and\
                      Email == row.children[3].value and\
                      not User in self.db.get_users()):
                        row.layout.border=''
                        self.header.value="<b>Add a new student or submit the current list of students</b>"



    def get_user_hbox(self):
        b = widgets.HBox(width = "100%")
        boxes = list()
        y = interactive(self.logit, First = "", Last = "", User="", Email="")
        y.children[0].layout.width = '20%'
        #y.children[0].layout.margin = '4px 15px 4px 0px'
        y.children[1].layout.width = '20%'
        #y.children[1].layout.margin = '4px 15px 4px 0px'
        y.children[2].layout.width = '20%'
        #y.children[2].layout.margin = '4px 15px 4px 0px'
        y.children[3].layout.width = '40%'
        #y.children[3].layout.margin = '4px 15px 4px 0px'
        boxes.extend(y.children)

        b.children = [b for b in boxes]
        return b

    def new_row(self, b):
        newrow = self.get_user_hbox()
        self.rows.append(newrow)
        if len(self.rows)>1:
            self.submit.close()
        display(newrow)
        self.submit = widgets.Button(description = "Submit Students", button_style='success')
        display(self.submit)
        self.header.value = "<b>Add a new student or submit the class list</b>"
        self.submit.on_click(self.on_submit_clicked)


    def draw_form(self):
        bt = widgets.Button(description = "New Student", button_style='primary')
        #submit = widgets.Button(description = "Submit Students", button_style='success')
        bt.on_click(self.new_row)
        top = widgets.HBox(children=[bt, self.header])
        display(top)

    #Input validator to protect from sql injection
    def valid_input(self, input_string):
        valid_string = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ@._ \''
        for char in input_string:
            if char not in valid_string:
                return False
        return True

    #Add the list of users to the database and create their accounts
    def add_users(self, info):
        #instantiate database object
        db = users.create_database()
        print('Working...')
        #Initalize Email server
        smtpserver = create.initialize_smtp_server('mail.engr.oregonstate.edu', 25, 'millelog', 'F1c2g3d4b5a')

        #create the users and grab the passwords that are returned
        passwds = create.create_all_users(info['USER'], info['email'], 
        smtpserver, 'student')

        #set the info dictionary for the database class
        db.set_info(info, 'student', passwds)

        #Insert and commit the information dictionary to the database
        db.insert_info()
        print("All students created succesfully")

    def valid_form(self):
        for row in self.rows:
            if(not (self.valid_input(row.children[0].value) and\
              self.valid_input(row.children[1].value) and\
              self.valid_input(row.children[2].value) and\
              self.valid_input(row.children[3].value))):
                return False;
            if not (row.children[0] or row.children[1] or\
                    row.children[2] or row.children[3]):
                return False;
        return True
    
    def on_submit_clicked(self, b):
        if(self.valid_form()):
            for row in self.rows:
                self.info['first'].append(row.children[0].value)
                self.info['last'].append(row.children[1].value)
                self.info['USER'].append(row.children[2].value)  
                self.info['email'].append(row.children[3].value)
            self.add_users(self.info)
        else:
            print("Invalid character(s) submitted")
