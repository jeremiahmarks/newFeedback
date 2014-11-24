#To Do

* Done - when creating new users also set up email preferences
* Done - create overview page
* Partially Done - admin functionality
* rewrite parse functionality
* Done - figure out the stupid cookie issue when you change users
* Done - Set up email verification when creating account
	New user creation process:
		check if email address ends with @infusionsoft.com
			if not:
				display error message
				display new user creation page
			if so:
				check if email address is in use
					if so
						display error message
						display new user creation page
					if not
						create new user record
							hash email address and save in column
							set verified column to 0
						send email with link to domain?verifyaddress=hash
							when user clicks link:
								set verified column to 1
								display welcome message
								display index
* Rework pages so they are more modular - make pagestart and headerinfo loaded in the pf functions so that multiple pages can be streamed together
* Done - set up email notifications for new feedback