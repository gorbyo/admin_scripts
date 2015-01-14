#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  wsavail.py
#
#  Copyright 2013 Oleh Horbachov <gorbyo@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
"""
The script checks the availability of web services. You must save list 
of urls as string in plaintext file. 

  usage: 
       python3 wsavail.py pattern filename
"""

import sys
import requests
import re
import logging
import logging.handlers
import yaml

# Set variables
config = yaml.load(open('config.yml','r'))
logfile = config["logfile"]
mailhost = config["mailsettings"]["mailhost"]
fromaddr = config["mailsettings"]["fromaddr"]
toaddrs = config["mailsettings"]["toaddrs"]
subject = config["mailsettings"]["subject"]
credentials = config["mailsettings"]["credentials"]
secure = config["mailsettings"]["secure"]

# Init Logger
logger = logging.getLogger('WebSitesAvailability')
logger.setLevel(logging.INFO)

# Set message of log
msg_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Enable write to log-file
to_logfile = logging.FileHandler(logfile)
to_logfile.setLevel(logging.INFO)
to_logfile.setFormatter(msg_format)

# Enable send mail for CRITICAL status
to_mail = logging.handlers.SMTPHandler(mailhost, fromaddr, toaddrs, subject, credentials, secure)
to_mail.setLevel(logging.CRITICAL)
to_mail.setFormatter(msg_format)

# Add Handlers to Logger
logger.addHandler(to_logfile)
logger.addHandler(to_mail)


def check_contents(url):
        """Function return count of records"""
        try:
            req = requests.request('GET', url)
            if req.status_code == 200:
                return len(re.findall(spattern, req.text))
        except requests.exceptions.Timeout:
            return 0
        except requests.exceptions.ConnectionError:
            return 0


def check_sites(urls):
    for url in urls:
        url_to_check = url 
        len_url = check_contents(url_to_check)
        if len_url != 0:
            logger.info(url_to_check + ' => Site is available with ' + str(len_url) + ' entry(ies).')
        else:
            logger.critical(url_to_check + ' => Site is not available.')

if __name__ == '__main__':
    try:
        spattern = sys.argv[1]
        fname = sys.argv[2]
        urls = (l.strip() for l in open(fname).readlines())
        check_sites(urls)
    except IndexError:
        logger.error('Please set parameters!')
        print(__doc__)
