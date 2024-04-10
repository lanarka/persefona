#!/bin/bash

MODE="300" # 100 300 rtty 1200 tdd same

RECORD_DURATION=7  # Seconds

IN_AUDIO_DEV="plughw:CARD=Device_1"

OUT_AUDIO_DEV="plughw:CARD=Device" # _1 = second sound card

PTT_DEV="/dev/ttyUSB0"
