#!/usr/bin/python3

#REQUIRES
#https://github.com/SpamScope/mail-parser
#https://pypi.org/project/mail-parser/

import sys, getopt, re 
import mailparser
import datetime,time
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
if not os.path.isdir(configdir):
    os.makedirs(user_config_dir(appname))
ini = os.path.join(configdir,'orindi.ini')


########################################################################
# Parsing that email!
########################################################################
def parse_that_email():
    #print 'Number of arguments:', len(sys.argv), 'arguments.'
    #print 'Argument List:', str(sys.argv)
    #messagefile = open(tmp,'r')
    messagefile = ''
    messagefile = (sys.argv[1])  # using ini here, oh procmail copy to handle
    print ('Message file is ' + messagefile)


    # If the e-mail headers are in a file, uncomment these two lines:
    with open(messagefile,'r') as fp:
         mail = mailparser.parse_from_file_obj(fp)

    #print (mail.body)

    #  Now the header items can be accessed as a dictionary:
    print('To: ' + str(mail.to))

    date_time_obj = datetime.datetime.strptime(str(mail.date),"%Y-%m-%d %H:%M:%S")
    #thetime=time.strftime("%Y%m%d%H%M%S",mail.date)
    # use this plus something else as filename - oh, NOW. Use now and then 
    # time sleep to make sure it's all different. 
    #time.sleep(2)
    print (str(date_time_obj.date()) + '-' + str(date_time_obj.time()))

    ##########################################################################
    # Match the fromstring to the outdirectory
    ##########################################################################
    for x in sections:
    if "feed" in (str.lower(x)):
        
        keyword=config[x]['keyword']
        FromList = str.lower(config[x]['from'])
        SubjectList = str.lower(config[x]['subject'])
        if str(mail.from_) in FromList.split():
            outdir = keyword
        else:
            if str(mail.subject) in SubjectList.split():
                outdir = keyword

    # You can also access the parts of the addresses:
    #define postfile
    #  f = open(postfile, 'a')
    #does not work
    #thetime=time.strftime("%Y%m%d%H%M%S",mail.date)
    #print ('Date2: ' + thetime)
    #print('Body: ' + mail.body)
    #print('text: ' + str(mail.text_plain))
    #print('html: ' + str(mail.text_html))
    #messagefile.close
    print ('---')
    print('Title: ' + str(mail.subject))
    print('Description: ' + str(mail.subject))
    print('Author: ' + str(mail.from_))
    print('Date: ' + str(mail.date))
    print('Robots: noindex,nofollow')
    print('Template: index')
    print ('---')
    #if mail.text_html:
        #print('html: ' + str(mail.text_html))
    #else:
        #print('text: ' + str(mail.text_plain))
    #f.close

########################################################################
# Read ini section
########################################################################

config = configparser.ConfigParser()
config.read(ini)
sections=config.sections()

########################################################################
# Main function
########################################################################
