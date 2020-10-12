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

The idea is that this should be able to slip into your existing workflow, 
regardless of what that is or what you're using.  And if it doesn't, it's meant 
to be as simple as possible to customize the code.

### Why Pico and Procmail?

I'd previously used [Kill The Newsletter](https://www.kill-the-newsletter.com/) 
which did a bangup job. But when the author changed it from using a cloud service 
to exim, I had a problem. I don't use exim, and the configuration was in the code 
that I (quite frankly) don't have the skill to understand.

Therefore, I wanted something that would rely on [procmail](https://linux.die.net/man/5/procmailrc), which can work with 
pretty much any mail transfer agent seamlessly, including after delivery if 
mail is in the maildir format.  (See [TODO](#6-todo) if you're about to say I 
should use something different like `courier-maildrop`.)

[Pico](http://picocms.org/) provides a good front-end for similar reasons. 
It's lightweight, does not require one to disrupt their existing setup, deals 
with plain text files, and can generate RSS feeds fairly easily.


## 2. License

This project is licensed under the MIT License. For the full license, see `LICENSE`.

## 3. Prerequisites

* [Pandoc](https://pandoc.org/)  
* [Pico](http://picocms.org/)   
* [procmail](https://linux.die.net/man/5/procmailrc)  


## 4. Installation

Ideally, you should create a virtualenv for this project, as there are a number 
of python dependencies.  Instructions on how to do that are beyond the scope of 
this document.  It is assumed that you have created and activated the 
virtualenv henceforth.

### Install MDA / procmail  

* This should be handled by your package manager.

### Install pandoc

* Follow the instructions at [Pandoc's documentation](https://pandoc.org/installing.html).  

### Install pico 

The instructions and program as written presume that `pico` is local to `orindi`. 
If the files need to be uploaded elsewhere by a script after processing, you will 
need a local mirror for the files to be written into. The user that runs `orindi` 
should be part of the same user group as pico (www-data, probably). 

* NOTE:  Tested with php7.3; when I had older versions of PHP the program ran 
just fine, but the output (particularly of the RSS feed) was sometimes mis-parsed.


* Follow the installation instructions in [pico's documentation](http://picocms.org/docs/).  
* Copy `orindi-index.twig` to pico's `/themes/default` directory.
* Copy `index.md` to pico's `/content` directory.
* Change permissions on pico's `/content` and `/themes/default` directory to 775 and
use the sticky bit (`chmod -t DIRECTORY`) to reduce the possibility of permission 
issues.  
* Optionally, if your setup will allow it, you may install pico somewhere else 
(such as in the same directory as `orindi`) and create a symlink to /var/www/html 
or wherever your webserver can see it.
* If you have problems with serving HTTPS, you may need to manually set 
`themes_url`, `base_url`, `assets_url`, `plugins_url`, and `rewrite_url` 
in `pico/config/config.yml`.  


### Install python modules and application

* `pip install -r requirements.txt` or `pip3 install -r requirements.txt` if you didn't make a venv and still have python2 installed.
* `mkdir -p $HOME/.config/orindi`
* Edit `orindi.ini` (see instructions below)
* `cp $PWD/orindi.ini $HOME/.config/orindi`
* Edit `orindi_procmailrc` (see instructions below)
* `cp $PWD/orindi_procmailrc $HOME/.config/procmail`
* `sudo chmod +x $PWD/orindi_parse.py`


### orindi_procmailrc setup  

There is only one thing to change in the procmail rc file:
```
:0Wc:
| /path/to/orindi/orindi_parse.py
```

Type in the path to orindi_parse.py on the second line, making sure you keep 
the pipe character.  This will pass a *copy* of each email on to `orindi`, and 
then allow it to be delivered normally.  

You *may* try letting `procmail` not wait between each email to process it; if 
you do, change the first line to `:0c:`.  

There is an alternate way to use procmail to match mails instead of using `orindi`, 
but since `orindi` must also have that list, you'll end up having to keep 
multiple lists synchronized... 

**Integrating procmail with your MTA is an exercise for the user.** 

### INI files setup

`orindi` can have one or many ini files; it's all up to how you want to 
organize things ... and how many things you're filtering for.  You *must* have 
`orindi.ini` in the configuration directory. The main `orindi.ini` file 
must have these lines (with the appropriate values):  

```
[DEFAULT]  
BaseDir = /var/www/html/pico/content  
BaseThemeDir = /var/www/html/pico/themes/default  
AppDir = /where/orindi/is/installed/to  
```

After that you can configure any number of feeds and the criteria that they 
match on.  You can put them all in one file, or in separate files in 
`$HOME/.config/orindi`.  For each feed, there are four elements.

* The label (the bit in brackets).  They should be in the format *feed###*, and each should be unique across *all* ini files.
* The keyword. This is how it will be organized under `pico`. 
* A list (indented if multiline) of strings that will be tested against the "from" field
* A list (comma separated) of strings that will be tested against the "subject" field.

Example: 

```
[feed5]
keyword = crowdfunding
from = @indiegogo.com
    bingo@patreon.com
    no-reply@patreon.com
    messages@gofundme.com
    gfm-community@gofundme.com
    hello@gofundme.com
    news@gofundme.com
    no-reply@kickstarter.com    
subject = Thanks for becoming a backer,Project Update,launched

```

Any mail that `orindi` gets that matches either the "from" condition or the 
"subject" condition will be put into the "crowdfunding" subdirectory and 
"crowdfunding" feed.

### Security  

There is no default security set up with `orindi`.  This is not ideal, for 
obvious reasons.

The easiest way is to use *htaccess* basic authentication.  Instructions on 
setting up *htaccess* for [Apache](https://www.elated.com/password-protecting-your-pages-with-htaccess/) and [Nginx](https://docs.nginx.com/nginx/admin-guide/security-controls/configuring-http-basic-authentication/) are available on the web (or the links in this sentence).

Once you've set up *htaccess* authentication, the generated RSS feeds are 
accessible at:

`https://USERNAME:PASSWORD@domain.for.your.site/feed-link`


## 5. Usage

`orindi` takes an email from either stdin or as a filename from the first 
command line variable. This provides additional flexibility in inserting it into 
your already existing workflow. 

It even works for already existent mail that is in the MAILDIR format.  For 
example, if you were to use `offlineimap` and `getmail` to pull down your 
email to a single directory, you could then use this bit of bash in a script 
to process the files:

``
for i in `find $MAILDIR -type f \( -iname "*.*" ! -iname "dovecot*" ! -name "subscriptions" \) `; do
  cat "$i" | procmail $PROCMAILD/orindi_procmailrc
done
``

or just as validly, use this bit of bash to do the same thing:

``
for i in `find $MAILDIR -type f \( -iname "*.*" ! -iname "dovecot*" ! -name "subscriptions" \) `; do
  $PATH/TO/orindi_parse.py "$i"
done
``

(If you wished to remove the files, obviously just add `rm "$i"` to the loop.)

A warning with the latter; the filenames that `dovecot` uses (at least) will 
sometimes completely pooch the process.

Or you could even use the same to process a different mailbox after some other 
program has had a crack at it.  


### Cleaning up  

When processing, `orindi` will set the outputted file to the same date/time 
as the mail header, which will help with maintenance and housekeeping.  

The easiest way to clean up old files is through using a script like this, 
substituting your pico content directory where appropriate:  

```
for i in `find /var/www/html/pico/content/ -type d | grep -v -e "content/$" | xargs realpath`; do 
    find "$i" -mtime +30 | xargs rm -f
    find "$i" -atime +30 | xargs rm -f
done

```

The reverse grep is needed so you don't accidentally delete your subject index 
files in the main content directory.  Of course, if you use pico for other 
sites, you will want to edit the script appropriately.

### Viewing the output

If `pico` is installed in the subdirectory `/pico` to your domain, then you 
can view it at `yourdomain.com/pico`.  Each keyword's output is viewable at 
`yourdomain/pico/?keyword` and the RSS feed is available at `yourdomain/pico/?keyword-feed`. 

To use the example above, that means I could see an index of the emails at 
`yourdomain/pico/?crowdfunding` and get the RSS feed at `yourdomain/pico/?crowdfunding-feed`.

MOST emails look pretty much how they're supposed to.  Linkedin emails seem to
get mangled to hell.  Some extra spaces and linefeeds, but I'm not sure I want 
to keep trying to parse them in the main program...

## 6. TODO


* Customize pico's theme a little bit
* Which plugins should be added in (recommendations, anyway):
    https://github.com/alejandroliu/ForceHttpsPlugin
* Per section output chooser - (or rather, first attempt one) so that we're not tied to pandoc so hard  
* Clean output further - remove empty paragraphs, maybe a tidy library? (Beautiful Soup did a LOT, though)
* Try use of dehtml instead of pypandoc
* Remove tracking beacons completely.  Not sure how other than to look for 
  img tags with small pixel sizes or img style="overflow: hidden"
```
<img style="overflow: hidden;position: fixed;visibility: hidden !important;display: block !important;height: 1px !important;width: 1px !important;border: 0 !important;margin: 0 !important;padding: 0 !important;" src="https://connectednation.cmail20.com/t/j-o-chklljl-yuiyjkttht/o.gif" width="1" height="1" border="0" alt="">
```
* Enable use of [courier-maildrop](http://www.courier-mta.org/maildrop/) instead of procmail.
* See if procmail has to wait between deliveries
* Use errorcodes (sys.exit(3) for example) to indicate non-match?


### Roadmap:

