#!/bin/bash
source config.sh

init() {
	python3 crypt.py > test.txt
	#echo "012345678901234567890123456789 Hello World 0123456789" > test.txt
}

send() {
	# FIXME: Remove sudo
	sudo ./ptt ${PTT_DEV}
}

recv() {
	minimodem --rx -q -A${IN_AUDIO_DEV} ${MODE} > test_in.txt
}

clean() {
	rm test.txt
	rm test_in.txt
}

abort() {
	sleep ${RECORD_DURATION}
	kill -SIGINT $(pidof minimodem)
}

post_process() {
	#cat test_in.txt
	python3 decrypt.py
}

xxx() {
	minimodem --rx -q -A${IN_AUDIO_DEV} ${MODE}
}


#clean
#init
#send & recv & abort
#post_process
xxx