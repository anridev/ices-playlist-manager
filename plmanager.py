#!/usr/bin/python
import sys,os,subprocess,datetime,random

LOGFILE = '/home/anri/logfile.log'
PLAYLIST = '/home/anri/playlist.txt'
DAYDIR='/home/anri/Dropbox/Shumny Miksher/DAY'	
NIGHTDIR='/home/anri/Dropbox/Shumny Miksher/NIGHT'
DAYGOLD='/home/anri/Dropbox/Shumny Miksher/GOLD/DAY'
NIGHTGOLD='/home/anri/Dropbox/Shumny Miksher/GOLD/NIGHT'

today = datetime.datetime.now()
if today.hour is 00:
	current_dir=NIGHTDIR
	gold_dir=NIGHTGOLD
else: 
	current_dir=DAYDIR
	gold_dir=DAYGOLD

playlist = []
goldlist = []

for dirname, dirnames, filenames in os.walk(current_dir):
	for filename in filenames:
		if 'mp3' in filename or 'MP3' in filename:
			filename=os.path.join(dirname,filename)
			playlist.append(filename)


for dirname, dirnames, filenames in os.walk(gold_dir):
        for filename in filenames:
                if 'mp3' in filename or 'MP3' in filename:
                        filename=os.path.join(dirname,filename)
                        goldlist.append(filename)
random.shuffle(playlist)
random.shuffle(goldlist)

shift = 0
for index, item in enumerate(goldlist):
	playlist.insert(index*3+shift,item)
	shift = shift + 1	


f=open(PLAYLIST,'w')
logfile=open(LOGFILE,'a')

for i in playlist:
	f.write(i + '\n')

f.close()

p = os.popen("ps -ef|grep ices |grep -v grep | awk '{print $2}'")
pid = p.readline()[:-1]
if pid:
	os.kill(int(pid),1)
	logfile.write(str(today)+' ' + current_dir + ' ' + "smoothly loaded\n")

else:
	try:
		result = subprocess.Popen('ices',stdout=subprocess.PIPE).communicate()[0]
	except Exception as e:
		logfile.write(str(today) + ' ' + e.strerror + '\n')
		logfile.close()
		sys.exit()
	logfile.write(str(today) + ' ' + current_dir + ' ' + result)
logfile.close()

