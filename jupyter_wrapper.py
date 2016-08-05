from __future__ import print_function
import student_creation_form as form
import manage_users as users
from IPython.display import display
from ipywidgets import *

class jupyter_wrapper(object):

	def __init__(self):
		self.add_user = create_add_user()
		self.remove_user = self.create_remove_user()
		self.change_password = self.create_change_password()
		self.print_database = self.create_print_database()

	def create_add_user(self):
		b = widgets.Box(width="100%")      
		rows = [None] * 4
		rows[0] = widgets.HTML(value="<u><b>User Creation:</b></u>")
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
		rows[0] = widgets.HTML(value="<u><b>User Deletion:</b></u>")
		d = [widgets.Text(description='User:'), widgets.Button(description='Delete User', button_style = 'danger')]
		rows[1] = widgets.HBox(children=d)
		b.children = [r for r in rows]
		b.children[1].children[0].layout.margin = '0px 25px 0px 0px'
		return b

	def create_change_password(self):
		b = widgets.Box(width="100%")
		rows = [None] * 3
		rows[0] = [widgets.HTML(value="<u><b>Change Password:</b></u>")]
		rows[1] = widgets.Text(description='User:')
		p = [widgets.Text(description='Pass:'), widgets.Button(description='Set Password', button_style='primary')]
		rows[2] = widgets.HBox(children=p)
		b.children = [r for r in rows]
		b.children[2].children[0].layout.margin = '0px 25px 0px 0px'
		return b

	def create_print_database(self):
		return None

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

	def on_submit_clicked(self):
		if(self.verify_form()):
			self.add_user.children[0].value = "<u><b>User Creation:</b></u>"
			users.add_user(self.add_user.children[1].children[0].value,
				self.add_user.children[1].children[1].value,
				self.add_user.children[2].children[0].value,
				self.add_user.children[2].children[1].value,
				self.add_user.children[3].children[0].value.lower(),
				users.create_database())
		else:
			self.add_user.children[0].value = "<u><b>User Creation:</b></u>            <b><font color=\"red\">Invalid Character(s) in the Highlighted Field(s)</font></b>"


	def on_remove_clicked(self, b):
		db = users.create_database()
		user = self.remove_user.children[1].children[0].value
		if(users.valid_input(user)):
			self.remove_user.children[0].value="<b>User Deletion:</b>"
			if(user in db.get_users()):
				users.remove_user(self.remove_user.children[1].children[0].value, db)
			else:
				self.remove_user.children[0].value="<b>User Deletion: <font color=\"red\">Username not found in database</font></b>"
		else:
			self.remove_user.children[0].value="<b>User Deletion: <font color=\"red\">Invalid Character(s)</font></b>"

	def on_pass_clicked(self, b):
		#First para is user second is password
		users.set_custom_password(self.change_password.children[1].value, 
			self.change_password.children[2].children[0].value, 
			users.create_database())
        
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
		display(self.print_database)
