#!/usr/local/bin/python2.7

from passlib.hash import sha256_crypt
import myfunc
import pageElements
import mysessions

class User(object):


	def __init__(self, username, password):
		self.uname=username.lower()
		self.pw = password
		self.hashed = sha256_crypt.encrypt(password)
		self.admin=False
		#self.session=mysessions.start()


	def createNew(self):
		db = myfunc.databaseConnection()
		cur = db.cursor()
		#check if username already exists
		if not (self.uname.lower().endswith("@infusionsoft.com") or self.uname.lower().endswith("@til.la")):
			return False
		countOfThisUserName = """SELECT COUNT(*) FROM users WHERE uname ="%s" """ %(self.uname)
		cur.execute(countOfThisUserName)
		total=cur.fetchall()

		if not(total[0][0]==0):
			return False
		else:
			isserver = myfunc.ISServer()
			usersName = self.uname[:self.uname.find('@')].replace('.',' ',1)
			newISContactID=isserver.addContact(usersName, self.uname)
			thishash = sha256_crypt.encrypt(self.uname)
			userAddStatement = """INSERT INTO users (uname, pass, daily, updates, namehash, isidnum) VALUES ("%s", "%s", %s, %s, "%s", %s)""" %(self.uname, self.hashed, self.daily, self.updates, thishash, newISContactID)
			cur.execute(userAddStatement)
			getuseridstatement = """SELECT id FROM users where uname = "%s" """ %(self.uname)
			cur.execute(getuseridstatement)
			userid = cur.fetchall()[0][0]
			addusertotallier = """INSERT INTO feedbackoverviewtotal (userid) VALUES (%s)""" %(userid)
			cur.execute(addusertotallier)
			# self.login()
			emailToSend=pageElements.verificationemail(thishash)
			isserver = myfunc.ISServer()
			isserver.sendEmail(emailToSend, asubject="Please Verify Your Account", contactList=[newISContactID,])
			return True
			# cur.execute("""SELECT LAST_INSERT_ID()""")
			# self.id=cur.fetchall()[0][0]

	def usernameExists(self):
		db = myfunc.databaseConnection()
		cur = db.cursor()
		#check if username already exists
		countOfThisUserName = """SELECT COUNT(*) FROM users WHERE uname ="%s" """ %(self.uname)
		cur.execute(countOfThisUserName)
		total=cur.fetchall()

		if (total[0][0]==0):
			return False
		else:
			return True

	def login(self):
		mysessions.start()
		db = myfunc.databaseConnection()
		cur = db.cursor()

		getPWField = """SELECT pass,id,admin,verified FROM users WHERE uname="%s" """ %(self.uname)

		cur.execute(getPWField)
		thisdata = cur.fetchall()
		try:
			storedpw = thisdata[0][0]
		except:
			return False
		if not(thisdata[0][3]==1):
			return False
		if (sha256_crypt.verify(self.pw, storedpw)):
			self.id=int(thisdata[0][1])
			if (thisdata[0][2]==1):
				self.admin=True
			mysessions.SESSION['user'] = self
			return True
		else:
			return False
	def indexpage(self):
		thishtml=pageElements.generateIndexPage()
		if self.admin:
			thishtml=thishtml+pageElements.adminNav()
		thishtml = thishtml+pageElements.footer()
		print thishtml
	def setPrefs(self, postdata):
		if postdata.has_key('daily'):
			self.daily=1
		else:
			self.daily=0
		if postdata.has_key('updates'):
			self.updates=1
		else:
			self.updates=0

	def sort(self, postdata={}):
		mysessions.start()
		#self.session=mysessions.start()
		if (postdata == {} ):
			self.indexpage()
		elif postdata.has_key('logout'):
			#mysessions.start()
			mysessions.destroy()
			#print mysessions.SESSION.output()
			thishtml = 	pageElements.loginpage()
			thishtml = thishtml + pageElements.footer()
		elif postdata.has_key('updateFromAllUsers'):
			#This watches for input from the admin all users page where they can set other accounts to active
			#inactive or admin/user
			myfunc.alluserupdate(postdata)
			thishtml = pageElements.listAllUsers()
			if self.admin:
				thishtml=thishtml+pageElements.adminNav()
			thishtml = thishtml+pageElements.footer()
			print thishtml
		elif postdata.has_key('singlesubmit'):
			#this loads the chat submission page
			thishtml = 	pageElements.individualAdd()
			if self.admin:
				thishtml=thishtml+pageElements.adminNav()
			thishtml = thishtml+pageElements.footer()
			print thishtml
		elif postdata.has_key('manageEmails'):
			#this loads the page that allows a single user to modify what emails they recieve
			thishtml = pageElements.notificationsManagement(self.id)
			if self.admin:
				thishtml=thishtml+pageElements.adminNav()
			thishtml = thishtml+pageElements.footer()
			print thishtml
		elif postdata.has_key('updatenotifications'):
			#this is the process that happes when a user updates their notifications
			myfunc.updateNotifications(self.id, postdata)
			thishtml = pageElements.notificationsManagement(self.id)
			if self.admin:
				thishtml=thishtml+pageElements.adminNav()
			thishtml = thishtml+pageElements.footer()
			print thishtml
		elif postdata.has_key('mysubmissions'):
			# a total over view on the users submissions
			thishtml = pageElements.seeMySubmissions(self.id)
			if self.admin:
				thishtml=thishtml+pageElements.adminNav()
			thishtml = thishtml+pageElements.footer()
			print thishtml
		elif postdata.has_key('singleChatSubmitted'):
			# the process that happens when A single chat is submitted
			myfunc.mainSequence(postdata['chatlog'].value, postdata['chatid'].value, self.id )
			self.indexpage()
		elif postdata.has_key('mode'):
			# this loads the cumulative information for a page
			thishtml = pageElements.cumulativePage(postdata['chat'].value)
			if self.admin:
				thishtml=thishtml+pageElements.adminNav()
			thishtml = thishtml+pageElements.footer()
			print thishtml
		elif postdata.has_key('chat'):
			# this loads the page where a user can provide feedback for a chat
			thishtml = pageElements.votingPage(postdata['chat'].value)
			if self.admin:
				thishtml=thishtml+pageElements.adminNav()
			thishtml = thishtml+pageElements.footer()
			print thishtml
		elif postdata.has_key('feedbacksubmit'):
			# this is the process where feedback from a submission page is saved. 
			myfunc.updateDatabase(postdata, self.id)
			thishtml = pageElements.cumulativePage(postdata['thischatid'].value)
			if self.admin:
				thishtml=thishtml+pageElements.adminNav()
			thishtml = thishtml+pageElements.footer()
			print thishtml
		elif postdata.has_key('useroverview'):
			# provides a simple overview of one users involvement
			thishtml = pageElements.overviewPage(self.id)
			if self.admin:
				thishtml=thishtml+pageElements.adminNav()
			thishtml = thishtml+pageElements.footer()
			print thishtml
		elif postdata.has_key('feedbackfrom'):
			#This is intended to display the feedback on one particular chat from one particular user
			thishtml = pageElements.oneUserFeedback(postdata['chatid'].value, postdata['feedbackfrom'].value)
			if self.admin:
				thishtml=thishtml+pageElements.adminNav()
			thishtml = thishtml+pageElements.footer()
			print thishtml
		elif postdata.has_key("ViewAllUsers"):
			#this provides a basic overview of all users information
			thishtml = pageElements.listAllUsers()
			if self.admin:
				thishtml=thishtml+pageElements.adminNav()
			thishtml = thishtml+pageElements.footer()
			print thishtml
		elif (postdata.has_key('seeAllActionBy') and self.admin):
			#This allows an admin to view a users overview page
			thishtml=pageElements.overviewPage(postdata['seeAllActionBy'].value)
			if self.admin:
				thishtml=thishtml+pageElements.adminNav()
			thishtml = thishtml+pageElements.footer()
			print thishtml
		elif (postdata.has_key('seeAllSubmissionsBy') and self.admin):
			#This loads all of the chats submitted by one users
			thishtml = pageElements.seeMySubmissions(postdata['seeAllSubmissionsBy'].value)
			if self.admin:
				thishtml=thishtml+pageElements.adminNav()
			thishtml = thishtml+pageElements.footer()
			print thishtml
		elif (postdata.has_key('seeAllFeedbackBy') and self.admin):
			#Allows admin to see all feedbacks left by one user
			thishtml = pageElements.seeFeedbackSubmissions(postdata['seeAllFeedbackBy'].value)
			if self.admin:
				thishtml=thishtml+pageElements.adminNav()
			thishtml = thishtml+pageElements.footer()
			print thishtml

		else:
			self.indexpage()










