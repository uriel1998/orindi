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
# Getting rid of problematic characters
########################################################################
def clean_string(instring):
    returnstring=str(instring)
    returnstring=unescape(returnstring)
    returnstring=returnstring.replace(':',' ').replace('|', ' ').replace('/',' ').replace('\\',' ').replace('  ',' ').replace('[', ' ').replace(']', ' ').replace('(', ' ').replace(')', ' ').replace("'", '’').replace('"', '“').replace('\n', '').replace('\r', '').replace('\t', '')
    return returnstring
    
    
########################################################################
# When a section doesn't exist yet and needs set up.
########################################################################
def make_new_section(section,fulloutdir,appdir,basethemedir,basedir):
    
    os.makedirs(fulloutdir)
    TemplateList = 'section_md.template section-feed_md.template section-feed_twig.template section-index_twig.template'
    for x in TemplateList.split(' '):
        templatefile=os.path.join(appdir,x)
        tmp1 = x.replace(".template", "").replace("_", ".").replace("section",section)
        if "twig" not in tmp1:
            outfile=os.path.join(basedir,tmp1)
        else:
            outfile=os.path.join(basethemedir,tmp1)
 
        if templatefile:
            infile = open(templatefile,'r')
            lines = infile.readlines()
            infile.close
            out = open(outfile, 'w')
            for line in lines:
                line = line.replace("@SECTION@",section)
                out.write(line)
            out.close
    

########################################################################
# Parsing that email!
########################################################################
def parse_that_email(messagefile):
    #print ('Message file is ' + messagefile)
    
    with open(messagefile,'r') as fp:
         mail = mailparser.parse_from_file_obj(fp)

    date_time_obj = datetime.datetime.strptime(str(mail.date),"%Y-%m-%d %H:%M:%S")
    #print (str(date_time_obj.date()) + '-' + str(date_time_obj.time()))

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
            
            fromliststr = clean_string(mail.from_)
            
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
            if not outdir:
                if SubjectList:
                    for y in SubjectList.split(','):
                        if y in str.lower(mail.subject):
                            outdir = keyword
            if outdir:
                
                FullOutDir = BaseOutDir + '/' + outdir
                if not os.path.isdir(FullOutDir):
                    make_new_section(outdir,FullOutDir,AppDir,BaseThemeDir,BaseOutDir)

                filename=shortuuid.uuid() + '.md'
                postfile = BaseOutDir + '/' + outdir + '/' + filename
                f = open(postfile, 'w')

                f.write ('---' + "\n")
                f.write('Title: ' + clean_string(mail.subject) + "\n")
                f.write('Description: ' + clean_string(mail.subject) + "\n")
                f.write('Author: ' + FromString + "\n")
                f.write('Date: ' + str(mail.date) + "\n")
                f.write('Robots: noindex,nofollow' + "\n")
                f.write('Template: index' + "\n")
                f.write ('---' + "\n")
                if mail.text_html:
                    bodyhtml = clean_string(mail.text_html)
                    bodyhtml = bodyhtml.replace("\\n", "<br />").replace("\\t", "")
                    writestring = pypandoc.convert_text(bodyhtml, 'markdown_github', format='html')
                    f.write(writestring + "\n")
                else:
                    if mail.text_plain:
                        bodytxt = clean_string(mail.text_plain)
                        f.write(bodytxt + "\n")
                    else: 
                        bodyhtml = clean_string(mail.text_not_managed)
                        bodyhtml = bodyhtml.replace("\\n", "").replace("\\t", "")
                        writestring = pypandoc.convert_text(bodyhtml, 'markdown_github', format='html')
                        f.write(writestring + "\n")
                f.close
        
    fp.close
                #currently commented out so stdout isn't cluttered
#TODO Also need to remove empty paragraphs
                # using github markdown with pypandoc seems to be working well
# TODO GET RID OF TRACKING BEACONS
                # <img style="overflow: hidden;position: fixed;visibility: hidden !important;display: block !important;height: 1px !important;width: 1px !important;border: 0 !important;margin: 0 !important;padding: 0 !important;" src="https://connectednation.cmail20.com/t/j-o-chklljl-yuiyjkttht/o.gif" width="1" height="1" border="0" alt="">

#NOTE: If directory does not exist, need to create KEYWORD.md and keyword-index.twig 
# (instead of blog-index.twig) and create feed.md file in content folder
                
#TODO:  The subject is a string fragment match, not a word match, gah
#TODO THE PICO URL IS /?subdir
#TODO: Determine which kind of parsing should be done first, then do that. 
#TODO:
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
BaseThemeDir=config['DEFAULT']['BaseThemeDir']
AppDir=config['DEFAULT']['AppDir']
infile = ''
infile = (sys.argv[1])  # using ini here, oh procmail copy to handle
parse_that_email(infile)
