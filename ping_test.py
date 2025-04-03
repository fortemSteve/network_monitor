#!/usr/bin/env python3

import subprocess
import re
import time
import json
import os

def run_pingtest(server,timeout,nPackets):
    timenow = time.time()

    cmd = ['ping', '-c',str(nPackets), '-W',str(timeout), '-q', server]

    print(' '.join(cmd))

    r = subprocess.run(cmd,capture_output=True)
    """ output should look like:
    PING hostname (x.x.x.x) 56(84) bytes of data.

    --- hostname ping statistics ---
    5 packets transmitted, 5 received, 0% packet loss, time 4006ms
    rtt min/avg/max/mdev = 53.334/53.459/53.534/0.072 ms
    or for an unreachable host:
    PING hostname (x.x.x.x) 56(84) bytes of data.

    --- x.x.x.x ping statistics ---
    5 packets transmitted, 0 received, 100% packet loss, time 4085ms

    """
    stdout = [i for i in r.stdout.decode().split('\n') if len(i)]
    pat1 = '\d+ packets transmitted, \d+ received, (\d+)% packet loss, time (\d+)ms'
    if stdout[-1].startswith('rtt'):
        # reachable host:
        pat2 = 'rtt min/avg/max/mdev = (\S+) ms'
        statsline = stdout[-2]
        timeline = stdout[-1]    
    else:
        # unreachable host:
        statsline = stdout[-1]
        timeline = None
        
    m = re.match(pat1,statsline)
    pct_loss = int(m.group(1))
    total_time_ms = int(m.group(2))
    if timeline:
        m = re.match(pat2,timeline)
        avg_rtt_ms = float(m.group(1).split('/')[1])
    else:
        avg_rtt_ms = 'N/A'
    return timenow,server,pct_loss,total_time_ms,avg_rtt_ms

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--interactive',action='store_true',help='print results to stdout rather than results file')
args = parser.parse_args()

cfg_file = os.environ['HOME'] + '/.pingtest_config'
with open(cfg_file,'r') as fp:
    cfg = json.load(fp)
    
timeout = cfg['timeout']
nPackets = cfg['nPackets']
servers = cfg['servers']
results_file = cfg['results_file']
if not os.path.exists(results_file):
    with open(results_file,'w') as fp:
        fp.write('utc_time_sec,server,pct_loss,cmd_duration_ms,avg_round_trip_time_ms\n')

fp = open(results_file,'a')
for server in servers:    
    timenow,server,pct_loss,total_time_ms,avg_rtt_ms = run_pingtest(server,timeout,nPackets)
    if type(avg_rtt_ms) is str:
        results_line = ('%.2f,%s,%d,%d,%s' % (timenow,server,pct_loss,total_time_ms,avg_rtt_ms))
    else:
        results_line = ('%.2f,%s,%d,%d,%.3f' % (timenow,server,pct_loss,total_time_ms,avg_rtt_ms))
    if args.interactive:
        print(results_line)
    else:
        fp.write(results_line); fp.write('\n')
fp.close()
