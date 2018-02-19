#!/usr/bin/env python

# monitor.py
# 2016-09-17
# Public Domain

# monitor.py          # monitor all GPIO
# monitor.py 23 24 25 # monitor GPIO 23, 24, and 25

import sys
import time
import pigpio

cont=0
last = [None]*32
cb = []

def cbf(GPIO, level, tick):
   global cont
   if last[GPIO] is not None:
      diff = pigpio.tickDiff(last[GPIO], tick)/1000.0
      localtime = time.localtime(time.time())
      cont += 1
      print("C={} G={} l={} d={:.5f}".format(cont, GPIO, level, diff))
   last[GPIO] = tick

pi = pigpio.pi()

if not pi.connected:
   exit()

if len(sys.argv) == 1:
   G = range(24,25)
else:
   G = []
   for a in sys.argv[24]:
      G.append(int(a))
   
for g in G:
   cb.append(pi.callback(g, pigpio.EITHER_EDGE, cbf))

try:
   while True:
      time.sleep(86400)
except KeyboardInterrupt:
   print("\nPassaram os 86400 segundos de gravacao")
   for c in cb:
      c.cancel()

pi.stop()

