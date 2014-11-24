#!/usr/bin/python

import myfunc
import myconfig
import re

def pagestart(pagetitle="InfusionSoft Chat PeerFeedback"):
	startstr="""
		<html>
			<head>
				<title>%s</title>
                                <script type='text/javascript' src='http://code.jquery.com/jquery-git2.js'></script>

				<style>
					body, button, input, select, textarea {
    					background-color: #333;
    					color: #fff;
    					font-family: Arial,Helvetica,sans-serif;
					    font-size: 1.3rem;
					    line-height: 1.5;
					}
					input[type="checkbox"].fback{
						display:none;

					}
					input[type="checkbox"].positive + label {
						display:inline-block;
						cursor:pointer;
						background-image: url("./images/gray_arrow_up.png");
						background-repeat: no repeat;
						background-size: 20px 20px;
						height: 20px;
						width: 20px;
					}
					input[type="checkbox"].positive:checked + label {
						background-image: url("./images/green_arrow_up.png");


					}
					input[type="checkbox"].negative + label {
						display:inline-block;
						cursor:pointer;
						background-image: url("./images/gray_arrow_down.png");
						background-repeat: no repeat;
						background-size: 20px 20px;
						height: 20px;
						width: 20px;
					}
					input[type="checkbox"].negative:checked + label {
						background-image: url("./images/red_arrow_down.png");


					}
					input[type="checkbox"].important + label {
						display:inline-block;
						cursor:pointer;
						background-image: url("./images/gray_important_icon.png");
						background-repeat: no repeat;
						background-size: 20px 20px;
						height: 20px;
						width: 20px;
					}
					input[type="checkbox"].important:checked + label {
						background-image: url("./images/important_icon.png");


					}

					.Green{
						background-color: Green;
					}
					.Yellow{
						background-color: Yellow;
					}
					.Red{
						background-color: Red;
					}
					.timebeteenchats{
						color: #000;
						text-align: center;
					}
					.agent{
						background-color: #444;
					}
					.user{
						background-color: #222;
					}
					.agentButtons{
						width: 100%%;
						text-align: center;
					}
					.userButton{
						text-align: center;
					}
					.complexfeedback{
						width: 100%%;
					}
					.writtenFeedback{
						width: 100%%;
					}
					.agentFeedback{
						width: 100%%;
						height: 100%%;
						text-align: center;
					}
					.userFeedback{
						text-align: center;
					}
					a:link	{
						color: red;
					}
					a:visited {
						color: #6A0000;
					}

					.nav{
						width:200px;
						height:100%%;
						position:absolute;

					}

					.nav input{
						display: block;
						width: 150px;
						font-size:0.7rem;
						
					}
					.maincontent{
						position:absolute;
						left:200px;
					}
					.adminnav{
						font-size:0.7rem;
						position:absolute;
						right:15px;
					}
					.adminnav input{
						font-size:0.7rem;
					}

				</style>
                                <script language="javascript" type="text/javascript">
                                $(window).load(function(){
                                    $("input:checkbox").click(function() {
                                        if ($(this).is(":checked")) {
                                            var group = "input:checkbox[name='" + $(this).attr("name") + "']";
                                            $(group).prop("checked", false);
                                            $(this).prop("checked", true);
                                        } else {
                                            $(this).prop("checked", false);
                                        }
                                    });
                                });


                                </script>
			</head>
			<body> """ %(pagetitle)
	return startstr


def mainnav():
	navstr="""	<div class="nav">
					<form class="addchats" name="addchats" method="post" action="./">
						<input type="submit" name="singlesubmit" value="Submit a single chat">
						<!-- <input type="submit" name="multisubmit" value="Submit multiple chats"> -->
						<input type="submit" name="goindex" value="Return to the Index Page">
						<!-- <input type="submit" name="emailRecent" value="Email Recent Updates"> -->
						<!-- <input type="submit" name="deleteData" value="delete"> -->
						<input type="submit" name="manageEmails" value="Manage Notifications">
						<input type="submit" name="logout" value="Logout">
						<input type="submit" name="mysubmissions" value="My Submissions">
						<input type="submit" name="useroverview" value="Total Overview">


					</form>
				</div>
	"""
	return navstr


def adminNav():
	adminnav= """
		<div class="adminnav">
			<form class="adminNav" name="adminNav" method="POST" action="./">
				<input type="submit" name="ViewAllUsers" value="All Users">
			</form>
		</div>
	"""
	return adminnav

def listAllUsers():    
	getUsers="""SELECT uname, id, admin, verified FROM users"""
	getTotalChatsSubmitted="""SELECT COUNT(*) FROM maintable WHERE submittedby = %s """
	getTotalFeedbackSubmitted="""SELECT COUNT(*) FROM feedbackrecord WHERE userid = %s"""
	getIncrementChatsSubmitted="""SELECT COUNT(*) FROM maintable WHERE submittedby = %s AND uploaded BETWEEN DATE_SUB(NOW(), INTERVAL %s DAY) AND NOW()"""
	getIncrementFeedbackSubmitted="""SELECT COUNT(*) FROM feedbackrecord WHERE userid = %s AND whensubmitted BETWEEN DATE_SUB(NOW(), INTERVAL %s DAY) AND NOW()"""
	db=myfunc.databaseConnection()
	cur = db.cursor()
	cur.execute(getUsers)
	incrementPeriods=[7,30,90]

	rows=cur.fetchall()
	cur.close()
	db.close()

	pagehtml = pagestart() + mainnav()
	pagehtml = pagehtml + """<div class="maincontent">
							<form name="allusers" method="post" action=".">
							<table class="allUserStats">
								<tr>
									<td width="200">User</td>
									<!-- <td>Agent</td> -->
									<td width="200">
										<table>
											<tr>
												<td colspan="4">Chats Submitted</td>
											</tr>
											<tr>
												<td width="49">7</td>
												<td width="49">30</td>
												<td width="49">90</td>
												<td width="49">Total</td>
											</tr>
										</table>
									</td>
									<td width="200">
										<table>
											<tr>
												<td colspan="4">Feedback Submitted</td>
											</tr>
											<tr>
												<td width="49">7</td>
												<td width="49">30</td>
												<td width="49">90</td>
												<td width="49">Total</td>
											</tr>
										</table>
									</td>
									<td width="50">Admin</td>
									<td width="50">Active</td>
								</tr>"""

	for row in rows:
		incrementChats={}
		incrementFB={}
		

		db = myfunc.databaseConnection()
		cur = db.cursor()
		cur.execute(getTotalChatsSubmitted, row[1])
		totalchatsSubmittedData = cur.fetchall()
		totalchatsSubmittedTotal = totalchatsSubmittedData[0][0]

		cur.execute(getTotalFeedbackSubmitted, row[1])
		totalfbSubmittedData = cur.fetchall()
		totalfbSubmittedTotal = totalfbSubmittedData[0][0]

		for timeperiod in incrementPeriods:
			cur.execute(getIncrementChatsSubmitted, (row[1],timeperiod))
			thisinfo = cur.fetchall()
			incrementChats[timeperiod] = thisinfo[0][0]

			cur.execute(getIncrementFeedbackSubmitted, (row[1],timeperiod))
			thatinfo = cur.fetchall()
			incrementFB[timeperiod] = thatinfo[0][0]



		cur.close()
		db.close()

		pagehtml = pagehtml + """	<tr>
										<td class="username">
											<a href="%s">%s</a>
										</td>
										<td>
											<table class="chatsSubmittedOverTime">
												<tr>
								""" %(myconfig.urltothisfile + "?seeAllActionBy="+str(row[1]), row[0])

		#Above: Starts the table main table and the chat details table
		#Below: Adds chat details
		for eachperiod in incrementPeriods:
			pagehtml = pagehtml + """
													<td width="49">%s</td>
				""" %(str(incrementChats[eachperiod]))

		pagehtml = pagehtml + """
													<td><a href="%s">%s</a></td>
												</tr>
											</table>
										</td>
										<td>
											<table class="feedbacksOverTime">
												<tr>
								""" %(myconfig.urltothisfile + "?seeAllSubmissionsBy="+str(row[1]), totalchatsSubmittedTotal)

		for aperiod in incrementPeriods:
			pagehtml = pagehtml + """
													<td width="49">%s</td>
			""" %(str(incrementFB[aperiod]))

		pagehtml = pagehtml + """
													<td><a href="%s">%s</a></td>
												</tr>
											</table>
										</td>
								""" %(myconfig.urltothisfile + "?seeAllFeedbackBy="+str(row[1]), totalfbSubmittedTotal)		
		if (row[2]==1):
			pagehtml = pagehtml + 	"""
										<td>
											<input type="checkbox" name="%s" value="%s" checked>
										</td>
									""" %("admin"+str(row[1]), str(row[1]))
		else:
			pagehtml = pagehtml + 	"""
										<td>
											<input type="checkbox" name="%s" value="%s">
										</td>
									""" %("admin"+str(row[1]), str(row[1]))
		if (row[3]==1):
			pagehtml = pagehtml + 	"""
										<td>
											<input type="checkbox" name="%s" value="%s" checked>
										</td>
									""" %("active"+str(row[1]), str(row[1]))
		else:
			pagehtml = pagehtml + 	"""
										<td>
											<input type="checkbox" name="%s" value="%s">
										</td>
									""" %("active"+str(row[1]), str(row[1]))
		pagehtml=pagehtml+	"""	</tr>"""
	pagehtml = pagehtml + """
		<tr colspan="4">
			<td>
				<input type="submit" name="updateFromAllUsers" value="Update changed Records">
			</td>
		</tr>
		</table>
		</form>
		</div>
	"""
	return pagehtml 



def generateIndexPage():
	"""
	This method is used for generally building and displaying a simple index page
	of all of the chats that have been submitted previously.
	"""
	db=myfunc.databaseConnection()
	cur = db.cursor()

	myquery = "SELECT * FROM maintable"
	cur.execute(myquery)

	rows = cur.fetchall()
	cur.close()
	db.close()
	pagehtml = pagestart() + mainnav()


	pagehtml = pagehtml + """<div class="maincontent">
								<table>
								<tr>
									<td width="200">ChatID</td>
									<!-- <td>Agent</td> -->
									<td width="200">Date Uploaded</td>
									<td width="200">Provide Feedback</td>
									<td width="200">View feedback</td>
									<td width="200">Times Submitted</td>
								</tr>"""

	for row in rows:
		pagehtml = pagehtml + """	<tr>
								<td class="chatid">%s</td>
								<td class="dateUploaded">%s</td>
								<td class="providefeedback"><a href="%s">Provide Feedback</td>
								<td class="viewfeedback"><a href="%s">View Feedback</td>
								<td class="submittedCount">%s</td>
							</tr> """ %(row[0], row[1], myconfig.urltothisfile + "?chat=" + row[0], myconfig.urltothisfile + "?chat=" + row[0] + "&mode=view", row[3])

	pagehtml = pagehtml + """</table></div>"""

	return pagehtml


def signuppage():
	pagehtml=pagestart() + mainnav()
	pagehtml = pagehtml + """<div class="maincontent">
					<form method="POST" action="./">
						<div class="signupForNotifications">
							<label for="Name">Name:</label>
							<input type="text" id="Name" name="Name" />
							<label for="Email">Email: </label>
							<input type="text" id="Email" name="Email">
							<input type="submit" name="signup" value="Signup" />
						</div>
					</form>
					</div>
					"""
	return pagehtml

def useradd(message=""):
	pagehtml=pagestart()+mainnav()

	pagehtml = pagehtml + """
		<h3 style="color:red;">%s</h3>
		""" %(message)

	pagehtml = pagehtml + """<div class="maincontent">
		<form method="POST" action="./">
			<table>
				<tr>
					<td>
						Email Address / Username
					</td>
					<td>
						<input type="text" name="username" />
					</td>
				</tr>
				<tr>
					<td>
						Password:
					</td>
					<td>
						<input type="password" name="password">
					</td>
				</tr>
				<tr>
					<td>
						Get daily updates?
					</td>
					<td>
						<input type="checkbox" name="daily" style="display:inline;" checked>
					</td>
				</tr>
				<tr>
					<td>
						Get an email when someone <br /> leaves feedback on one of your chats?
					</td>
					<td>
						<input type="checkbox" name="updates" style="display:inline;" checked>
				<tr>
					<td colspan="2">
						<input type="submit" name="newUser" value="Create New User" />
					</td>
				</tr>
			</table>
		</form></div>"""

	return pagehtml



def votingPage(chatid):
	"""
	This page is used to collect feedback on a chat record.
	"""
	myconfig.timeGreen
	myconfig.timeYellow

	db=myfunc.databaseConnection()
	cur=db.cursor()
	agentQuery = "SELECT agent FROM maintable WHERE chatid ='%s'" %(chatid)
	cur.execute(agentQuery)
	name=cur.fetchall()
	fullname=name[0][0]
	fname=fullname.split()[0]

	fullNameReplace = re.compile(re.escape(fullname),re.IGNORECASE)
	firstNameReplace = re.compile(re.escape(fname),re.IGNORECASE)



	myquery = "SELECT * FROM interactions WHERE chatid ='%s' ORDER BY line" %(chatid)
	cur.execute(myquery)


	rows = cur.fetchall()
	cur.close()
	db.close()
	totalLines=len(rows)

	htmlString= pagestart() + mainnav()
	htmlString = htmlString + 	"""<div class="maincontent">
									<form class="feedback" name="%s" method="post" action="./">
										<table class="chatRecord" border="1">
											<tr class="heading">
												<td width="10%%">Who</td>
												<td width="30%%">What Was Said</td>
												<td width="10%%">Simple Feedback</td>
												<td width="30%%">Complex Feedback</td>
											</tr>""" %(chatid)
	htmlString = htmlString + """ 	<input type="hidden" name="thischatid" value="%s">
									<input type="hidden" name="linesOfChat" value="%s">""" %(chatid, totalLines)
	for row in rows:
		#thistext = row[3].replace(fullname, "Agent")
		#thistext = thistext.replace(fname, "Agent")
		thistext = firstNameReplace.sub('Agent', fullNameReplace.sub('Agent', row[3]))
		if (row[4]=="0"):
			totalSeconds=0
		else:
			hoursString, minutesString, secondsString = row[4][2:].split(':')
			hours=int(hoursString)
			minutes=int(minutesString)
			seconds=int(secondsString)
			totalSeconds = seconds+minutes*60+hours*3600

		if (totalSeconds<myconfig.timeGreen):
			timeClass="Green"
		elif (totalSeconds<myconfig.timeYellow):
			timeClass="Yellow"
		else:
			timeClass="Red"


		if (row[1] == "%05d" %(1) or row[1]=="%05d" %(0)):
			htmlString=htmlString + """

			<tr class="agent" >
				<td class="WhoIsTalking">%s</td>
				<td class="WhatWasSaid">%s</td>
				<td>
					<table class="agentButtons">
						<tr>
							<td class="posButton">
								<input class="positive fback" type="checkbox" name="%s" value="pos" id="%s" />
								<label for="%s"><!-- <img src="./images/gray_arrow_up.png" height="20px" width="20px" /> --></label>
							</td>
						</tr>
						<tr>
							<td class="negButton">
								<input class="negative fback" type="checkbox" name="%s" value="neg" id="%s" />
								<label for="%s"></label>
							</td>
						</tr>
					</table>
				</td>
				<td>
					<input type="textarea" name="%s" class="complexfeedback" ></textarea>
				</td>
			</tr>""" %(row[2], thistext, "simple"+row[1],"pos"+row[1], "pos"+row[1], "simple"+row[1],"neg"+row[1],"neg"+row[1], "text"+row[1])

		elif (row[2] == "agent"):
			htmlString=htmlString + """
			<tr class="timebeteenchats"><td colspan="4" class="%s">%s</td></tr>
			<tr class="agent" >
				<td class="WhoIsTalking">%s</td>
				<td class="WhatWasSaid">%s</td>
				<td>
					<table class="agentButtons">
						<tr>
							<td class="posButton">
								<input class="positive fback" type="checkbox" name="%s" value="pos" id="%s" />
								<label for="%s"><!-- <img src="./images/gray_arrow_up.png" height="20px" width="20px" /> --></label>
							</td>
						</tr>
						<tr>
							<td class="negButton">
								<input class="negative fback" type="checkbox" name="%s" value="neg" id="%s" />
								<label for="%s"></label>
							</td>
						</tr>
					</table>
				</td>
				<td>
					<input type="textarea" name="%s" class="complexfeedback"></textarea>
				</td>
			</tr>
			   """ %(timeClass, row[4], row[2], thistext, "simple"+row[1],"pos"+row[1], "pos"+row[1], "simple"+row[1],"neg"+row[1],"neg"+row[1], "text"+row[1])
		else:
			htmlString = htmlString+"""
			<tr class="timebeteenchats"><td class="%s" colspan="4">%s</td></tr>
			<tr class="user" >
				<td class="WhoIsTalking">%s</td>
				<td class="WhatWasSaid">%s</td>
				<td class="userButton">
					<input class="important fback" type="checkbox" name="%s" value="important" id="%s">
					<label for="%s"></label>
				</td>
				<td>
					<input type="textarea" name="%s" class="complexfeedback"></textarea>
				</td>
			</tr>
			""" %(timeClass, row[4], row[2], thistext , "simple"+row[1], "important"+row[1], "important"+row[1], "text"+row[1])
	htmlString=htmlString + """
		</table>
		<input type="submit" name="feedbacksubmit" value="submit">
	</form></div>
	"""
	return htmlString

def cumulativePage(chatid):
	"""
	This page is used to display the cumulative results of one particular chat
	record
	"""
	thischat = myfunc.Chat()


	tables = ["complexfeedback", 'interactions', 'maintable', 'simplefeedback']

	pageinformation={}

	for eachtable in tables:
		db=myfunc.databaseConnection()
		cur=db.cursor()
		if (eachtable=="maintable"):
			thisquery = """SELECT * FROM %s WHERE chatid="%s" """ %(eachtable, chatid)
		else:
			thisquery = """SELECT * FROM %s WHERE chatid = "%s" ORDER BY line""" %(eachtable, chatid)
		cur.execute(thisquery)
		pageinformation[eachtable] = cur.fetchall()
		cur.close()
		db.close()

	fullname = pageinformation["maintable"][0][2]
	fname = fullname.split()[0]

	fullNameReplace = re.compile(re.escape(fullname),re.IGNORECASE)
	firstNameReplace = re.compile(re.escape(fname),re.IGNORECASE)

	htmlString = pagestart() + mainnav()

	#######
	## setting up the top of the page
	#######
	# headString = "<div><span>Agent: %s</span><span>ChatID: %s</span></div>" %(pageinformation['maintable'][0][2] , chatid)
	headString = """<div class="maincontent"> <div><span>ChatID : %s</span></div>""" %(chatid)
	##########
	## Setting Up The Data  (it is capitalized because it is important (>.<)  )
	##########

	for eachline in pageinformation['interactions']:
		thistext = firstNameReplace.sub('Agent', fullNameReplace.sub('Agent', eachline[3]))
		thischat.orderedLines[eachline[1]] = myfunc.Line(eachline[1], eachline[2], thistext)
	for eachline in pageinformation['simplefeedback']:
		thischat.orderedLines[eachline[1]].setSimpleFeedBack(eachline[2], eachline[3])
	for eachline in pageinformation['complexfeedback']:
		thischat.orderedLines[eachline[1]].addComplexFeedback(eachline[2])

	##########
	## Creating the table
	##########

	tablestring="""<table class="chatfeedback" border="1">
					<tr class="feedbackHeader">
						<td width="10%">Who</td>
						<td width="30%">What</td>
						<td width="10%">Simple</td>
						<td width="30%">In-Depth</td>
					</tr>
					"""
	for eachline in range(len(thischat.orderedLines.keys())):

		el='%05d' %int(eachline)
		if (thischat.orderedLines[el].whoSaidIt == "agent"):
			thisrow="""
			<tr class="agent" >
				<td class="WhoIsTalking">%s</td>
				<td class="WhatWasSaid">%s</td>
				<td>
					<table class="agentFeedback" border="1">
						<tr>
							<td class="posFeedback" >
								%s people think this was said well
							</td>
						</tr>
						<tr>
							<td class="negFeedback">
								%s people think this could be refined
							</td>
						</tr>
					</table>
				</td>
				<td>
					<table class="writtenFeedback" border="1">""" %(thischat.orderedLines[el].whoSaidIt, thischat.orderedLines[el].whatWasSaid, str(thischat.orderedLines[el].simpleA), str(thischat.orderedLines[el].simpleB))
			for eachFeedback in thischat.orderedLines[el].allComplexFeedback:
				thisrow = thisrow + """<tr class="writtenFeedback"><td class="writtenFeedback">%s</td></tr>""" %(eachFeedback, )
			thisrow=thisrow + """
					</table>
				</td>
			</tr>"""
		else:
			thisrow="""
			<tr class="user" >
				<td class="WhoIsTalking">%s</td>
				<td class="WhatWasSaid">%s</td>
				<td class="userFeedback">
					%s people think that the customer made an important point here
				</td>
				<td>
					<table class="writtenFeedback" border ="1">""" %(thischat.orderedLines[el].whoSaidIt, thischat.orderedLines[el].whatWasSaid, str(thischat.orderedLines[el].simpleA))
			for eachFeedback in thischat.orderedLines[el].allComplexFeedback:
				thisrow = thisrow + """<tr class="writtenFeedback"><td class="writtenFeedback">%s</td></tr>""" %(eachFeedback, )
			thisrow=thisrow + """
					</table>
				</td>
			</tr>"""
		tablestring = tablestring + thisrow
	tablestring = tablestring + "</table>"

	htmlString = htmlString + headString + tablestring + "</div>"
	return htmlString

def individualAdd():
	htmlString=pagestart() + mainnav()
	htmlString=htmlString + """<div class="maincontent">
	<form name="singlesubmit" class="chatsubmission" method="post" action="./">
		<table>
			<tr>
				<td>
					<textarea name="chatlog" cols="90" rows="50"></textarea>
				</td>
				<td>
					<label for="chatid">Chat ID</label>
					<input type="text" id="chatid" name="chatid"><br />
					<input type="submit" name="singleChatSubmitted" value="Submit Chat">
				</td>
			</tr>
		</table>
	</form>
	</div>
	"""
	return htmlString

def loginpage():

	htmlString=pagestart()
	htmlString = htmlString + """<div class="maincontent">
		<form method="POST">
			<input name="username" type="text">
			<input name="password" type="password">
			<input name="login" type="submit" value="login">
			<input name="newUser" type="submit" value="create New User">
			<!-- <input name="passwordReset" type="submit" value="ResetPassword"> -->
		</form>
		</div>
		"""
	return htmlString

def notificationsManagement(userid, admin=False):
	db=myfunc.databaseConnection()
	cur = db.cursor()

	"""
		This page allows a user to manage if they recieve daily emails about new
		submissions as well as updates on feedback that others have provided.
	"""
	query = """SELECT daily,updates FROM users WHERE id = %i """ %(userid)
	cur.execute(query)
	rows = cur.fetchall()
	cur.close()
	db.close()
	if (rows[0][0] == 0):
		daily = ""
	else:
		daily = "checked"
	if (rows[0][1] == 0):
		updates = ""
	else:
		updates="checked"


	htmlString = pagestart() + mainnav()
	htmlString = htmlString + """<div class="maincontent">
	<form class="addchats" name="notifications" method="post" action="./">
		<table>
			<tr>
				<td>
					Get Daily Updates
				</td>
				<td>
					<input type="checkbox" name="daily" value="daily" style="display:inline;" %s>
				</td>
			</tr>
			<tr>
				<td>
					Get updates when feedback is left on your submissions?
				</td>
				<td>
					<input type="checkbox" name="updates" value="updates" style="display:inline;" %s>
				</td>
			</tr>
			<tr>
				<td colspan="2">
					<input type="submit" name="updatenotifications" value="Update">
				</td>
			</tr>
		</table>
	</form></div>
	""" %(daily, updates)
	return htmlString

def seeMySubmissions(userid):
	db=myfunc.databaseConnection()
	cur = db.cursor()

	query = """SELECT chatid, uploaded, feedbackssubmitted FROM maintable WHERE submittedby = %i """ %(int(userid))
	cur.execute(query)
	rows = cur.fetchall()
	cur.close()
	db.close()

	pagehtml = pagestart() + mainnav()


	pagehtml = pagehtml + """<div class="maincontent">
							<table>
								<tr>
									<td width="200">ChatID</td>
									<!-- <td>Agent</td> -->
									<td width="200">Date Uploaded</td>
									<!-- <td width="200">Provide Feedback</td> -->
									<td width="200">View feedback</td>
									<td width="200">Times Submitted</td>
								</tr>"""

	for row in rows:
		pagehtml = pagehtml + """	<tr>
								<td class="chatid">%s</td>
								<td class="dateUploaded">%s</td>
								<!-- <td class="providefeedback"><a href="%s">Provide Feedback</td> -->
								<td class="viewfeedback"><a href="%s">View Feedback</td>
								<td class="submittedCount">%s</td>
							</tr> """ %(row[0], row[1], myconfig.urltothisfile + "?chat=" + row[0], myconfig.urltothisfile + "?chat=" + row[0] + "&mode=view", row[2])

	pagehtml = pagehtml + """</table></div>"""

	return pagehtml

def seeFeedbackSubmissions(userid):  ##Finish Me
	db=myfunc.databaseConnection()
	cur = db.cursor()

	query="""SELECT DISTINCT(chatid) as chatid FROM feedbackrecord WHERE userid = %s""" %(userid)

	cur.execute(query)

	chatids = cur.fetchall()

	anotherquery = """SELECT uname FROM users WHERE id = %s """ %(int(userid))
	cur.execute(anotherquery)
	name = cur.fetchall()[0][0]

	cur.close()
	db.close()

	pagehtml = pagestart() + mainnav() + """
	<div class="maincontent">
		<span> Feedback left by : %s </span></br></br></br>
									<table>
										<tr>
											<td width="100"> chatid </td>
											<td width="200"> When Submitted </td>
											<td width="100"> Pos </td>
											<td width="100"> Neg </td>
										</tr>
	""" %(name)

	for eachid in chatids:
		q1 = """SELECT users.uname,users.id FROM users LEFT JOIN maintable ON users.id = maintable.submittedby WHERE maintable.chatid = "%s" """ %(eachid[0])
		q2 = """SELECT complexfeedback, line FROM complexfeedback WHERE chatid = "%s" """ %(eachid[0])
		q3 = """SELECT totalup, totaldown, submitted FROM feedbackoverviewindiv WHERE chatid = "%s" AND userid = %s """ %(eachid[0], int(userid))
		db=myfunc.databaseConnection()
		cur=db.cursor()
		cur.execute(q1)
		info1=cur.fetchall()
		try:
			submittersName=info1[0][0]
		except:
			submittersName="Unknown" 
		try:
			submittersid=info1[0][1]
		except:
			submittersid="Unknown"
		cur.execute(q2)
		allfbdata = cur.fetchall()
		cur.execute(q3)
		realdata=cur.fetchall()
		cur.close()
		db.close()
		for eachrecord in range(len(realdata)):
			pagehtml = pagehtml + """
				<tr>
					<td class="chatidwhichlinkstochatfeedback"><a href="%s">%s</a></td>
					<td cladd="whenthischatwassubmitted">%s</td>
					<td class="positivevotesleft">%s</td>
					<td class="negativenotesleft">%s</td>
				</tr>
			""" %(myconfig.urltothisfile + "?chat=" + eachid[0] + "&mode=viewonesub&feedbackfrom=" +str(submittersid), eachid[0], realdata[eachrecord][2],realdata[eachrecord][0],realdata[eachrecord][1] )

		# pagehtml = pagehtml + """	<table>
		# 								<tr>
		# 									<td colspan="2">
		# 										<table><tr><td>Chat Id:</td><td><a href="%s">%s</a></td></tr></table>
		# 									</td>
		# 									<td colspan="2">
		# 										<table><tr><td>Submitted by:</td><td><a href="%s">%s</a></td></table>
		# 									</td>
		# 								</tr>""" %(myconfig.urltothisfile + "?chat=" + eachid[0] + "&mode=view", eachid[0], myconfig.urltothisfile + "?seeAllActionBy="+str(submittersid),submittersName)
		# pagehtml = pagehtml + """
		# 								<tr>
		# 									<td> chatid </td>
		# 									<td> When Submitted </td>
		# 									<td> Pos </td>
		# 									<td> Neg </td>
		# 								</tr>
		# """

		# for eachfbleft in allfbdata:
		# 	db=myfunc.databaseConnection()
		# 	cur=db.cursor()
		# 	q3 = """SELECT linetext from interactions WHERE chatid = "%s" AND line = "%s" """ %(eachid[0], eachfbleft[1])
		# 	cur.execute(q3)
		# 	atext = cur.fetchall()
		# 	atext = atext[0][0]

		# 	cur.close()
		# 	db.close()
		# 	pagehtml = pagehtml + """	<tr>
		# 									<td><a href="%s">%s</a></td>
		# 									<td><span title="%s">%s</span></td>
		# 									<td>%s</td>
		# 								</tr>
		# 	""" %(myconfig.urltothisfile + "?chat=" + eachid[0] + "&mode=view", eachid[0], atext, eachfbleft[1], eachfbleft[0])
	pagehtml = pagehtml + """</table><br />"""

	return pagehtml+"""</div>"""




def overviewPage(userid, timeframe=0):
	"""
		This will provide an overview of the submissions from one particular user.
	"""
	stmt0 = """SELECT chatid, uploaded, feedbackssubmitted FROM maintable WHERE submittedby = %i """ %(int(userid))
	db = myfunc.databaseConnection()
	cur = db.cursor()
	cur.execute(stmt0)
	rows = cur.fetchall()


	htmlString = pagestart() + mainnav()
	htmlString = htmlString + """<div class="maincontent">
							<h3> Chats Submitted </h3>
							<table>
								<tr>
									<td width="200">ChatID</td>
									<!-- <td>Agent</td> -->
									<td width="200">Date Uploaded</td>
									<!-- <td width="200">Provide Feedback</td> -->
									<td width="200">View feedback</td>
									<td width="200">Times Submitted</td>
								</tr>"""

	for row in rows:
		htmlString = htmlString + """	<tr>
								<td class="chatid">%s</td>
								<td class="dateUploaded">%s</td>
								<!-- <td class="providefeedback"><a href="%s">Provide Feedback</td> -->
								<td class="viewfeedback"><a href="%s">View Feedback</td>
								<td class="submittedCount">%s</td>
							</tr> """ %(row[0], row[1], myconfig.urltothisfile + "?chat=" + row[0], myconfig.urltothisfile + "?chat=" + row[0] + "&mode=view", row[2])

	htmlString = htmlString + """</table>

	<h3> Feedback Provided </h3>
	<table>
		<tr>
			<td>
				Chat ID
			</td>
			<td>
				Submitted
			</td>
		</tr>
			"""

	stmt1 = """SELECT chatid, whensubmitted FROM feedbackrecord WHERE userid = %i """ %(int(userid))
	cur.execute(stmt1)
	theseRows = cur.fetchall()

	for eachrow in theseRows:
		thislink = myconfig.urltothisfile + """?feedbackfrom=%s&chatid=%s""" %(int(userid), eachrow[0])
		htmlString=htmlString+"""
			<tr>
				<td>
					<a href="%s">%s</a>
				</td>
				<td>
					%s
				</td>
			</tr>
			""" %(thislink, eachrow[0], eachrow[1])
	htmlString = htmlString + """
		</table></div>

	"""
	return htmlString


def oneUserFeedback(chatid, userid):
	"""
		This method is intended to display the feedback that one user has provided
	"""
	thischat = myfunc.Chat()


	tables = ["complexfeedback", 'interactions', 'maintable', 'simplefeedback']

	pageinformation={}

	for eachtable in tables:
		db=myfunc.databaseConnection()
		cur=db.cursor()
		if (eachtable=="maintable"):
			thisquery = """SELECT * FROM %s WHERE chatid="%s" """ %(eachtable, chatid)
		elif (eachtable=='complexfeedback'):
			thisquery = """SELECT * FROM %s WHERE chatid="%s" and submittedby = %s ORDER BY line""" %(eachtable, chatid, userid)
		else:
			thisquery = """SELECT * FROM %s WHERE chatid = "%s" ORDER BY line""" %(eachtable, chatid)
		cur.execute(thisquery)
		pageinformation[eachtable] = cur.fetchall()
		cur.close()
		db.close()

	fullname = pageinformation["maintable"][0][2]
	fname = fullname.split()[0]

	fullNameReplace = re.compile(re.escape(fullname),re.IGNORECASE)
	firstNameReplace = re.compile(re.escape(fname),re.IGNORECASE)

	htmlString = pagestart() + mainnav() + """<div class="maincontent">"""

	#######
	## setting up the top of the page
	#######
	# headString = "<div><span>Agent: %s</span><span>ChatID: %s</span></div>" %(pageinformation['maintable'][0][2] , chatid)
	headString = "<div><span>ChatID : %s</span></div>" %(chatid)
	##########
	## Setting Up The Data  (it is capitalized because it is important (>.<)  )
	##########

	for eachline in pageinformation['interactions']:
		thistext = firstNameReplace.sub('Agent', fullNameReplace.sub('Agent', eachline[3]))
		thischat.orderedLines[eachline[1]] = myfunc.Line(eachline[1], eachline[2], thistext)
	for eachline in pageinformation['simplefeedback']:
		thischat.orderedLines[eachline[1]].setSimpleFeedBack(eachline[2], eachline[3])
	for eachline in pageinformation['complexfeedback']:
		thischat.orderedLines[eachline[1]].addComplexFeedback(eachline[2])

	##########
	## Creating the table
	##########

	tablestring="""<table class="chatfeedback" border="1">
					<tr class="feedbackHeader">
						<td width="10%">Who</td>
						<td width="30%">What</td>
						<!-- <td width="10%">Simple</td> -->
						<td width="30%">In-Depth</td>
					</tr>
					"""
	for eachline in range(len(thischat.orderedLines.keys())):

		el='%05d' %int(eachline)
		if (thischat.orderedLines[el].whoSaidIt == "agent"):
			thisrow="""
			<tr class="agent" >
				<td class="WhoIsTalking">%s</td>
				<td class="WhatWasSaid">%s</td>
				<!-- <td>
					<table class="agentFeedback" border="1">
						<tr>
							<td class="posFeedback" >
								%s people think this was said well
							</td>
						</tr>
						<tr>
							<td class="negFeedback">
								%s people think this could be refined
							</td>
						</tr>
					</table>
				</td> -->
				<td>
					<table class="writtenFeedback" border="1">""" %(thischat.orderedLines[el].whoSaidIt, thischat.orderedLines[el].whatWasSaid, str(thischat.orderedLines[el].simpleA), str(thischat.orderedLines[el].simpleB))
			for eachFeedback in thischat.orderedLines[el].allComplexFeedback:
				thisrow = thisrow + """<tr class="writtenFeedback"><td class="writtenFeedback">%s</td></tr>""" %(eachFeedback, )
			thisrow=thisrow + """
					</table>
				</td>
			</tr>"""
		else:
			thisrow="""
			<tr class="user" >
				<td class="WhoIsTalking">%s</td>
				<td class="WhatWasSaid">%s</td>
				<!-- <td class="userFeedback">
					%s people think that the customer made an important point here
				</td> -->
				<td>
					<table class="writtenFeedback" border ="1">""" %(thischat.orderedLines[el].whoSaidIt, thischat.orderedLines[el].whatWasSaid, str(thischat.orderedLines[el].simpleA))
			for eachFeedback in thischat.orderedLines[el].allComplexFeedback:
				thisrow = thisrow + """<tr class="writtenFeedback"><td class="writtenFeedback">%s</td></tr>""" %(eachFeedback, )
			thisrow=thisrow + """
					</table>
				</td>
			</tr>"""
		tablestring = tablestring + thisrow
	tablestring = tablestring + "</table>"

	htmlString = htmlString + headString + tablestring + "</div>"
	return htmlString

def footer():

	return """</body></html>"""

def verificationemail(thathash):
	pagehtml = pagestart()

	pagehtml = pagehtml + 	""" 	<p>Hello and thank you for signing up for the peer feedback website.  In order to complete registration, please click on 
								<a href="%s">this link</a>.  </p>
								<p> You're an awesome blossom! </p>
								<p> Thank you, have an awesome day!</p>
								<br />
								<br />
								<p> (If you are having issues with this, please let me know.)
									<ul>
										<li>
											<a href="mailto:JeremiahMarks@Infusionsoft.com">E-mail</a>
										</li>
										<li>
											Trillian : jlmarks
										</li>
									</ul>
								</p>
							</body>
						</html>

							""" %(myconfig.urltothisfile + "?verification=" + thathash)
	return pagehtml

def thanksForRegging():
	pagehtml = pagestart()
	pagehtml = pagehtml + """	<div class="maincontent"> <h1>Thank you!</h1>
								<p>Thank you for registering, please check your email to complete registration</p> </div>"""
	return pagehtml

def successfulVerification(userValues):
	pagehtml = pagestart()
	pagehtml = pagehtml + 	"""	<div class="maincontent">
								<h1>
									Verification Complete!
								</h1>
								<p>
									Thank you for successfully verifying the email address %s.  You may now 
									<a href="%s">log in</a>.
								</p></div>
							""" %(userValues[0], myconfig.urltothisfile)
	return pagehtml

def updateEmail(chatid):
	pagehtml= pagestart()
	pagehtml = pagehtml + 	"""
							<p>
								Hey There!  Someone provided feedback on your chat!  Check out what they had to say <a href="%s">here</a>.
							</p>
							<p>
								Have an amazing day!
							</p>
							""" %(myconfig.urltothisfile + "?chat=" + chatid + "&mode=view")
	return pagehtml
