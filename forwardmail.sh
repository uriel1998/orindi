#!/bin/bash


#currently borked due to sendgrid being down

exit

MAIL=/home/steven/mail
PROCMAILD=/home/steven/.config/procmail

for i in `find $MAIL/archive/dayton -type f \( -iname "*.*" ! -iname "dovecot*" ! -name "subscriptions" \) `; do
  cat "$i" | procmail $PROCMAILD/rc_dayton
  rm "$i"
done

for i in `find $MAIL/archive/deals -type f \( -iname "*.*" ! -iname "dovecot*" ! -name "subscriptions" \) `; do
  cat "$i" | procmail $PROCMAILD/rc_deals
  rm "$i"  
done

for i in `find $MAIL/archive/edeals -type f \( -iname "*.*" ! -iname "dovecot*" ! -name "subscriptions" \) `; do
  cat "$i" | procmail $PROCMAILD/rc_edeals
  rm "$i"
done

for i in `find $MAIL/archive/food -type f \( -iname "*.*" ! -iname "dovecot*" ! -name "subscriptions" \) `; do
  cat "$i" | procmail $PROCMAILD/rc_food
  rm "$i"
done

for i in `find $MAIL/archive/jobs -type f \( -iname "*.*" ! -iname "dovecot*" ! -name "subscriptions" \) `; do
  cat "$i" | procmail $PROCMAILD/rc_jobs
  rm "$i"
done

for i in `find $MAIL/archive/money -type f \( -iname "*.*" ! -iname "dovecot*" ! -name "subscriptions" \) `; do
  cat "$i" | procmail $PROCMAILD/rc_money
  rm "$i"
done

for i in `find $MAIL/archive/patreon -type f \( -iname "*.*" ! -iname "dovecot*" ! -name "subscriptions" \) `; do
  cat "$i" | procmail $PROCMAILD/rc_patreon
  rm "$i"
done

for i in `find $MAIL/archive/selfhelp -type f \( -iname "*.*" ! -iname "dovecot*" ! -name "subscriptions" \) `; do
  cat "$i" | procmail $PROCMAILD/rc_selfhelp
  rm "$i"
done

for i in `find $MAIL/archive/sjw -type f \( -iname "*.*" ! -iname "dovecot*" ! -name "subscriptions" \) `; do
  cat "$i" | procmail $PROCMAILD/rc_sjw
  rm "$i"
done
