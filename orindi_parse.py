#!/usr/bin/python3

import shortuuid
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
            
            fromliststr = str(mail.from_).replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace(',', ' ').replace("'", ' ').replace("  ", ' ').replace('\n', '').replace('\r', '').replace('\t', '')
            fromliststr = str.lower(fromliststr)
            outdir = ''
            if FromList:
                print("a")
                for y in FromList.split():
                    print(y)
                    if y in fromliststr:
                        outdir = keyword
                        print(keyword)
            if not outdir:
                if SubjectList:
                    for y in SubjectList.split(','):
                        print(y)
                        if y in str.lower(mail.subject):
                            outdir = keyword
                            print(keyword)
            if outdir:
                
                FullOutDir = BaseOutDir + '/' + outdir
                if not os.path.isdir(FullOutDir):
                    os.makedirs(FullOutDir)
                filename=shortuuid.uuid()
                postfile = BaseOutDir + '/' + outdir + '/' + filename
                f = open(postfile, 'w')

                f.write ('---' + "\n")
                f.write('Title: ' + str(mail.subject) + "\n")
                f.write('Description: ' + str(mail.subject) + "\n")
                f.write('Author: ' + str(mail.from_) + "\n")
                f.write('Date: ' + str(mail.date) + "\n")
                f.write('Robots: noindex,nofollow' + "\n")
                f.write('Template: index' + "\n")
                f.write ('---' + "\n")
                #currently commented out so stdout isn't cluttered
                # This is currently returning html: [' like i had the problem with teh subject ugh
                if mail.text_html:
                    f.write('html: ' + str(mail.text_html) + "\n")
                else:
                    f.write('text: ' + str(mail.text_plain) + "\n")
                f.close
        
    fp.close


                
#TODO:  The subject is a string fragment match, not a word match, gah
    

########################################################################
# Read ini section
########################################################################

config = configparser.ConfigParser()
config.read(ini)
sections=config.sections()

########################################################################
# Main function
########################################################################
BaseOutDir=config['DEFAULT']['BaseDir']
infile = ''
infile = (sys.argv[1])  # using ini here, oh procmail copy to handle
parse_that_email(infile)
