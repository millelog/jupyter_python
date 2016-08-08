import sqlite3
import subprocess
import sys
import os
from datetime import datetime

class database(object):
	"""This class will do all read and writes to the username database"""
	def __init__(self):
		"""initialize the info dictionary and variables for database connection"""
		self.info = {'first' : [], 'last' : [], 'USER' : [], 'email' : [], 'pass' : [], 'group' : [] }
		self.db_path = "/srv/cgrb/database.sqlite"
		self.tn = 'users'
		self.user = 'USER'
		self.dp = 'default_pass'
		self.g = 'group'
		self.f = 'first'
		self.l = 'last'
		self.e = 'email'
		self.conn = self.get_connection()

	def get_connection(self):
		"""try a connection to the database path"""
		try:
			self.conn = sqlite3.connect(self.db_path)
		except sqlite3.Error:
			print("Error connecting to database")

	def create_table(self):
		self.get_connection()
		c = self.conn.cursor()
		#Create the table with the proper initial columns
		c.execute('''CREATE TABLE IF NOT EXISTS '{tn}' (
			'{id}' {tf} PRIMARY KEY,
			'{dp}' {tf} NOT NULL,
			'{gr}' {tf} NOT NULL,
			'{f}' {tf} NOT NULL,
			'{l}' {tf} NOT NULL,
			'{e}' {tf} NOT NULL);'''\
			.format(tn=self.tn, id=self.user, tf='TEXT', dp=self.dp, gr=self.g, f=self.f, l=self.l, e=self.e))
		#print confimration and commit changes
		print('Database object instantiated')
		self.commit_db()

	def log_users_creation(self):
		with open("/srv/log.txt", "a") as log:
			for i in range(len(self.info['USER'])):
				log.write(str(datetime.now())+" : added to database : "+self.info['USER'][i]+" "+self.info['pass'][i]\
					+" "+self.info['first'][i]+" "+self.info['last'][i]+" "+self.info['group'][i]+" "+self.info['email'][i]+"\n")
			log.close()
	
	def replace_apostrophe(self, s):
		string = ''
		for i in range(len(s)):
			if s[i] == '\'':
				string+= '\"'
			else:
				string+=s[i]
		return string

	def replace_all_apostrophes(self):
		for array in self.info:
			for i in range(len(self.info[array])):
				self.info[array][i] = self.replace_apostrophe(self.info[array][i])
            
	def insert_info(self):
		"""Insert all of the information from the info dictionary into the sql database"""
		self.get_connection()
		c = self.conn.cursor()
		#For every USER in the dictionary
		for i in range(len(self.info['USER'])):
			#insert them into the database (I <3 SQL INJECTIONS)
			c.execute("INSERT OR REPLACE INTO '{tn}' ('{user}', '{dp}', '{g}', '{f}', '{l}', '{e}') VALUES ('{idv}', '{dpv}', '{gv}', '{fv}', '{lv}', '{ev}');".\
				format(tn=self.tn, user=self.user, dp=self.dp, g=self.g, f=self.f, l=self.l, e=self.e,
					idv=self.info['USER'][i], dpv=self.info['pass'][i], gv=self.info['group'][i],
					 fv=self.info['first'][i], lv=self.info['last'][i], ev=self.info['email'][i]))
		#Log this datbase manipulation
		self.log_users_creation()
		#commit to database and close connection
		self.commit_db()

	def set_info(self, info, group, passwds):
		"""Set the memeber dictionary for info to the dictionary parameter"""
		self.info = {'first' : [], 'last' : [], 'USER' : [], 'email' : [], 'pass' : [], 'group' : []}
		for i in range(len(info['USER'])):
			self.info['USER'].append(info['USER'][i])
			self.info['first'].append(info['first'][i])
			self.info['last'].append(info['last'][i])
			self.info['email'].append(info['email'][i])
			self.info['pass'].append(passwds[i])
			self.info['group'].append(group)
		self.replace_all_apostrophes()

	def remove_user(self, USER):
		"""Given an USER this function will remove that student from the database"""
		USER = USER.lower()
		self.get_connection()
		c = self.conn.cursor()
		#sql command string
		sql = """
		DELETE FROM {tn}
		WHERE {user} = '{u}';
		""".format(tn=self.tn, user=self.user, u=USER)
		#log the account deletion
		with open("/srv/log.txt", "a") as log:
			log.write(str(datetime.now())+" : deleted from database : "+USER+"\n")
			log.close()
		#Execute the command and commit it to the database
		c.execute(sql)
		self.commit_db()

	def get_instructors(self):
		self.get_connection()
		c=self.conn.cursor()
		users = []
		for row in c.execute("SELECT {user} FROM {tn} WHERE {gr} = {inst};".\
			format(user=self.user, tn = self.tn, gr = self.gr, inst = 'instructor')):
				users.append(row)
		return users
		
	def get_users(self):
		self.get_connection()
		c = self.conn.cursor()
		users = []
		for row in c.execute("SELECT {user} FROM {tn};".format(user=self.user, tn=self.tn)):
			users.append(row)
		return users

	def print_db(self):
		self.get_connection()
		c = self.conn.cursor()
		for row in c.execute("SELECT {id}, * FROM {tn} ORDER BY {user};".\
			format(id='rowid', tn=self.tn, user=self.user)):
			print(row)



	def commit_db(self):
		"""commit database changes in info and close the connection"""
		self.conn.commit()
		self.conn.close()



