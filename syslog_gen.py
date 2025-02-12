#!/usr/bin/env python3
"""
Syslog Generator

Had a need to generate generic syslog messages to 
test open source logging solutions.
"""

import socket
import argparse
import random
import sys
import time
import logging
from logging.handlers import SysLogHandler

"""
Modify these variables to change the hostname, domainame, and tag
that show up in the log messages. 
"""
hostname = "host"
domain_name = ".example.com"
tag = ["kernel", "python", "ids", "ips"]
syslog_level = ["info", "error", "warning", "critical"]


def raw_udp_sender(message, host, port):
    # Stubbed in or later use
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        message = bytes(message, "UTF-8")
        send = sock.sendto(message, (host, port))
    finally:
        sock.close()


def open_sample_log(sample_log):
    try:
        with open(sample_log, "r") as sample_log_file:
            random_logs = random.choice(list(sample_log_file))
            return random_logs
    except FileNotFoundError:
        print("[+] ERROR: Please specify valid sample filename")
        return sys.exit()


def open_hosts(source_host):
    try:
        with open(source_host, "r") as host_file:
            random_host = random.choice(list(host_file))
            return random_host.strip()
    except FileNotFoundError:
        print("[+] ERROR: Please specify valid host filename")
        return sys.exit()


def syslogs_sender():
    # Initalize SysLogHandler
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    syslog = SysLogHandler(address=(args.host, args.port))
    logger.addHandler(syslog)

    for message in range(1, args.count + 1):
        # Randomize some fields
        time_output = time.strftime("%b %d %H:%M:%S")
        # random_host = random.choice(range(1, 11))
        random_host = open_hosts(args.src_names)
        random_tag = random.choice(tag)
        random_level = random.choice(syslog_level)
        # commented out fqdn, IP or short hostname will only be used
        # fqdn = "{0}{1}{2}".format(hostname, random_host, domain_name)
        random_pid = random.choice(range(500, 9999))

        message = open_sample_log(args.msg)
        fields = {
            # "host_field": fqdn,
            "host_field": random_host,
            "date_field": time_output,
            "tag_field": random_tag,
        }

        format = logging.Formatter(
            "%(date_field)s %(host_field)s {0}[{1}]: %(message)s".format(
                random_tag, random_pid
            )
        )
        syslog.setFormatter(format)

        print(
            "[+] Sent: {0}: {1} {2} ".format(
                time_output, random_host, message
            ),
            end="",
        )

        getattr(logger, random_level)(message, extra=fields)

    logger.removeHandler(syslog)
    syslog.close()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--host", required=True, help="Remote host to send messages"
    )
    parser.add_argument(
        "--port", type=int, required=True, help="Remote port to send messages"
    )
    parser.add_argument("--msg", required=True, help="Read messages from file")
    parser.add_argument(
        "--src_names",
        required=True,
        help="Obtain random hostname or ip for the source host",
    )
    parser.add_argument(
        "--count", type=int, required=True, help="Number of messages to send"
    )
    parser.add_argument(
        "--sleep",
        type=float,
        help="Use with count flag to \
                        send X messages every X seconds, sleep being seconds",
    )

    args = parser.parse_args()

    if args.sleep:
        print(
            "[+] Sending {0} messages every {1} seconds to {2} on port {3}".format(
                args.count, args.sleep, args.host, args.port
            )
        )
        try:
            while True:
                syslogs_sender()
                time.sleep(args.sleep)
        except KeyboardInterrupt:
            # Use ctrl-c to stop the loop
            print("[+] Stopping syslog generator...")
    else:
        print(
            "[+] Sending {0} messages to {1} on port {2}".format(
                args.count, args.host, args.port
            )
        )
        syslogs_sender()
