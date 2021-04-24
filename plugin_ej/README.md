This is a sort-of plugin for [orindi](https://uriel1998.github.io/orindi), 
specifically for someone who has *subscribed* to elephant journal but wants 
to read articles off the website.

The script can work on its own, but it fits seamlessly alongside an installation 
of `orindi`, since that's what I use as well.  :)

Elephant Journal annoyingly does not have an RSS feed, or a way to even read 
the front page without loading javascript.  It does, however, have a daily 
mailer.  To make this work, have `imapfilter` or another tool move the emails 
to the directory of your choice.  (It works with a maildir directory.)  

You will need to get your cookies in 
[netscape format](https://everything.curl.dev/http/cookies). I used 
[EditThisCookie](http://www.editthiscookie.com/).  Place them in the script 
installation directory in a file named `elephant_journal_cookies.txt` .

Create a new subdirectory in your pico installation (and the relevant config 
files) as you do for [orindi](https://uriel1998.github.io/orindi).  Make a 
symbolic link from that content directory to a ./data subdirectory for this 
script.  For example, if I installed this script in `/home/steven/plugin_ej`,:

`/var/www/pico/content/journal`  ->  `/home/steven/apps/plugin_ej/data`

Then, perhaps every day or so, run `process_ej.sh`, feeding it the directory 
where the mails are as the sole output variable.  

It will parse the emails for URLs, unobfuscate them, only select articles from 
EJ, make sure you've not already got them, then download them, strip all the 
extra crap (200k on average down to less than 10k) and place them nicely in 
`./data` in pico-ready markdown.  

It maintains two text files - `ej_queue.txt` and `ej_done.txt` to accomplish 
this.

It requires `muna`, `HTML-XML-utilities`, `lynx`, `tidy`, and of course, `pico`.
