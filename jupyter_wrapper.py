from __future__ import print_function
from . import manage_users as users
from IPython.display import display
from ipywidgets import *

class jupyter_wrapper(object):

	def __init__(self):
		self.add_students = widgets.Button(description="Add list of students")
		self.add_user = widgets.Button(description="Add user")
		self.remove_user = widgets.Button(description="Remove user")
		self.set_pass = widgets.Button(description="Set password")
		#Individual user form
		self.first = widgets.Text(description='First:')
		self.last = widgets.Text(description='Last:')
		self.ONID = widgets.Text(description='ONID:')
		self.email = widgets.Text(description='Email:')
		self.group = widgets.RadioButtons(description='Group:', options=['student', 'instructor'])
		self.submit = widgets.Button(description="Create Student")

		#remove user form
		self.user = widgets.Text(description='ONID:')

		#Change password form
		self.user2 = widgets.Text(description='ONID:')
		self.password = widgets.Text(description='Password:')

		#Form input
		#Combine widgets into lists for formatting
		name = [self.first , self.last]
		login = [self.ONID, self.email]
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


		self.draw_pages()

	def on_form_clicked(self, b):
		users.create_form()
		self.draw_pages()

	def on_submit_clicked(self, b):
		users.add_user(self.first.value, self.last.value, self.ONID.value,
			self.email.value, self.group.value, users.create_database())
		self.draw_pages()

	def draw_input_box(self):
		display(user_info)

	def on_add_clicked(self, b):
		self.draw_input_box()
		self.draw_pages()

	def on_remove_clicked(self, b):
		print(self.user.value)
		users.remove_user(self.user.value, users.create_database())
		self.draw_pages()

	def on_pass_clicked(self, b):
		users.set_custom_password(self.user2.value, self.password.value, users.create_database())
		self.draw_pages()

	def draw_pages(self):
		tabs = widgets.Tab(children = [self.page1, self.page2, self.page3, self.page4])
		display(tabs)

		tabs.set_title(0, 'Student List Input')
		tabs.set_title(1, 'Add User')
		tabs.set_title(2, 'Remove User')
		tabs.set_title(3, 'Change Password')

		self.submit.on_click(self.on_submit_clicked)
		self.add_students.on_click(self.on_form_clicked)
		self.add_user.on_click(self.on_add_clicked)
		self.remove_user.on_click(self.on_remove_clicked)
		self.set_pass.on_click(self.on_pass_clicked)

