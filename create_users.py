#!/usr/bin/env python
import sys
import subprocess
import pwd
import random
import smtplib

#Check if a given user name exists already
def is_user(user):
	try:
		pwd.getpwnam(user)
		return True
	except KeyError:
		return False

#add given user to the given group
def add_to_group(group, user):
	subprocess.check_output(["sudo", "usermod", "-a", "-G", group, user])
	#print confirmation
	print("Added "+user+" to group "+group)

#Generate a 10 character long string of randome lower case letters
def generate_passwd():
	s = "abcdefghijklmnopqrstuvwxyz1234567890"
	return ''.join(random.sample(s, 10))

#Initialize and greet the SMTP server.
def initialize_smtp_server(smtpserver, smtpport, email, pwd):
	smtpserver = smtplib.SMTP(smtpserver, smtpport)
	#this is my favorite function name ever
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.ehlo()
	smtpserver.login(email, pwd)
	return smtpserver

def send_instructor_email(instructor_email, users, passwds, emails, smtpserver):
	from_email = 'millelog@oregonstate.edu'
	subject = "New Users Added to Jupyterhub"
	message = """	To: %s
	From: %s
	Subject: New Users Added to Jupyterhub
	A list of new accounts has been added to the Jupyterhub interface. Their default credentials are as follows.
	""" %(instructor_email, from_email)

	for i in range(len(users)):
		message+="""Username: %s
		Password: %s
		Email: %s\n\n""" % (users[i], passwds[i], emails[i]) 

	mail = 'Subject: %s\n\n%s' % (subject, message)

	try:
		smtpserver.sendmail(from_email, instructor_email, mail)
	except SMTPException:
		print("Error: unable to send email")



def send_new_user_email(email, user, passwd, smtpserver):
	to_email = email
	from_email = 'millelog@oregonstate.edu'
	message = 'Subject: %s\n\n%s' % ("[Important] Jupyter Notebook Account","""To: %s <%s>
	From: Logan Miller <millelog@oregonstate.edu>
	Subject: [Important] Jupyter Notebook Account Password
	An account has been created under your ONID username and email for the online coding platform Jupyter Notebook. Please go to the link provided and use the following credentials to login.
	Username: %s
	Password: %s
	Link: http://52.87.197.201:8000
	""" % (user, email, user, passwd))

	try:
		smtpserver.sendmail(from_email, to_email, message)
	except smtplib.SMTPException:
		print("Error: unable to send email")

def create_user_root(user, passwd, group, email, smtpserver):
	#Create the user and set their default group
	subprocess.check_output(["useradd","-m", "-g", group, user])
	#Set their password
	subprocess.check_output(["/home/jupyter_python/passwd.exp", user, passwd])
    	#If they're an instructor add them to student group
	if(group == 'instructor'):
		add_to_group('student', user);
        
	#set all file permissions
	subprocess.check_output(["chown", ":instructor", "/home/"+str(user)])
	subprocess.check_output(["chmod", "-R", "770", "/home/"+str(user)])
    
    
	#send and email to this user with the random password
	send_new_user_email(email, user, passwd, smtpserver)
	print("User: "+user+" Password: " + passwd + " Email: " + email)

#Create the new user with given user name, group and password
def create_user(user, passwd, group, email, smtpserver):
	#Create the user and set their default group
	subprocess.check_output(["sudo","useradd","-m", "-g", group, user])
	#Set their password
	subprocess.check_output(["sudo","/home/jupyter_python/passwd.exp", user, passwd])
    #If they're an instructor add them to student group
	if(group == 'instructor'):
		add_to_group('student', user);
        
	#set all file permissions
	subprocess.check_output(["sudo", "chown", ":instructor", "/home/"+str(user)])
	subprocess.check_output(["sudo", "chmod", "-R", "770", "/home/"+str(user)])
    
    
	#send and email to this user with the random password
	send_new_user_email(email, user, passwd, smtpserver)
	print("User: "+user+" Password: " + passwd + " Email: " + email)

def create_all_users(users, emails, instructor_emails, smtpserver, group):
	#list of passwds
	passwds = []
	#For all the users in the file
	for user in users:
		#generate password for user
		passwd = generate_passwd()
		passwds.append(passwd)
		#if the user exists
		if is_user(user):
			#add the user to that group
			add_to_group(group, user)
		else:
			#create a new user
			create_user(user, passwd, group, emails[users.index(user)], smtpserver)


	for instructor_email in instructor_emails:
		send_instructor_email(instructor_email, users, passwds, emails, smtpserver)

	return passwds;
