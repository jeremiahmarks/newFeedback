#!/usr/local/bin/python2.7
import cgi
import cgitb

cgitb.enable()
import myfunc
import mysessions
import pfuser as users
import pageElements




def sorting(postdata):
	"""
	My basic logic:
		mysessions.start()

		if the post data says to send the daily email, send that ish.

		if the post data has login info, try and log info try and log in
			if successful,
				display main index
			if failure
				display faulure message and login screen
		elif the user is logged in:
			Lots of logic will go here.
		else
			delete the cookie and display the page


	"""
	mysessions.start()
	print "Content-type: text/html"

	if (postdata.has_key("emailRecent")):
		"""
		Add this function:
		myfunc.emailUpdates()
		"""
		pass
	if postdata.has_key('verification'):
		q0 = """SELECT COUNT(*) FROM users WHERE namehash = "%s" """ %(postdata['verification'].value)
		q1 = """SELECT * FROM users WHERE namehash = "%s" """ %(postdata['verification'].value)
		q2 = """UPDATE users SET verified = 1 WHERE namehash = "%s" """%(postdata['verification'].value)
		db=myfunc.databaseConnection()
		cur=db.cursor()
		cur.execute(q0)
		total=cur.fetchall()
		if not(total[0][0]==1):
			"""This means that there are either multiple of zero instances of the value"""
			cur.close()
			db.close()
			pass
		else:
			cur.execute(q1)
			values=cur.fetchall()
			cur.execute(q2)
			cur.close()
			db.close()
			print pageElements.successfulVerification(values[0])
			return 0
	if postdata.has_key('logout'):
		mysessions.SESSION.set_expires(-1)
		print mysessions.SESSION.output()
		thishtml = pageElements.loginpage()
		thishtml = thishtml + pageElements.footer()
		print thishtml
		#print mysessions.SESSION.output()
	else:
		if not(mysessions.SESSION.isset("loggedin")):
			mysessions.SESSION['loggedin'] = False
		if (mysessions.SESSION["loggedin"] == True):
			print mysessions.SESSION.output()
			thisuser = mysessions.SESSION['user']
			thisuser.sort(postdata)

		elif (postdata.has_key("newUser")):
			if not(postdata.has_key("username") and postdata.has_key('password')):
				thishtml = pageElements.useradd()
				thishtml = thishtml+pageElements.footer()
				print thishtml
			else:
				thisuser=users.User(postdata["username"].value, postdata["password"].value)
				thisuser.setPrefs(postdata)
				if thisuser.usernameExists():
					thishtml = pageElements.useradd(message="Username already exists")
					thishtml = thishtml + pageElements.footer()
					print thishtml
				else:
					if not (thisuser.createNew()):
						thishtml = pageElements.loginpage()
						thishtml = thishtml + pageElements.footer()
						print thishtml
					else:
						# mysessions.SESSION["loggedin"] = True
						# print mysessions.SESSION.output()
						# thisuser.indexpage()
						print pageElements.thanksForRegging()
		elif (postdata.has_key("username") and postdata.has_key("password")):
			thisuser=users.User(postdata["username"].value, postdata["password"].value)
			if thisuser.login():
				mysessions.SESSION["loggedin"] = True
				mysessions.SESSION['user'] = thisuser
				print mysessions.SESSION.output()
				thisuser.indexpage()
			else:
				thishtml = pageElements.loginpage()
				thishtml = thishtml + pageElements.footer()
				print thishtml
		else:
			thishtml = pageElements.loginpage()
			thishtml = thishtml + pageElements.footer()
			print thishtml
		#mysessions.print_session(mysessions.SESSION)


def testthis():
	mysessions.start()

	mysessions.SESSION["loggedin"] = True
	print "Content-type: text/html"
	if (postdata.has_key("emailRecent")):
		"""
		Add this function:
		myfunc.emailUpdates()
		"""
		pass
	if not(mysessions.SESSION.isset("loggedin")):
		mysessions.SESSION['loggedin'] = False
	iflogged = mysessions.SESSION["loggedin"]
	if (iflogged == True):
		# print mysessions.SESSION.output()
		# print "hello!"
		pass

	elif (postdata.has_key("newUser")):
		thisuser=users.User(postdata["username"].value, postdata["password"].value)
		if thisuser.usernameExists():
			pageElements.newUser(message="Username already exists")
		else:
			thisuser.createNew()
			mysessions.SESSION["loggedin"] = True
			print mysessions.SESSION.output()
			thisuser.indexpage()
	elif (postdata.has_key("username") and postdata.has_key("password")):
		thisuser=users.User(postdata["username"].value, postdata["password"].value)
		if thisuser.login():
			mysessions.SESSION["loggedin"] = True
			mysessions.SESSION['user'] = thisuser
			print mysessions.SESSION.output()
			thisuser.indexpage()
		else:
			pageElements.loginpage()
	else:
		pageElements.loginpage()
	mysessions.print_session(mysessions.SESSION)



if __name__=="__main__":
#	mysessions.start()
	postdata = cgi.FieldStorage()
#	sessionsWrite()
	#testthis()
	sorting(postdata)
#	print mysessions.SESSION.output()
	#mysessions.print_session(mysessions.SESSION)
#	testthis()







