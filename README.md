# network_monitor
Simple network monitoring via ping, python, and crontab

# installation
- clone the repo
- write a config file - $HOME/.pingtest_config. see below for an example
- make a crontab entry - see below
- run check_install.py to verify you've set everything up correctly

# example config:
{
    "timeout" : 5,
    "nPackets" : 5,
    "servers" :
    ["somehost","8.8.8.8"],
    "results_file" : "/home/user/.pingtest_results"
}

# example crontab entry:
0,30 * * * * /home/user/network_monitor/ping_test.py

# usage
- run plot_pingtest.py to plot the results of the test over time
