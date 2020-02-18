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
import pypandoc
from html import unescape
########################################################################
# Defining configuration locations and such
########################################################################

appname = "orindi"
appauthor = "Steven Saus"
configdir = user_config_dir(appname)
if not os.path.isdir(configdir):
    os.makedirs(user_config_dir(appname))

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
            # need to loop over these and append them to a matching string, 
            keyword=config[x]['keyword']
            FromList = str.lower(config[x]['from'])
            SubjectList = str.lower(config[x]['subject'])
            # Mailparser returns each thing as an odd tuple, so this works
            # best for trying to parse it.
            
            fromliststr = str(mail.from_).replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace(',', ' ').replace("'", ' ').replace("  ", ' ').replace('\n', '').replace('\r', '').replace('\t', '')
            
            # Getting output from addresses here before I transform the string
            FromString = ''
            for y in fromliststr.split('  '):
                if y:
                    if not FromString:
                        FromString = y.strip()

            fromliststr = str.lower(fromliststr)
            outdir = ''
            if FromList:
                for y in FromList.split():
                    if y in fromliststr:
                        outdir = keyword
                        print(keyword)
            if not outdir:
                if SubjectList:
                    for y in SubjectList.split(','):
                        if y in str.lower(mail.subject):
                            outdir = keyword
                            print(keyword)
            if outdir:
                
                FullOutDir = BaseOutDir + '/' + outdir
                if not os.path.isdir(FullOutDir):
                    os.makedirs(FullOutDir)
                filename=shortuuid.uuid() + '.md'
                postfile = BaseOutDir + '/' + outdir + '/' + filename
                f = open(postfile, 'w')

                f.write ('---' + "\n")
                f.write('Title: ' + str(mail.subject) + "\n")
                f.write('Description: ' + str(mail.subject) + "\n")
                f.write('Author: ' + FromString + "\n")
                f.write('Date: ' + str(mail.date) + "\n")
                f.write('Robots: noindex,nofollow' + "\n")
                f.write('Template: index' + "\n")
                f.write ('---' + "\n")
                if mail.text_html:
                    bodyhtml = str(mail.text_html).replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace(',', ' ').replace("'", ' ').replace("  ", ' ').replace('\n', '').replace('\r', '').replace('\t', '')
                    bodyhtml = bodyhtml.replace("\\n", "<br />").replace("\\t", "")
                    bodyhtml = unescape(bodyhtml)
                    writestring = pypandoc.convert_text(bodyhtml, 'markdown_github', format='html')
                    f.write(writestring + "\n")
                else:
                    if mail.text_plain:
                        bodytxt = str(mail.text_plain).replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace(',', ' ').replace("'", ' ').replace("  ", ' ').replace('\n', '').replace('\r', '').replace('\t', '')
                        bodytxt = bodytxt.replace("\\n", "<br />").replace("\\t", "")
                        f.write(bodytxt + "\n")
                    else: 
                        bodyhtml = str(mail.text_not_managed).replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace(',', ' ').replace("'", ' ').replace("  ", ' ').replace('\n', '').replace('\r', '').replace('\t', '')
                        bodyhtml = bodyhtml.replace("\\n", "").replace("\\t", "")
                        bodyhtml = unescape(bodyhtml)
                        writestring = pypandoc.convert_text(bodyhtml, 'markdown_github', format='html')
                        f.write(writestring + "\n")
                f.close
        
    fp.close

                #currently commented out so stdout isn't cluttered
                #Also need to remove empty paragraphs
                # using github markdown with pypandoc seems to be working well
                # AND GET RID OF TRACKING BEACONS
                # <img style="overflow: hidden;position: fixed;visibility: hidden !important;display: block !important;height: 1px !important;width: 1px !important;border: 0 !important;margin: 0 !important;padding: 0 !important;" src="https://connectednation.cmail20.com/t/j-o-chklljl-yuiyjkttht/o.gif" width="1" height="1" border="0" alt="">

#NOTE: If directory does not exist, need to create KEYWORD.md and keyword-index.twig 
# (instead of blog-index.twig) and create feed.md file in content folder
                
#TODO:  The subject is a string fragment match, not a word match, gah
    #FFS THE PICO URL IS /?subdir

########################################################################
# Read ini section
########################################################################

#https://stackoverflow.com/questions/4029946/multiple-configuration-files-with-python-configparser
#multiple ini files for each section
config = configparser.ConfigParser()
IniList = os.listdir(configdir)    
for x in IniList:
    ini=os.path.join(configdir,x)
    config.read([ini])
    sections=config.sections()

########################################################################
# Main function
########################################################################
BaseOutDir=config['DEFAULT']['BaseDir']
infile = ''
infile = (sys.argv[1])  # using ini here, oh procmail copy to handle
parse_that_email(infile)
