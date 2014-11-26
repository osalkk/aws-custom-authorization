#!/bin/bash



while read keyword           
do           
    	result=`w3m "http://www.indeed.co.uk/jobs?q=$keyword" -dump | grep  -E '(Jobs.*to)' | awk -F"of" '{print $2}' | awk -F" " '{print $1}'`
	if [ -n "$result" ]
       	then
		new=`echo $keyword | cut -d " " -f1`
		echo -e "$new \t\t $result" >> result.txt
	
	else
		echo "bos geldi" >>/dev/null
	fi	
    done <list.txt 




#w3m "http://www.indeed.co.uk/jobs?q=jenkins" -dump | grep  -E '(Jobs.*to)' | awk -F"of" '{print $2}' | awk -F" " '{print $1}'
