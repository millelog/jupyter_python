from . import student_creation_form as ipython_form
from . import create_users as create
from . import database as data
import sys
import subprocess

def add_users(db, info):
	print('Working... may take several minutes...')
	#Initalize Email server
	smtpserver = create.initialize_smtp_server('mail.engr.oregonstate.edu', 25, 'millelog', 'F1c2g3d4b5a')

	#create the users and grab the passwords that are returned
	group = 'student'
	passwds = create.create_all_users(info['ONID'], info['email'], 
		['milleflog@oregonstate.edu'], smtpserver, group)

	#set the info dictionary for the database class
	db.set_info(info, group, passwds)

	#Insert and commit the information dictionary to the database
	db.insert_info()

def add_user(first, last, user, email, db):
	#Format username
	user = user.lower()
	#Initalize Email server
	smtpserver = create.initialize_smtp_server('mail.engr.oregonstate.edu', 25, 'millelog', 'F1c2g3d4b5a')

	#Set values and create the student
	group = 'student'
	passwd = create.generate_passwd()
	create.create_user(user, passwd, group, email, smtpserver)
	#format for passing it into the database
	info = {'first' : [first], 'last' : [last], 'ONID' : [user], 'email' : [email] }
	db.set_info(info, group, [passwd])
	db.insert_info()

def remove_user(ONID, db):
	db.remove_user(ONID)
	subprocess.check_output(["sudo", "userdel", "-r", ONID])

def set_custom_password(ONID, passwd, db):
	db.add_custom_password(ONID, passwd)
	subprocess.check_output(["sudo","/home/bigbenny/jupyter_python/passwd.exp", ONID, passwd])

def create_form():
	#display the table
	form = ipython_form.student_creation_form()
	return form.info

def create_database():
	db = data.database()
	db.create_table()
	return db

def main():
	#instantiate databse if not already created
	db = create_database()
	#pipe the info from the widget form into the info dictionary
	info = create_form()
	#add the students from the info dictionary to the database
	add_students(db, info)
    

    
    

