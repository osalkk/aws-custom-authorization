#!/bin/bash

read -p "enter search key: " key
read -p "enter search limit: " limit
read -p "enter key to search in founded jobs: " word

url="http://www.indeed.co.uk/jobs?as_and=$key&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=contract&st=&salary=&radius=25&l=&fromage=any&limit=$limit&sort=&psf=advsrch"


count=`lynx $url -dump -list_inline | grep clk | grep jk | awk -F"]" '{print $1}' | awk -F"[" '{print $2}' | xargs -n 1 lynx -dump | grep -o $word | wc -l`

echo $count "found in the job list"

