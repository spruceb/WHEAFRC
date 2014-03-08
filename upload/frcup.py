#!/usr/bin/python
import argparse
import socket
import subprocess
import time
import sys
import ast
import os
from ftplib import FTP

def parser_setup():
    parser = argparse.ArgumentParser(description="Automated uploading of robot code that also restores network settings")
    parser.add_argument("code", default="robot.py", help="the path of the file to be uploaded")
    parser.add_argument("-tn", type=int, nargs="?", default=3881, help="FRC team number")
    parser.add_argument("-ip-end", type=int, nargs="?", default=6, help="Last byte of the IP")
    parser.add_argument("--no-reboot", action="store_true", help="Prevents the cRIO from rebooting after upload")
    parser.add_argument("--ethernet", action="store_const", const="en0", dest="interface")
    return parser

def set_ip(team_number, ip_end):
    ip = "10.%d.%d.%d" % (team_number / 100, team_number % 100, ip_end)
    subprocess.check_call("sudo ipconfig set en1 MANUAL %s 255.255.255.0" % ip, shell=True)

def connect_network(network_name):
    if subprocess.check_output("airport -s %s" % network_name, shell=True) == "No networks found\n":
        restart_dhcp()
        raise RuntimeError("No such network available, try turning on the robot")
    subprocess.check_call("sudo networksetup -setairportnetwork en1 %s" % network_name, shell=True)

def connect_robot(team_number, ip_end):
    set_ip(team_number, ip_end)
    connect_network(team_number)

def restart_dhcp():
    print("Reserting network...")
    subprocess.check_call("sudo ipconfig set en1 DHCP", shell=True)
    subprocess.check_call("networksetup -setairportpower en1 off", shell=True)
    subprocess.check_call("networksetup -setairportpower en1 on", shell=True)
    subprocess.check_call("sudo networksetup -setdnsservers Wi-Fi 8.8.8.8", shell=True)

def imported_modules(code):
    for node in ast.walk(ast.parse(code, mode="exec")):
        if type(node) == ast.Import:
            for n in (alias.name for alias in node.names):
                yield n
        elif type(node) == ast.ImportFrom:
            yield node.module

def ftp_upload(code, team_number):
    robot = FTP("10.%d.%d.2" % (team_number / 100, team_number % 100))
    robot.login()
    robot.cwd("py")
    robot.storlines("STOR " + "robot.py", open(code))
    directory = os.path.dirname(os.path.abspath(code))
    for module in imported_modules(open(code).read()):
        module += ".py"
        try:
            robot.storlines("STOR "+module, open(directory+"/"+module))
        except:
            pass

def reboot_crio(team_number):
    UDP_IN_PORT=6666
    UDP_OUT_PORT=6668
    out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    out.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    out.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    out.bind(('',UDP_OUT_PORT))
    out.sendto("reboot\n", ("10.%d.%d.2" % (team_number / 100, team_number % 100), UDP_OUT_PORT))
    print("Rebooting cRIO...")

if __name__ == "__main__":
    print("Starting...")
    argv = parser_setup().parse_args(sys.argv[1:])
    #connect_robot(argv.tn, argv.ip_end)
    time.sleep(3)
    ftp_upload(argv.code, argv.tn)
    time.sleep(2)
    if not argv.no_reboot: reboot_crio(argv.tn)
    #restart_dhcp()
    #print("Done.")