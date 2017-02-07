import re
import subprocess
import datetime

cmd = ['bqueues', '-u malewick']

#QUEUE_NAME      PRIO STATUS          MAX JL/U JL/P JL/H NJOBS  PEND   RUN  SUSP 
#test             99  Open:Active       -    1    -    -     0     0     0     0

regex = re.compile(r"""^
(?P<queue>\S*?)\s+
(?P<priority>\d*?)\s+
(?P<status>\S*?)\s+
(?P<max>-|\d*?)\s+
(?P<jlu>-|\d*?)\s+
(?P<jlp>-|\d*?)\s+
(?P<jlh>-|\d*?)\s+
(?P<njobs>-|\d*?)\s+
(?P<pending>-|\d*?)\s+
(?P<running>-|\d*?)\s+
(?P<suspended>-|\d*?)
$""", re.VERBOSE)

readout = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0]

f = open("/afs/cern.ch/user/m/malewick/private/bmonitor/bqueues.log","a")

# timestamp (test 8nm 1nh 8nh 1nd 8nd 1nw 2nw 2nw4cores) x (njobs pending running)

f.write(datetime.datetime.now().strftime('%d-%m-%Y %H:%M'))
f.write("\t")
for line in readout.split("\n"):
	match = regex.match(line)
	if match:
		#print datetime.datetime.now().strftime('%d-%m-%Y %H:%M'), "\t",
		#print match.group("queue"), "\t",
		#print match.group("njobs"), "\t",
		#print match.group("pending"), "\t",
		#print match.group("running")

		f.write(match.group("njobs"))
		f.write("\t")
		f.write(match.group("pending"))
		f.write("\t")
		f.write(match.group("running"))
		f.write("\t")
f.write("\n")
