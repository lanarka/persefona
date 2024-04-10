#!/bin/bash
source config.sh

cat test.txt | minimodem --tx -A${OUT_AUDIO_DEV} ${MODE}