from __future__ import print_function
import manage_users as users
from IPython.display import display
from ipywidgets import *

class jupyter_wrapper(object):

	def __init__(self):
		#tab submit buttons         
		self.add_students = widgets.Button(description="Add list of students")
		self.add_user = widgets.Button(description="Add user")
		self.remove_user = widgets.Button(description="Remove user")
		self.set_pass = widgets.Button(description="Set password")
		self.print_db = widgets.Button(description="Print user database")
		#Individual user form
		self.first = widgets.Text(description='First:')
		self.last = widgets.Text(description='Last:')
		self.USER = widgets.Text(description='USER:')
		self.email = widgets.Text(description='Email:')
		self.group = widgets.RadioButtons(description='Group:', options=['student', 'instructor'])
		self.submit = widgets.Button(description="Create User")

		#remove user form
		self.user = widgets.Text(description='USER:')

		#Change password form
		self.user2 = widgets.Text(description='USER:')
		self.password = widgets.Text(description='Password:')

		#Form input
		#Combine widgets into lists for formatting
		name = [self.first , self.last]
		login = [self.USER, self.email]
		group = [self.group, self.submit]

		#orient the boxes horizontally
		subcontainers = [widgets.HBox(children=name), 
						 widgets.HBox(children=login),
						 widgets.HBox(children=group)]

		#Contain all of these widgets into one box and format
		self.page1 = widgets.Box(children = [self.add_students])
		self.page2 = widgets.Box(children = subcontainers)
		self.page3 = widgets.Box(children = [self.user, self.remove_user])
		self.page4 = widgets.Box(children = [self.user2, self.password, self.set_pass])
		self.page5 = widgets.Box(children = [self.print_db])


		self.draw_pages()

	def on_form_clicked(self, b):
		users.create_form()
        
	def replace_apostrophe(self, s):
		string = ''
		for i in range(len(s)):
			if s[i] == '\'':
				string+= '\"'
			else:
				string+=s[i]
		return string
        
	def on_submit_clicked(self, b):
		if users.valid_input(self.first.value) and\
		users.valid_input(self.last.value) and\
		users.valid_input(self.USER.value) and\
		users.valid_input(self.email.value):
			print('Loading...')
			users.add_user(self.replace_apostrophe(self.first.value), self.replace_apostrophe(self.last.value), self.USER.value,
				self.replace_apostrophe(self.email.value), self.group.value, users.create_database())
		else:
			print('Invalid input(s). Please only use valid characters.')
			self.first.value=self.last.value=self.USER.value=self.email.value=""

	def draw_input_box(self):
		display(user_info)

	def on_add_clicked(self, b):
		print('Loading...')
		self.draw_input_box()

	def on_remove_clicked(self, b):
		print('Loading...')
		users.remove_user(self.user.value, users.create_database())

	def on_pass_clicked(self, b):
		print('Loading...')
		users.set_custom_password(self.user2.value, self.password.value, users.create_database())
        
	def on_print_clicked(self, b):
		db = users.create_database()
		db.print_db()

	def draw_pages(self):
		tabs = widgets.Tab(children = [self.page1, self.page2, self.page3, self.page4, self.page5])
		display(tabs)

		tabs.set_title(0, 'Student List Input')
		tabs.set_title(1, 'Add User')
		tabs.set_title(2, 'Remove User')
		tabs.set_title(3, 'Change Password')
		tabs.set_title(4, 'Print User Database')

		self.submit.on_click(self.on_submit_clicked)
		self.add_students.on_click(self.on_form_clicked)
		self.add_user.on_click(self.on_add_clicked)
		self.remove_user.on_click(self.on_remove_clicked)
		self.set_pass.on_click(self.on_pass_clicked)
		self.print_db.on_click(self.on_print_clicked)

