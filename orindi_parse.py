#!/usr/bin/python3

#REQUIRES
#https://github.com/SpamScope/mail-parser
#https://pypi.org/project/mail-parser/

import sys, getopt, re 
import mailparser
import datetime,time
from time import strftime,localtime
argv = None
import configparser
import os
from os.path import expanduser
from appdirs import *
from pathlib import Path

########################################################################
# Defining configuration locations and such
########################################################################

appname = "orindi"
appauthor = "Steven Saus"
configdir = user_config_dir(appname)
if not os.path.isdir(configdir):
    os.makedirs(user_config_dir(appname))
ini = os.path.join(configdir,'orindi.ini')


########################################################################
# Parsing that email!
########################################################################
def parse_that_email(messagefile):
    print ('Message file is ' + messagefile)

    with open(messagefile,'r') as fp:
         mail = mailparser.parse_from_file_obj(fp)

    print('To: ' + str(mail.to))

    date_time_obj = datetime.datetime.strptime(str(mail.date),"%Y-%m-%d %H:%M:%S")
    print (str(date_time_obj.date()) + '-' + str(date_time_obj.time()))

    ##########################################################################
    # Match the fromstring to the outdirectory
    ##########################################################################
    for x in sections:
        if "feed" in (str.lower(x)):
            keyword=config[x]['keyword']
            FromList = str.lower(config[x]['from'])
            SubjectList = str.lower(config[x]['subject'])
            # Mailparser returns each thing as an odd tuple, so this works
            # best for trying to parse it.
            fromliststr=str(mail.from_).replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace(',', ' ').replace("'", ' ').replace("  ", ' ').replace('\n', '').replace('\r', '').replace('\t', '')
            for y in FromList.split():
                if y in fromliststr:
                    outdir = keyword
                    print(keyword)
                else:
                    if str(mail.subject) in SubjectList.split():
                        outdir = keyword
                        print(keyword)
#TODO:  The subject is a string fragment match, not a word match, gah
#TODO:  The directory is attached to the base outdir.

# Using now/localtime + time sleep to make sure it's all different for filename of outfile. 
    
    time.sleep(2)
    date_published = localtime()  
    thetime=time.strftime("%Y%m%d%H%M%S",localtime())
    print ('Date2: ' + thetime)
    #define postfile name
    #  f = open(postfile, 'a')

    print ('---')
    print('Title: ' + str(mail.subject))
    print('Description: ' + str(mail.subject))
    print('Author: ' + str(mail.from_))
    print('Date: ' + str(mail.date))
    print('Robots: noindex,nofollow')
    print('Template: index')
    print ('---')
    #currently commented out so stdout isn't cluttered
    #if mail.text_html:
    #    print('html: ' + str(mail.text_html))
    #else:
    #    print('text: ' + str(mail.text_plain))
    #f.close
    fp.close

########################################################################
# Read ini section
########################################################################

config = configparser.ConfigParser()
config.read(ini)
sections=config.sections()

########################################################################
# Main function
########################################################################
infile = ''
infile = (sys.argv[1])  # using ini here, oh procmail copy to handle
parse_that_email(infile)