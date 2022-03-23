syslog-generator
================

Generates syslog messages from a user defined file and sends them to a remote host. 

### Functionality
This script generates random hostnames, syslog levels, and tags to be used in a message. The variables and data structures can be modified to fit your needs by changing them towards the top of the script. The script also randomly pulls messages from a user defined file to provide variety to log data.  

### Usage
This script is written for Python 3+ and is meant to be run from the command line.

#### Required Arguments

* --host: IP or hostname to send syslog messages.
* --port: UDP port to send syslog messages.  
* --msg: Filename to read syslog messasges from. This file should contain ONLY the text of the message. Syslog format is handled by the script. 
* --src_names: Filename to read random hosts from.  This file may contain IP or hostname, one per line.
* --count: Number of messages to send at one time. 

#### Optional Arguments

* --sleep: Number of seconds to sleep until the next batch of messages is sent. Using this argument continues the script indefinitely or until the CTRL-C combination is invoked.  

#### Example

Send 10 messages at once:
```
python3 syslog_gen.py --host 10.0.1.90 --port 514 --msg random_message.txt --src_names random_hosts.txt --count 10

```

Send 10 messages every 30 seconds:
```
python3 syslog_gen.py --host 10.0.1.90 --port 514 --msg random_message.txt --src_names random_hosts.txt --count 10 --sleep 30

```
