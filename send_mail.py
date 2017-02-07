import smtplib
from email.mime.text import MIMEText

msg = MIMEText("Mail notification test 1.")

me = "malewick@cern.ch"
you ="lewickimaciejj@gmail.com" 
you2 ="malewick@cern.ch" 

msg['Subject'] = 'Mail notifs text'
msg['From'] = me
msg['To'] = you

s = smtplib.SMTP('localhost')
s.sendmail(me, [you2], msg.as_string())
s.quit()

