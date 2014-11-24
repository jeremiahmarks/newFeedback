#!/usr/local/bin/python2.7


import MySQLdb
import cgi
import re
import datetime
import xmlrpclib
#import random
import cgitb
import myconfig
import Cookie
import os
import time
import errno
import pageElements
#import hashlib

################################################################################
##
## Classes
##
################################################################################


class Line(object):
	def __init__(self, lineNumber, whoSaidIt, whatWasSaid, timeItWasSaid="", timeSinceLastStatement=""):
		self.lineNumber=lineNumber
		self.whoSaidIt=whoSaidIt
		self.whatWasSaid=whatWasSaid
		self.timeItWasSaid=timeItWasSaid
		self.timeSinceLastStatement=timeSinceLastStatement
		self.allComplexFeedback=[]

	def setSimpleFeedBack(self, simpleA, simpleB):
		self.simpleA=simpleA
		self.simpleB=simpleB

	def addComplexFeedback(self, feedback):
		self.allComplexFeedback.append(feedback)

class Chat(object):
	def __init__(self):
		self.Agent=""
		#self.AgentID=
		self.Agentfname=""
		self.Agentlinitial=""
		self.Customer=""
		self.chatID=""
		self.fullLog=""
		self.orderedLines={}
		self.lines=[]

class ISServer:
	myconfig.infusionsoftapp
	myconfig.infusionsoftAPIKey
	myconfig.tagID
	myconfig.fromAddress

	def __init__(self):
		self.appurl = "https://" + myconfig.infusionsoftapp+".infusionsoft.com:443/api/xmlrpc"
		self.connection = xmlrpclib.ServerProxy(self.appurl)

	def sendEmail(self, emailBody, asubject="Please Provide Feedback", contactList=[]):
		"""
		This method will take the body of an email and mail it to all contacts
		who have the tag "ChatSupport" and email addresses that end in @infusionsoft.com
		"""
		if (contactList==[]):
			contactList = [5641,]
		toAddress='~Contact.Email~'
		ccAddress=''
		bccAddress=''
		contentType="HTML"
		subject=asubject
		htmlBody=emailBody
		textBody=''
		self.connection.APIEmailService.sendEmail(myconfig.infusionsoftAPIKey, contactList, myconfig.fromAddress, toAddress, ccAddress, bccAddress, contentType, subject, htmlBody, textBody)


	def getContacts(self):
		desiredResults=[]
		listOfDicts = self.connection.DataService.query(myconfig.infusionsoftAPIKey, "ContactGroupAssign", 1000,0,{'GroupId':395},['ContactId'],"ContactId", True )
		for eachEntry in listOfDicts:
			desiredResults.append(eachEntry['ContactId'])
		return desiredResults

	def addContact(self, fname, email):
		newContact={}
		newContact["FirstName"]=fname
		#newContact["LastName"]=lname
		newContact["Email"]=email

		thiscontact = self.connection.ContactService.addWithDupCheck(myconfig.infusionsoftAPIKey, newContact, 'Email')
		self.connection.ContactService.addToGroup(myconfig.infusionsoftAPIKey, thiscontact, myconfig.tagID)
		self.connection.APIEmailService.optIn(myconfig.infusionsoftAPIKey, email, "This email was opted in to recieve notifications regarding peer feedback")
		return thiscontact


def databaseConnection():
	myconfig.mysqlhostname
	myconfig.mysqlusername
	myconfig.mysqlpassword
	myconfig.mysqldbname
	return MySQLdb.connect(host=myconfig.mysqlhostname, user=myconfig.mysqlusername, passwd=myconfig.mysqlpassword, db=myconfig.mysqldbname )

################################################################################
##
##  Submission Processing
##
################################################################################
	############################################################################
	##The main logic behind the process
	############################################################################
def mainSequence(txt, chatid, userid):
	thischat = parseBlobIntoLines(txt)
	thischat.chatID=chatid
	thischat.AgentID=int(userid)
	db=databaseConnection()

	cursor = db.cursor()

	cmd = "INSERT INTO maintable (chatid, agent, submittedby) VALUES (%s, %s, %s)"
	cursor.execute(cmd, (chatid,thischat.Agent, thischat.AgentID))
	for each in thischat.lines:
		if ((each.whoSaidIt==thischat.Agent) or (each.whoSaidIt==thischat.Agentfname + " " + thischat.Agentlinitial)):
			whosaid="agent"
		else:
			whosaid="customer"

		cmd = """INSERT INTO interactions (chatid, line, whois, linetext, timefromlastline) VALUES (%s, %s, %s, %s, %s)"""
		vals = (chatid, '%05d' %int(each.lineNumber), whosaid, each.whatWasSaid, each.timeSinceLastStatement)

		cursor.execute(cmd, (chatid, '%05d' %int(each.lineNumber), whosaid, each.whatWasSaid, each.timeSinceLastStatement))

		cmd2 = """INSERT INTO simplefeedback (chatid, line, submittedby) VALUES (%s, %s, %s)"""
		cursor.execute(cmd2, (chatid, '%05d' %int(each.lineNumber), userid))
	cursor.close()
	db.close()
		########################################################################
		##	Takes an entire chat interaction and returns a series of Lines
		########################################################################
def parseBlobIntoLines(txt):
	"""
	This method is intended to take a full text blob and parse it into individual lines
	That said, there are three lines that need special treatment and two additional line
	types that will need consideration

	The lines that need special treatment are the zeroth, the first, and the last line.
	The line types that will need special treatment are file upload lines, agent transfer lines,
	and "Absent" lines.
	"""
	#the zeroth line is the line that starts the blob and ends immediatly before the
	#first instance of [HH:MM:SS [AP]M]
	thischat=Chat()
	zerothLine=re.match(r'(.*)(?=\[[0-9])*',txt,re.M|re.I).group(1)
	txt=txt.replace(zerothLine,"")
	#This while loop basically clears out any additional "\n"s that are floating around
	while True:
		if (txt[0]=='\n'):
			txt=txt.replace('\n','',1)
		else:
			break
	##This checks if the first character is a '[', if it is not, it finds the next '[' and truncates
	##the text to that point
	if not (re.match(r'^\[',txt)):
		nextbracket = txt.find('[')
		txt=txt[nextbracket:]
	firstlineTimestamp = re.match(r'.*(\[[0-9][0-9]:[0-9][0-9]:[0-9][0-9] [AP]M\]).*',txt).group(1)

	txt=txt.replace(firstlineTimestamp,'',1) # This removes the first time stamp

	nextTimeStamp=txt.find('\n[') #since we are still dealing with the first line this finds the start of the next line.
	firstline = txt[:nextTimeStamp] #this creates the first line which is the first line.
	txt=txt.replace(firstline, '', 1) #this removes the first line from the rest of the text.

	thischat.lines.append(convertZerothLine(zerothLine,thischat))
	thischat.Agent=thischat.lines[0].whoSaidIt
	thischat.lines.append(convertFirstLine(thischat, txt[:14],firstline))

	while(len(txt)>0):
		(messageTimeStamp, thisMessage, txt) = getNextLine(txt)
		convertNormalLine(messageTimeStamp, thisMessage, thischat)
	return thischat
		########################################################################
		##	This method breaks off the next interaction and returns two peices
		########################################################################
def getNextLine(txt):
	"""
	This method will take a large block of text figure out where the next
	full submission ends, and return the next submission and the block of text
	without the next submission
	"""
	while (txt[0]=='\n'):
		txt=txt.replace('\n','',1)
	nextLinesTimeStamp=re.match(r'.*(\[[0-9][0-9]:[0-9][0-9]:[0-9][0-9] [AP]M\])',txt).group(1)
	txt=txt.replace(nextLinesTimeStamp,'',1)

	nextBracket = txt.find('[')
	if (nextBracket==-1):
		return (nextLinesTimeStamp, txt,'')
	if (re.match(r'(\[[0-9][0-9]:[0-9][0-9]:[0-9][0-9] [AP]M\])',txt[nextBracket:nextBracket+13])):
		return (nextLinesTimeStamp, txt[:nextBracket], txt[nextBracket:])
	while True:
		oldBracket=nextBracket
		nextBracket = txt.find('[',nextBracket)
		if (re.match(r'(\[[0-9][0-9]:[0-9][0-9]:[0-9][0-9] [AP]M\])',txt[nextBracket:nextBracket+13])):
			return (nextLinesTimeStamp, txt[:nextBracket], txt[nextBracket:])
		if (oldBracket==nextBracket):
			return(nextLinesTimeStamp, txt[:nextBracket], "")
		########################################################################
		##	This converts the very first line of text into the table
		########################################################################
def convertZerothLine(zline, thischat):
	chatStartTime=re.match( r'.*([0-9][0-9])/([0-9][0-9])/([0-9][0-9][0-9][0-9]) ([0-9][0-9]):([0-9][0-9]) ([AP]M)(.*) (.*),.*', zline, re.M|re.I)
	startTime={}
	startTime["month"] = int(chatStartTime.group(1))
	startTime["day"] = int(chatStartTime.group(2))
	startTime["year"] = int(chatStartTime.group(3))
	startTime["hour"] = int(chatStartTime.group(4))
	startTime["minute"] = int(chatStartTime.group(5))
	if (chatStartTime.group(6)=="PM"):
		startTime["hour"] = startTime["hour"] + 12
	agentsName=chatStartTime.group(7) + " " + chatStartTime.group(8)
	thischat.Agentfname = chatStartTime.group(7)
	thischat.Agentlinitial = chatStartTime.group(8)[0]

	#zline = zline.replace(agentsName, "Agent")

	startTimeAsObject = datetime.datetime(startTime["year"],startTime["month"],startTime["day"],startTime["hour"],startTime["minute"])
	zerothAsLine=Line(0,agentsName,zline,startTimeAsObject,0)

	return zerothAsLine
		########################################################################
		##	Since the second line that is recorded is also different from the
		##	rest of the chat, this method deals with that line
		########################################################################
def convertFirstLine(thischat, firstlineTimestamp,firstline):
	firstlineTimestamp=firstlineTimestamp.replace('\n','')
	messageSentTime=re.match(r'.*([0-9][0-9]):([0-9][0-9]):([0-9][0-9]) ([AP]M)', firstlineTimestamp)
	messageTime={}
	messageTime["hour"] = int(messageSentTime.group(1))
	messageTime["minute"] = int(messageSentTime.group(2))
	messageTime["second"] = int(messageSentTime.group(3))
	if (messageSentTime.group(4)=="PM"):
		messageTime["hour"] = messageTime["hour"] + 12
	stime = thischat.lines[0].timeItWasSaid
	messageTimeAsObject = datetime.datetime(stime.year, stime.month, stime.day, messageTime["hour"], messageTime["minute"], messageTime["second"])
	timeDifference = messageTimeAsObject - stime
	return Line(1,thischat.Agent,firstline,messageTimeAsObject,timeDifference)
		########################################################################
		##	Most of the rest of the lines are about the same, this method deals
		##	with them
		########################################################################
def convertNormalLine(chattimeStamp, txt, thischat):
	lineNumber = len(thischat.lines)
	messageSentTime=re.match(r'.*([0-9][0-9]):([0-9][0-9]):([0-9][0-9]) ([AP]M)', chattimeStamp)
	messageTime={}
	messageTime["hour"] = int(messageSentTime.group(1))
	messageTime["minute"] = int(messageSentTime.group(2))
	messageTime["second"] = int(messageSentTime.group(3))
	if (messageSentTime.group(4)=="PM" and not (messageTime["hour"]==12)):
		messageTime["hour"] = messageTime["hour"] + 12
	prevTime=thischat.lines[lineNumber-1].timeItWasSaid
	messageTimeAsObject = datetime.datetime(prevTime.year, prevTime.month, prevTime.day, messageTime["hour"], messageTime["minute"], messageTime["second"])
	timeDifference = messageTimeAsObject - prevTime
	txt=txt.strip()
	if(txt.startswith(thischat.Agentfname + " " + thischat.Agentlinitial)):
		whoSaidIt = thischat.Agent
	else:
		whoSaidIt = txt[:txt.find(':')]
	thischat.lines.append(Line(lineNumber,whoSaidIt,txt[txt.find(':'):],messageTimeAsObject,timeDifference))


		########################################################################
		##  This method parses feedback and sends each feedback to the
		## 	appropriate place for it to get updated
		########################################################################
def updateDatabase(arguments, userid):
	chatid = arguments["thischatid"].value
	totalLines = arguments["linesOfChat"].value
	stmt="""UPDATE maintable SET feedbackssubmitted = feedbackssubmitted + 1 where chatid="%s" """ %(chatid)
	stmt2="""INSERT INTO feedbackrecord (userid, chatid) VALUES (%s, %s) """
	stmt3="""SELECT users.updates,users.isidnum,users.id FROM users LEFT JOIN maintable ON users.id=maintable.submittedby WHERE maintable.chatid = "%s" """ %(chatid)
	db=databaseConnection()
	cur=db.cursor()
	cur.execute(stmt)
	cur.execute(stmt2, (userid, chatid))
	cur.execute(stmt3)
	values=cur.fetchall()
	cur.close()
	db.close()
	if (values[0][0]==1):
		sendMessage=True
	else:
		sendMessage=False
	allsimpleFeedback=""
	totalup=0
	totaldown=0

	for x in range(int(totalLines)):

		if arguments.has_key("simple"+str("%05d" %x)):
			val=arguments["simple"+str("%05d" %x)].value
			if (val=="pos"):
				totalup+=1
			elif (val=="neg"):
				totaldown+=1
			allsimpleFeedback = allsimpleFeedback + """%s:%s;""" %(str("%05d" %x),val)

			incrementSimple(chatid, str("%05d" %x), val)
		if arguments.has_key("text"+str("%05d" %x)):
			updateComplex(chatid, str("%05d" %x),arguments["text"+str("%05d" %x)].value, userid)
	#pageElements.cumulativePage(chatid)
		########################################################################
		##	This method increments the simple feedback mechanism
		########################################################################
	updateindivoverview = """INSERT INTO feedbackoverviewindiv (userid, chatid, totalup, totaldown, overview) VALUES (%s, %s, %s, %s, %s ) """ # %(int(userid), chatid, totalup, totaldown, allsimpleFeedback)
	updatefeedbackoverviewtotal1 = """UPDATE feedbackoverviewtotal SET totalsubmitted = totalsubmitted + 1, totalsubup = totalsubup + %s, totalsubdown = totalsubdown + %s WHERE userid = %s """ #%(totalup, totaldown, int(userid))
	updatefeedbackoverviewtotal2 = """UPDATE feedbackoverviewtotal SET totalrecieved = totalrecieved + 1, totalrecup = totalrecup + %s, totalrecdown = totalrecdown + %s WHERE userid = %s """ #%(totalup, totaldown, int(values[0][2]))
	if True:
		#because I wanted it indented, that is why.
		db=databaseConnection()
		cur=db.cursor()
		cur.execute(updateindivoverview,(int(userid), chatid, totalup, totaldown, allsimpleFeedback))
		cur.execute(updatefeedbackoverviewtotal1, (totalup, totaldown, int(userid)))
		cur.execute(updatefeedbackoverviewtotal2, (totalup, totaldown, int(values[0][2])))

	if sendMessage:
		basicEmailUpdate=pageElements.updateEmail(chatid)+"""</body></html>"""
		isserver = ISServer()
		isserver.sendEmail(basicEmailUpdate, asubject="update on chat " + chatid, contactList=[values[0][1],])
def incrementSimple(chatid, linesOfChat, value):
	db=databaseConnection()
	cur = db.cursor()
	if (value=="pos" or value=="important"):
		stmt="""UPDATE simplefeedback SET counta = counta + 1 WHERE chatid="%s" AND line = "%s" """ %(chatid, linesOfChat)

	else:
		stmt = """UPDATE simplefeedback SET countb = countb + 1 WHERE chatid ="%s" AND line = "%s" """ %(chatid, linesOfChat)

	cur.execute(stmt)
	cur.close()
	db.close()
		########################################################################
		##	This method updates the written feedback section
		########################################################################
def updateComplex(chatid, linesOfChat, feedback, userid):
	db=databaseConnection()
	cur = db.cursor()
	stmt="""INSERT INTO complexfeedback (chatid, line, complexfeedback, submittedby) VALUES (%s, %s, %s, %s)"""
	cur.execute(stmt, (chatid, linesOfChat, feedback, userid))
	cur.close()
	db.close()
	############################################################################
	##
	##  This function clears the tables data
	##
	############################################################################
def dropall():
	tables = ["complexfeedback", 'interactions', 'maintable', 'simplefeedback', 'emailed']
	db = databaseConnection()
	cur = db.cursor()

	for eachtable in tables:
		stmt="""TRUNCATE TABLE %s;""" %(eachtable)
		cur.execute(stmt)
	cur.close()
	db.close()
	print "all dropped"
	generateIndexPage()
def updateNotifications(userid, postdata):
	if (postdata.has_key('daily')):
		dailyVal=1
	else:
		dailyVal=0
	if (postdata.has_key('updates')):
		updatesVal=1
	else:
		updatesVal=0
	stmt="""UPDATE users SET daily = %i, updates = %i where id = %i """ %(dailyVal, updatesVal, userid)
	db=databaseConnection()
	cur=db.cursor()
	cur.execute(stmt)
	cur.close()
	db.close()
def alluserupdate(postdata):
	q0 = """SELECT * FROM users"""
	db=databaseConnection()
	cur=db.cursor()
	cur.execute(q0)
	allUserValues = cur.fetchall()
	cur.close()
	db.close()

	for eachUser in allUserValues:
		thisID=eachUser[4]
		if (eachUser[5]==1):
			isAdmin=True
		else:
			isAdmin=False
		if (eachUser[7]==1):
			isVerified=True
		else:
			isVerified=False
		if (postdata.has_key('admin' + str(thisID)) and isAdmin):
			pass #noupdate
		elif (not(postdata.has_key('admin' + str(thisID))) and not(isAdmin)):
			pass #noupdate
		elif ( postdata.has_key('admin' + str(thisID))):
			q1="""UPDATE users SET admin = 1 WHERE id = %s """ %(int(thisID))
			db=databaseConnection()
			cur=db.cursor()
			cur.execute(q1)
			cur.close()
			db.close()
		else:
			q2="""UPDATE user SET admin = 0 WHERE id = %s""" %(int(thisID))
			db=databaseConnection()
			cur=db.cursor()
			cur.execute(q2)
			cur.close()
			db.close()
		if (postdata.has_key('active' + str(thisID)) and isVerified):
			pass #noupdate
		elif (not(postdata.has_key('active' + str(thisID))) and not(isVerified)):
			pass #noupdate
		elif ( postdata.has_key('active' + str(thisID))):
			q3="""UPDATE users SET verified = 1 WHERE id = %s """ %(int(thisID))
			db=databaseConnection()
			cur=db.cursor()
			cur.execute(q3)
			cur.close()
			db.close()
		else:
			q4="""UPDATE user SET verified = 0 WHERE id = %s""" %(int(thisID))
			db=databaseConnection()
			cur=db.cursor()
			cur.execute(q4)
			cur.close()
			db.close()


