from __future__ import print_function
import student_creation_form as form
import manage_users as users
from IPython.display import display
from ipywidgets import *

class jupyter_wrapper(object):

	def __init__(self):
		self.add_user = self.create_add_user()
		self.remove_user = self.create_remove_user()
		self.change_password = self.create_change_password()
		self.print_database = self.create_print_database()
		self.has_run = False

	def create_add_user(self):
		b = widgets.Box(width="100%")      
		rows = [None] * 4
		rows[0] = widgets.HTML(value="<b>User Creation:</b>")
		name = [widgets.Text(description='First:'), widgets.Text(description='Last:')]
		rows[1] = widgets.HBox(children=name)
		user = [widgets.Text(description='User:'), widgets.Text(description='Email:')]
		rows[2] = widgets.HBox(children=user)
		rows[3] = widgets.HBox(children = [widgets.RadioButtons(description='Group:', options=['Student', 'Instructor']),
			widgets.Button(description='Create User', button_style='success')])
		b.children = [r for r in rows]
		b.children[3].children[1].layout.margin='10px 0px 0px 250px'
		return b

	def create_remove_user(self):
		b = widgets.Box(width="100%")      
		rows = [None] * 2
		rows[0] = widgets.HTML(value="<b>User Deletion:</b>")
		d = [widgets.Text(description='User:'), widgets.Button(description='Delete User', button_style = 'danger')]
		rows[1] = widgets.HBox(children=d)
		b.children = [r for r in rows]
		b.children[1].children[0].layout.margin = '0px 25px 0px 0px'
		return b

	def create_change_password(self):
		b = widgets.Box(width="100%")
		rows = [None] * 3
		rows[0] = widgets.HTML(value="<b>Change Password:</b>")
		rows[1] = widgets.Text(description='User:')
		p = [widgets.Text(description='Pass:'), widgets.Button(description='Set Password', button_style='primary')]
		rows[2] = widgets.HBox(children=p)
		b.children = [r for r in rows]
		b.children[2].children[0].layout.margin = '0px 25px 0px 0px'
		return b

	def create_print_database(self):
		return widgets.Button(description='Print Database', button_style='primary')

	def verify_form(self):
		valid = True
		#First name
		if not users.valid_input(self.add_user.children[1].children[0].value):
			self.add_user.children[1].children[0].layout.border='3px solid red'
			valid = False
		else:
			self.add_user.children[1].children[0].layout.border=''
		#Last name
		if not users.valid_input(self.add_user.children[1].children[1].value):
			self.add_user.children[1].children[1].layout.border='3px solid red'
			valid = False
		else:
			self.add_user.children[1].children[1].layout.border=''
		#Username
		if not users.valid_input(self.add_user.children[2].children[0].value):
			self.add_user.children[2].children[0].layout.border='3px solid red'
			valid = False
		else:
			self.add_user.children[2].children[0].layout.border=''
		#Email
		if not users.valid_input(self.add_user.children[2].children[1].value):
			self.add_user.children[2].children[1].layout.border='3px solid red'
			valid = False
		else:
			self.add_user.children[2].children[1].layout.border=''
		return valid

	def successful_creation(self):
		self.add_user.children[1].children[0].value=''
		self.add_user.children[1].children[1].value=''
		self.add_user.children[2].children[0].value=''
		self.add_user.children[2].children[1].value=''
		self.add_user.children[1].children[0].value = "<b>User Creation: {name} was created successfully</b>".format(name=self.add_user.children[1].children[0])

	def on_submit_clicked(self, b):
		db = users.create_database()
		if(self.verify_form()):
			if not self.add_user.children[2].children[0].value in db.get_users():
				self.add_user.children[0].value = "<b>User Creation:</b>"
				users.add_user(self.add_user.children[1].children[0].value,
					self.add_user.children[1].children[1].value,
					self.add_user.children[2].children[0].value,
					self.add_user.children[2].children[1].value,
					self.add_user.children[3].children[0].value.lower(),
					db)
				self.successful_creation()
			else:
				self.add_user.children[0].value = "<b>User Creation:<font color=\"red\"> User already exists in the database</font></b>"	
		else:
			self.add_user.children[0].value = "<b>User Creation:</b>            <b><font color=\"red\">Invalid Character(s) in the Highlighted Field(s)</font></b>"


	def on_remove_clicked(self, b):
		db = users.create_database()
		user = self.remove_user.children[1].children[0].value
		if(users.valid_input(user)):
			self.remove_user.children[0].value="<b>User Deletion:</b>"
			if(user in db.get_users()):
				#remove user
				users.remove_user(self.remove_user.children[1].children[0].value, db)
				#Reset the fields to blank
				self.remove_user.children[1].children[0].value = ''
				#Success message
				self.remove_user.children[0].value="<b>User Deletion: {user} was deleted successfully</b>".format(user=user)
			else:
				#User not found in database
				self.remove_user.children[0].value="<b>User Deletion: <font color=\"red\">Username not found in database</font></b>"
		else:
			#Invalid characters in form
			self.remove_user.children[0].value="<b>User Deletion: <font color=\"red\">Invalid Character(s)</font></b>"

	def on_pass_clicked(self, b):
		#First para is user second is password
		db = users.create_database()
		#If the user is in the database
		if(self.change_password.children[1].value in db.get_users()):
			#set password
			users.set_custom_password(self.change_password.children[1].value, 
				self.change_password.children[2].children[0].value, db)
			#Reset fields
			self.change_password.children[1].value = ''
			self.change_password.children[2].children[0].value = ''
			#Success message
			self.change_password.children[0].value = "<b>Change Password: {name}'s password changed</b>".format(name=self.change_password.children[1].value)
		else:
			self.change_password.children[0].value = "<b>Change Password: <font color=\"red\">Username not found in database</font></b>"
			#user not found in database
        
	def on_print_clicked(self, b):
		db = users.create_database()
		db.print_db()

	def draw_input_form(self):
		form.student_creation_form()

	def draw_user_creation(self):
		display(self.add_user)
		self.add_user.children[3].children[1].on_click(self.on_submit_clicked)

	def draw_user_deletion(self):
		display(self.remove_user)
		self.remove_user.children[1].children[1].on_click(self.on_remove_clicked)

	def draw_change_password(self):
		display(self.change_password)
		self.change_password.children[2].children[1].on_click(self.on_pass_clicked)

	def print_db(self):
		self.has_run = True
		display(self.print_database)
		self.print_database.on_click(self.on_print_clicked)
