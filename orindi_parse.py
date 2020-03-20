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
from bs4 import BeautifulSoup
import tempfile
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
    
    
def replace_last(string, find, replace):
    reversed = string[::-1]
    replaced = reversed.replace(find[::-1], replace[::-1], 1)
    return replaced[::-1]

def replace_first(string, find, replace):
    replaced = string.replace(find,replace, 1)
    return replaced
    
    
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
    print ('Parsing message file  ' + messagefile)
    
    with open(messagefile,'r') as fp:
         mail = mailparser.parse_from_file_obj(fp)

    # Making sure there's not a missing date/time attribute here
    if mail.date:
        date_time_obj = datetime.datetime.strptime(str(mail.date),"%Y-%m-%d %H:%M:%S")
    else:
        thetime=time.strftime("%Y-%m-%d %H:%M:%S",localtime())
        date_time_obj=datetime.datetime.strptime(thetime,"%Y-%m-%d %H:%M:%S")
    
    mailtime=(str(date_time_obj.date()) + ' ' + str(date_time_obj.time()))

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
                f.write('Date: ' + str(mailtime) + "\n")
                f.write('Robots: noindex,nofollow' + "\n")
                f.write('Template: index' + "\n")
                f.write ('---' + "\n")
                if mail.text_html:
                    bodyhtml=str(mail.text_html)
                    bodyhtml=replace_first(bodyhtml,"['","")
                    bodyhtml=replace_last(bodyhtml,"']","")
                    bodyhtml = bodyhtml.replace("=\n", "")
                    bodyhtml = bodyhtml.replace("\n", "")
                    bodyhtml=unescape(bodyhtml)
                    tree = BeautifulSoup(bodyhtml, 'lxml')
                    bodyhtml = tree.prettify()
                    bodyhtml = bodyhtml.replace("\\n", "<br />").replace("\\t", "")
                    writestring = pypandoc.convert_text(bodyhtml, 'markdown_github', format='html')
                    writestring = writestring.replace("\nstyle", " style")
                    writestring = writestring.replace("\n]", "]")
                    writestring = writestring.replace("[\n", "[")
                    f.write(writestring + "\n")
                else:
                    if mail.text_plain:
                        bodytxt = clean_string(mail.text_plain)
                        f.write(bodytxt + "\n")
                    else: 
                        bodyhtml=str(mail.text_not_managed)
                        bodyhtml=replace_first(bodyhtml,"['","")
                        bodyhtml=replace_last(bodyhtml,"']","")
                        bodyhtml = bodyhtml.replace("=\n", "")
                        bodyhtml=unescape(bodyhtml)
                        tree = BeautifulSoup(bodyhtml, 'lxml')
                        bodyhtml = tree.prettify()
                        bodyhtml = bodyhtml.replace("\\n", "<br />").replace("\\t", "")
                        writestring = pypandoc.convert_text(bodyhtml, 'markdown_github', format='html')
                        writestring = writestring.replace("\nstyle", " style")
                        f.write(writestring + "\n")
                f.close
        
    fp.close

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
if len(sys.argv)!= 2:
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as afp:
        inf = sys.stdin
        lines = inf.readlines()
        for line in lines:
            afp.write(line)
        afp.close
    infile = afp.name
else:
    infile = (sys.argv[1])  
        
parse_that_email(infile)


cleanit = afp.name
if os.path.exists(cleanit):
    os.unlink(cleanit)