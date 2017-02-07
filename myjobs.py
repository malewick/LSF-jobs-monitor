import re
import subprocess
import datetime
import pickle
import smtplib
from email.mime.text import MIMEText

# sending email message
def send_notif(message):
	msg = MIMEText(message)
	me = "malewick@cern.ch"
	you ="lewickimaciejj@gmail.com"
	you2 ="malewick@cern.ch"
	msg['Subject'] = 'Mail notifs text'
	msg['From'] = me
	msg['To'] = you
	s = smtplib.SMTP('localhost')
	s.sendmail(me, [you2], msg.as_string())
	s.quit()

# command to log
cmd = ['bjobs', '-a']

# command regex syntax
regex = re.compile(r"""^
(?P<jobid>\d*?)\s+
(?P<user>\S*?)\s+
(?P<status>\S*?)\s+
(?P<queue>\S*?)\s+
(?P<from_host>\S*?)\s+
(?P<exec_host>\S*?)\s+
(?P<job_name>\S*?)\s+
(?P<submit_time>.*?)
$""", re.VERBOSE)

readout = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0]

# decalaring the dictionary of following structure: queue -> status -> count
counter={}

# loop over lines in command output
for line in readout.split("\n"):
	match = regex.match(line)
	if match:
		queue = match.group("queue")
		status = match.group("status")
		if queue in counter:
			if status in counter[queue]:
				counter[queue][status] += 1
			else:
				counter[queue][status] = 1
		else:
			counter[queue]={}
			counter[queue][status] = 1

# will write log into file
f = open("/afs/cern.ch/user/m/malewick/private/bmonitor/bjobs.log","a")

# if there is something in couter put an entry into the logfile
if counter:
	f.write(datetime.datetime.now().strftime('%d-%m-%Y %H:%M'))

	for key in counter:
		f.write("\t")
		f.write(key)
		f.write(": ")
		for k, v in counter[key].iteritems():
			f.write(k)
			f.write("=")
			f.write(str(v))
			f.write(" ")
	f.write("\n")

# read stored number of running jobs
f = open('store.pckl', 'rb')
stored = pickle.load(f)
f.close()

# check how many running jobs there is
running=0
for key, val in counter.iteritems() :
	if 'RUN' in val:
		running+=val['RUN']

# if stored number of running jobs wasn't 0 and now running is - send email notification
if running==0 and stored!=0:
	text = "Jobs finished.\n"
	for key, val in counter.iteritems() :
		text += str(key) + " " + str(val) + "\n"
	send_notif(text)

# store number of running jobs for future usage
f = open('store.pckl', 'wb')
pickle.dump(running, f)
f.close()
