#This Module Designed for Communication
import smtplib


class communication:
		
	def send_email(self,recipient, subject, body):
    		gmail_user = "gini4artin@gmail.com"
    		gmail_pwd = "mynewbot"
    		FROM = gmail_user
    		TO = recipient if type(recipient) is list else [recipient]
    		SUBJECT = subject
    		TEXT = body

    		# Prepare actual message
    		message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    		""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
    		try:
        		server = smtplib.SMTP("smtp.gmail.com", 587)
        		server.ehlo()
        		server.starttls()
        		server.login(gmail_user, gmail_pwd)
        		server.sendmail(FROM, TO, message)
        		server.close()
        		print 'successfully sent the mail'
    		except:
        		print "failed to send mail"


	
