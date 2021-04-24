#!/bin/bash


#get install directory
export SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
# Needed for unredirector
source `which muna.sh`

if [ ! -d "$1" ];then
    EMAIL_DIR=${SCRIPT_DIR}
else
    EMAIL_DIR="${1}"
fi

function ProgressBar {
# Process data
    let _progress=(${1}*100/${2}*100)/100
    let _done=(${_progress}*4)/10
    let _left=40-$_done
# Build progressbar string lengths
    _fill=$(printf "%${_done}s")
    _empty=$(printf "%${_left}s")

# 1.2 Build progressbar strings and print the ProgressBar line
# 1.2.1 Output example:                           
# 1.2.1.1 Progress : [########################################] 100%
printf "\rProgress : [${_fill// /#}${_empty// /-}] ${_progress}%%"

}

tfile=$(mktemp)
tfile2=$(mktemp)
tfile3=$(mktemp)
tfile4=$(mktemp)


while IFS= read -d $'\0' -r file ;do
    #Just in Case
    if [[ "${file}" == *'dovecot'* ]];then
        echo "Skipping dovecot file"
    else
        echo "Processing ${file}"
        cat "${file}" | sed '1,/X-Report-Abuse-To/d' | sed 's/=$//' | sed 's/=3D/=/g' | sed 's/=09/ /g' | sed 's/=2E/./g'  | lynx -dump -stdin -display_charset UTF-8 -width 140 -hiddenlinks=merge -listonly | awk '{print $2}' >> $tfile
        rm "${file}"
    fi
done < <(find ${EMAIL_DIR} -type f -print0 )

cat $tfile | sort | awk '!_[$0]++' > $tfile2
echo "Unredirecting and selecting URLs"

let i=0
totallines=$(wc -l "$tfile2")

while read -r line; do 
    ((i++))
    ProgressBar $i $totallines
    if [ ! -z "$line" ];then 
        #echo "$line"
        url=$(printf "%s" "$line")
        unredirector #because $url is now set
        #echo "$url"
        if [ ! -z "$url" ];then  #yup, that url exists; just skipping if it doesn't
            #echo "$url"
            if [[ "$url" =~ ^http[?s]://www.elephantjournal.com\/[0-9][0-9][0-9][0-9] ]];then
                echo "$url" >> "$tfile3"
                #echo "BOOH"
            fi 
        fi
    fi
done < <(cat $tfile2)

if [ ! -f ${SCRIPT_DIR}/ej_queue.txt ];then 
    touch ${SCRIPT_DIR}/ej_queue.txt
fi

if [ ! -f ${SCRIPT_DIR}/ej_done.txt ];then 
    touch ${SCRIPT_DIR}/ej_done.txt
fi


cat "$tfile3" | sort | awk '!_[$0]++' > ${SCRIPT_DIR}/ej_queue.txt

### NOW TO GET THE FILES

echo "Fetching, converting, and cleaning URLs"

# Removing comment feed posts
sed -i '/#comments/d' ${SCRIPT_DIR}/ej_queue.txt

let b=0
totallines=$(wc -l "${SCRIPT_DIR}/ej_queue.txt")

while read -r line; do
    haveit=$(grep -c "$line" ${SCRIPT_DIR}/ej_done.txt)
    ((b++))
    ProgressBar $b $totallines
    if [[ $haveit -lt 1 ]];then
   
        echo "$line" >> ${SCRIPT_DIR}/ej_done.txt
        # Getting the last part of the url is useful, so there's no / 
        # hoping substitution works here and that inline editing doesn't mess up the loop
        keyurl=$(echo "$line" | awk -F '/' '{print $6}')
        sed -i "/$keyurl/d" ${SCRIPT_DIR}/ej_queue.txt  
        curl -s -b ${SCRIPT_DIR}/elephant_journal_cookies.txt "$line" -o ${tfile4}
        dadate=$(curl -s -I -b ${SCRIPT_DIR}/elephant_journal_cookies.txt "$line" | grep -e "^date" | awk -F ':' '{print $2 ":" $3 ":" $4}')
        title=$(hxextract title ${tfile4} 2>/dev/null | cut -d'>' -f2 | cut -d'|' -f1 )
        if [[ "$title" == *'{Partner}'* ]];then
            echo "Partner sponsored post; skipping."
        else
            outfile=$(echo ${SCRIPT_DIR}/data/ej_`date +%s`.md)
            touch ${outfile}
            printf "%s\n" "---" >> ${outfile}
            printf "Title: %s\n" "${title}" >> ${outfile}
            printf "Description: %s\n" "${title}" >> ${outfile}
            printf "Author: 'Elephant Journal'\n" >> ${outfile}
            printf "Date: %s\n" "${dadate}" >> ${outfile}
            printf "Template: index\n" >> ${outfile}
            printf "%s\n" "Robots: noindex,nofollow" >> ${outfile}
            printf "%s\n\n\n" "---" >> ${outfile}
            printf "<h1>%s</h1>\n\n" "$title" >> ${outfile}
           

            hxextract -s '<html><body>' -e '</body></html>' ".content-wrap" ${tfile4} 2>/dev/null | \
             xml2asc | hxprune -c cat-author | hxprune -c comments-area | hxprune -c ej-oembed | \
             hxprune -c relephant-headline | hxprune -c relephant-article | hxprune -c relephant-article |hxprune -c above-footer-wrapper | \
             hxprune -c author | hxprune -c feed-more | hxprune -c tab-section | \
             hxprune -c ej-post-meta | hxprune -c footer-bucket | \
             hxprune -c element-form | hxprune -c full-width-footer-wrap | sed -e 's/<img[^>]*>//g' | \
             sed -e 's/<div[^>]*>//g' | hxclean | hxnormalize -e -L -s 2>/dev/null | \
             tidy -quiet -omit -clean 2>/dev/null | hxunent | iconv -t utf-8//TRANSLIT - | \
             sed -e 's/\(<em>\|<i>\|<\/em>\|<\/i>\)/\^/g' | \
             sed -e 's/\(<strong>\|<b>\|<\/strong>\|<\/b>\)/\^/g' | \
             lynx -dump -stdin -display_charset UTF-8 -width 80 | \
             sed -e 's/\*/•/g' | sed -e 's/Θ/\*/g' | sed -e 's/Φ/🞯/g' | sed 's/^/\t/' | sed -e 's/\^/\*/g' | sed -e 's/^[ \t]*//' \
              >> ${outfile} 
            
#TODO: Extract further URLs (and then select what we want) via cat ${tfile4} | hxwls  
# Would probably require making these all functions, but it could also lead to a 
# LOT of reprocessing. Except onthe webpage there's no need for redirect...
            printf "\n\nOriginally found at %s\n\n" "$line" >> ${outfile}      
        fi
    fi
done < <(cat ${SCRIPT_DIR}/ej_queue.txt)
echo " "

echo "Cleaning up"
rm "$tfile1"
rm "$tfile2"
rm "$tfile3"
rm "$tfile4"

