"""
	Project Persefona
	Simple Radio Messenger
	
	DEPS.: minimodem alsa

	MODES: 100 300 rtty 1200 tdd same

	TODO:
		- watchdog/VOX ?
		- sender/recipient filters

	SUCCESS:	
		- 300/7  0.3 kbit/s	0.03 kB/s
		- 1200/3 1.2 kbit/s	0.15 kB/s

	LINKS:
		- http://www.whence.com/minimodem/
		- https://en.wikipedia.org/wiki/List_of_interface_bit_rates

	--------------------------------------------------------------------------------
	White PC Installation
	--------------------------------------------------------------------------------
	apt update
	apt upgrade
	apt install wget joe mc minimodem python3-serial python3-cryptography
"""

# User configuration
MODE = '1200'
OUT_AUDIO_DEV = 'plughw:CARD=Device_1'
IN_AUDIO_DEV = 'plughw:CARD=Device'
PTT_DEV = '/dev/ttyUSB1'
CALL_SIGN = 'NO-CALLSIGN'
ENCRYPTION_KEY = b'0StHs9vdDCqL4EP1PC2lzs_PhODj4f2Rxx6dkn7QnFA='
# /User configuration

__version__ = '0.0.1'
__all__ = ['send', 'monitor']

import os
import time
import sys
import serial
import subprocess
from multiprocessing import Process
from cryptography.fernet import Fernet

RECORD_DURATION = 3
PREAMBLE = '0123456789'
SEPARATOR = '\n\n'
ALL_RECIPIENTS = '*'
TMP_FILE = 'x.x' #'/tmp/_pf_data.0.tmp'

def cmd(command):
	proc = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
	return proc.communicate()

def cmd_pipe(command1, command2):
	p1 = subprocess.Popen(command1, stdout=subprocess.PIPE)
	p2 = subprocess.Popen(command2, stdin=p1.stdout, stdout=subprocess.PIPE)
	p1.stdout.close()
	return p2.communicate()

def checksum(message):
	return 'asdfghjkl'

def send(message, sender=CALL_SIGN, recipient=ALL_RECIPIENTS, encryption_key=ENCRYPTION_KEY):
	t0=time.time()
	ptt = serial.Serial(PTT_DEV)
	ptt.setRTS(True)
	if encryption_key:
		fernet = Fernet(encryption_key)
		message = fernet.encrypt(message.encode())
		message = message.decode()
	done = ''
	done += PREAMBLE
	done += SEPARATOR
	done += '%s:%s' % (sender, recipient)
	done += SEPARATOR
	done += message
	done += SEPARATOR
	done += checksum(message)
	done += PREAMBLE
	out_audio_dev = '-A%s' % OUT_AUDIO_DEV
	command1 = ['echo', done]
	command2 = ['minimodem', '--tx', out_audio_dev, MODE]
	cmd_pipe(command1, command2)
	ptt.setRTS(False)
	t1=time.time()
	print('took=', t1-t0)

def abort_rec(duration=RECORD_DURATION):
	time.sleep(duration)
	pid = cmd(['pidof', 'minimodem'])
	try:
		pid = pid[0].decode().split(" ")[0].strip()
	except Exception:
		return
	cmd(['kill', '-SIGINT', pid])

def receive(encryption_key=ENCRYPTION_KEY):
	in_audio_dev = '-A%s' % IN_AUDIO_DEV
	command = ['minimodem', '--rx', '-q', in_audio_dev, MODE]
	message = cmd(command)[0]
	message = message.decode('iso-8859-1')
	parts = message.split(SEPARATOR)
	message = parts[2]
	message = bytes(message, 'utf-8')
	try:
		fernet = Fernet(encryption_key)
		message = fernet.decrypt(message).decode()
	except ValueError:
		message = message.decode('utf-8')
	return message

def loop_test():
	data = "Hello123"*4 #32 Chars
	_send = lambda: send(data)
	_receive = lambda: print(receive())
	Process(target=_send).start()
	Process(target=_receive).start()
	Process(target=abort_rec).start()


#####################################################################
"""
def flush():
	fh = open(TMP_FILE, 'wb')
	fh.write(b"")
	fh.close()

class Monitor:

	def __init__(self, watch_file, call_func_on_change=None, *args, **kwargs):
		self._cached_stamp = 0
		self.filename = watch_file
		self.call_func_on_change = call_func_on_change
		self.args = args
		self.kwargs = kwargs

	def look(self):
		stamp = os.stat(self.filename).st_mtime
		if stamp != self._cached_stamp:
			self._cached_stamp = stamp
			#print('File changed')
			if self.call_func_on_change is not None:
				self.call_func_on_change(*self.args, **self.kwargs)

	def loop(self):
		while True: 
			try: 
				time.sleep(0.001) 
				self.look() 
			except KeyboardInterrupt: 
				break 
			except FileNotFoundError:
				pass

def verify(data):
	data = data.decode('iso-8859-1')
	parts = data.split(SEPARATOR)
	try:
		message = parts[2]
	except IndexError:
		return None
	message = bytes(message, 'utf-8')
	try:
		fernet = Fernet(ENCRYPTION_KEY)
		try:
			message = fernet.decrypt(message).decode()
		except:
			return None
		#flush()
	except ValueError:
		message = message.decode('utf-8')
	return message
	
def proc(proc_cb):
	f = open(TMP_FILE, 'rb')
	x = f.read()
	d = verify(x)
	if d:
		proc_cb(d)
	f.close()

def monitor(encryption_key=ENCRYPTION_KEY, callback=None):
	flush()
	mon = Monitor(TMP_FILE, proc, proc_cb=callback)
	mon.loop()

#####################################################################

def monitor_callback(message):
	print('message received: %s' % message)
"""
if __name__=='__main__':
	if len(sys.argv) == 2 or len(sys.argv) == 3:
		if sys.argv[1] == '-m':
			pass
			#monitor(callback=monitor_callback)
		if sys.argv[1] == '-s':
			#send(sys.argv[2])
			data = "Hello123"*4 #32 Chars
			send(data)
	else:
		loop_test()
