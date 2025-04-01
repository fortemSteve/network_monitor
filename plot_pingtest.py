#!/usr/bin/env python3
import matplotlib.pyplot as plt
from csvread import *
import numpy as np
import time
import os
import json

units = 'min'
cfg_file = os.environ['HOME'] + '/.pingtest_config'
with open(cfg_file,'r') as fp:
    cfg = json.load(fp)

x = csvread(cfg['results_file'])
#utc_time_sec,server,pct_loss,cmd_duration_ms,avg_round_trip_time_ms
uservers = list(set(x['server']))
uservers.sort()
fig,ax = plt.subplots()
tref = np.min(x['utc_time_sec'])

if units == 's':
    divisor = 1
elif units == 'min':
    divisor = 60
elif units == 'hr':
    divisor = 3600
elif units == 'day':
    divisor = 86400    

for iserver in range(0,len(uservers)):
    server = uservers[iserver]
    #theselines = [i for i in x if i['server'] == server]
    iTheseLines = [i for i in range(0,len(x['server'])) if x['server'][i] == server]
    #t = np.array([i['utc_time_sec'] for i in theselines])
    #rtt = np.array([i['avg_round_trip_time_ms'] for i in theselines]) # TODO - account for N/A
    t = x['utc_time_sec'][iTheseLines]-tref
    t = t / divisor
    ax.plot(t,x['avg_round_trip_time_ms'][iTheseLines],'--',label=server)

tref_st = time.gmtime(tref)
ttl_str = ('%d/%d/%d %02d:%02d:%02d' % (tref_st.tm_mon,tref_st.tm_mday,tref_st.tm_year,tref_st.tm_hour,tref_st.tm_min,tref_st.tm_sec))
fig.suptitle(f'logs begin at {ttl_str} UTC')
ax.legend()
ax.set_ylabel('round trip latency (ms)')
ax.set_xlabel(f'time ({units}) since tref')
plt.show()
    