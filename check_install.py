#!/usr/bin/env python3

# check the config file:
import os

cfg_file = os.environ['HOME'] + '/.pingtest_config'
assert os.path.exists(cfg_file)

import json
with open(cfg_file,'r') as fp:
    cfg = json.load(fp)

assert 'timeout' in cfg
timeout = cfg['timeout']
assert type(timeout) is int

assert 'nPackets' in cfg
nPackets = cfg['nPackets']
assert type(nPackets) is int

assert 'servers' in cfg
servers = cfg['servers']
assert type(servers) is list
for server in servers:
    assert type(server) is str

assert 'results_file' in cfg    
results_file = cfg['results_file']
assert type(results_file) is str

# check the crontab:
import subprocess
r = subprocess.run(['crontab','-l'],capture_output=True)
lines = [i.strip() for i in r.stdout.decode().split('\n') if len(i)]
lines = [i for i in lines if not i.startswith('#')]
found = 0
exe_path = os.getcwd() + '/ping_test.py'
for i in lines:
    fields = i.split(' ')
    if fields[-1] == exe_path:
        found = 1
        break
assert found
