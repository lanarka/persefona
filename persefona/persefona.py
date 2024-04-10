"""
Project Persefona

TODO:
	- sender/recipient filters
	- resolve: watchdoch (VOX??)
	
	MODES 100 300 rtty 1200 tdd same

		300/7  0.3 kbit/s	0.03 kB/s
		1200/3 1.2 kbit/s	0.15 kB/s

	'minimodem','--rx','--binary-output','1200','--ascii','-f', fn

	* http://www.whence.com/minimodem/
	* https://en.wikipedia.org/wiki/List_of_interface_bit_rates
	* http://www.whence.com/minimodem/minimodem.1.html#EXAMPLES
	* https://github.com/a53m0t4n/pycidminimodemwrap/blob/master/ReadCIDTone.py
"""

import time
import sys
import serial
import subprocess
from cryptography.fernet import Fernet

__all__ = ['send', 'receive', 'abort_rec']


# Options
#--------------------------------------------------------------------
MODE = '1200' 
RECORD_DURATION = 3

OUT_AUDIO_DEV = 'plughw:CARD=Device'
IN_AUDIO_DEV = 'plughw:CARD=Device_1'
PTT_DEV = '/dev/ttyUSB0'

CALL_SIGN = '12345'
ENCRYPTION_KEY = b'0StHs9vdDCqL4EP1PC2lzs_PhODj4f2Rxx6dkn7QnFA='
#--------------------------------------------------------------------

PREAMBLE = '0123456789'
SEPARATOR = '\n\n'
ALL_RECIPIENTS = '*'

def cmd(command):
	proc = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
	return proc.communicate()

def cmd_pipe(command1, command2):
	p1 = subprocess.Popen(command1, stdout=subprocess.PIPE)
	p2 = subprocess.Popen(command2, stdin=p1.stdout, stdout=subprocess.PIPE)
	p1.stdout.close()
	return p2.communicate()

def send(message, sender=CALL_SIGN, recipient=ALL_RECIPIENTS, encryption_key=ENCRYPTION_KEY):
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
	done += PREAMBLE
	out_audio_dev = '-A%s' % OUT_AUDIO_DEV
	command1 = ['echo', done]
	command2 = ['minimodem', '--tx', out_audio_dev, MODE]
	cmd_pipe(command1, command2)
	ptt.setRTS(False)

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
	array = message.split(SEPARATOR)
	message = array[2]
	message = bytes(message, 'utf-8')
	try:
		fernet = Fernet(encryption_key)
		message = fernet.decrypt(message).decode()
	except ValueError:
		message = message.decode('utf-8')
	return message

# Test
if __name__=='__main__':
	from multiprocessing import Process as p
	test_msg = "Test message"

	def _send():
		send(test_msg)

	def _receive():
		assert receive()==test_msg
	
	p(target=_send).start()
	p(target=_receive).start()
	p(target=abort_rec).start()
