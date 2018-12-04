#!/usr/bin/env python

from scapy.all import *
import logging as log
import requests
import os
import sys
from config import ifttt_key, macs

ifttt_url = 'https://maker.ifttt.com/trigger/{event}/with/key/{key}'

log.basicConfig(level=log.INFO)

def button_pressed(event):
    request_url = ifttt_url.format(event=event, key=ifttt_key)
    log.debug("URL = {url}".format(url=request_url))
    r = requests.get(request_url)
    if r.status_code != requests.codes.ok:
        log.error("Bad response: {resp}".format(resp=r.text))
    else:
        log.info("Event {event} triggered successfully".format(event=event))

def check_arp(pkt):
    if ARP in pkt:
        src = pkt[Ether].src
        log.debug("ARP received from {src}".format(src=src))
        if src in macs:
            log.info("Button pressed")
            log.info("{event} event triggering".format(event=macs[src]))
            button_pressed(macs[src])
        else:
            log.debug("{src} not in macs".format(src=src))

def root(): 
    return os.geteuid() == 0

def main():
    if not root():
        log.error("Must be root to run this script, exiting")
        sys.exit(1)
    else:
        log.debug("You are root")
        log.info('Waiting for ARP packets...')
        sniff( filter="arp", prn = check_arp )

if __name__ == "__main__": main()
