# orindi

Transform your e-mail newsletters into webpages and an RSS feed. Uses pico as a front end.
`orindi` is an anglicization of ørindi, meaning "message".


![orindi logo](https://raw.githubusercontent.com/uriel1998/orindi/master/orindi-icon.png "logo")

## Contents
 1. [About](#1-about)
 2. [License](#2-license)
 3. [Prerequisites](#3-prerequisites)
 4. [Installation](#4-installation)
 5. [Usage](#5-usage)
 6. [TODO](#6-todo)

***

## 1. About

Transform your e-mail newsletters into webpages and an RSS feed. Uses pico as a front end.
`orindi` is an anglicization of ørindi, meaning "message".


## 2. License

This project is licensed under the MIT License. For the full license, see `LICENSE`.

## 3. Prerequisites


ShortUUID https://github.com/skorokithakis/shortuuid
#REQUIRES
#https://github.com/SpamScope/mail-parser
#https://pypi.org/project/mail-parser/
#pypandoc from package (python3-pypandoc) or via pip  https://pypi.org/project/pypandoc/
#beautifulsoup - because holy crap, there's a lot of bad html out there.

## 4. Installation

### Installation of pico - include feed.twig creation as setup process.
Basedir should be the base CONTENT directory.  
Indent for multiline input
multifile input as well, woot.

User should be part of same group as pico (www-data, probably) and CHMOD pico/content and pico/themes to 775 instead of 755 and use sticky bit (chmod -t DIR) to reduce probability 
of malicious overwrites, etc.

ini files help keep things separate, but can be all in one as well. Just make 
sure the `[feed#]` tags are different so it doesn't overwrite

## 5. Usage

THE PICO URL IS /?subdir
So http://bunyip.stevesaus.me/pico/?sjw-feed
for the feed

MOST emails look pretty much how they're supposed to.  Linkedin emails seem to
get mangled to hell.  Some extra spaces and linefeeds, but I'm not sure I want 
to keep trying to parse them in the main program...

## 6. TODO

* I don't want to further customize themes. Seems like against the point of 
  pico here.  However, should have default index.md that shows ALL pages, right?
* Add a header/footer which reflects the program.  (But it also is beside the 
  point because we're using pico to make an RSS feed anyway)
* Which plugins should be added in (recommendations, anyway):
    - GZIP
    - PicoTooManyPages
    - Pico-Robots
    - pico-minify
* Per section output chooser - (or rather, first attempt one)  
* Clean output further - remove empty paragraphs, maybe a tidy library? (Beautiful Soup did a LOT, though)
* Remove tracking beacons completely.  Not sure how other than to look for 
  img tags with small pixel sizes or img style="overflow: hidden"

<img style="overflow: hidden;position: fixed;visibility: hidden !important;display: block !important;height: 1px !important;width: 1px !important;border: 0 !important;margin: 0 !important;padding: 0 !important;" src="https://connectednation.cmail20.com/t/j-o-chklljl-yuiyjkttht/o.gif" width="1" height="1" border="0" alt="">
* set up input from procmail as well, right now we can scan a directory or take an input file only
* Clean up documentation, duh
* Create requirements.txt

### Roadmap:

