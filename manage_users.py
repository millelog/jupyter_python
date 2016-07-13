from . import student_creation_form as ipython_form
from . import create_users as create
from . import database as data
import sys
import subprocess
import argparse
# Hello :)

def add_user(first, last, user, email, group, db):
	#Format username
	user = user.lower()
	#Initalize Email server
	smtpserver = create.initialize_smtp_server('mail.engr.oregonstate.edu', 25, 'millelog', 'F1c2g3d4b5a')

	#create password then create student
	passwd = create.generate_passwd()
	create.create_user(user, passwd, group, email, smtpserver)
	#format for passing it into the database
	info = {'first' : [first], 'last' : [last], 'ONID' : [user], 'email' : [email] }
	db.set_info(info, group, [passwd])
	db.insert_info()
	print(user+' has been created sucesfully')

def remove_user(ONID, db):
	db.remove_user(ONID)
	subprocess.check_output(["sudo", "userdel", "-r", ONID])
	print(ONID+' has been deleted succesfully')

def set_custom_password(ONID, passwd, db):
	db.add_custom_password(ONID, passwd)
	subprocess.check_output(["sudo","./passwd.exp", ONID, passwd])
	print(ONID+' has changed their password succesfully')

def create_form():
	#display the table
	form = ipython_form.student_creation_form()


def create_database():
	db = data.database()
	db.create_table()
	return db

def valid_input(input_string):
        valid_string = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ@. '+"'"
        for char in input_string:
            if char not in valid_string:
                return False
        if not input_string:
            return False
        return True

def parse_args():
	#instantiate argument parser
	parser = argparse.ArgumentParser(description='Command line input to manage jupyter hub users')
	#add the possible arguments (functions above)
	parser.add_argument('-a', '--add_user', dest='user_info', nargs='+',
		help = "Create a new Jupyter user. \nFormat: manage_users.py --add_user <first> <last> <ONID> <email> <group>")
	parser.add_argument('-r', '--remove_user', dest='remove_student',
		help = "Delete a Jupyter user by ONID. \nFormat: manage_users.py --remove_user <ONID>")
	parser.add_argument('-p', '--password', dest='user_pass', nargs='+',
		help = "Set a custom password for a given ONID. \nFormat: manage_users.py --password <ONID> <password>")
	return parser.parse_args()

def main():
	#Parse command line arguments
	args = parse_args()
	#Instantiate database object
	db = create_database()
	#conditional statements to verify command line arguments
	if args.user_info and len(args.user_info)==5:
		#if all the args are valid
		if all(valid_input(arg) for arg in args.user_info):
			info = args.user_info
			#add the user
			add_user(info[0], info[1], info[2], info[3], info[4], db)
			print(info[2]+' was succesfully created.')
		else:
			print('Invalid inputs. please only use valid characters.')
	
	elif args.remove_student:
		#remove the given user
		remove_user(args.remove_student, db)
		print(args.remove_student+' was succesfully removed.')
	
	elif args.user_pass and len(args.user_pass)==2:
		#Set the custom password
		set_custom_password(args.user_pass[0], args.user_pass[1], db)
		print(args.user_pass[0]+'\'s password was succesfully changed')

	else:
		print('Invalid command line syntax. please use manage_users.py --help')

if __name__ == '__main__':
	main()
	