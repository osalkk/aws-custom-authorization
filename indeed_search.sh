w3m "http://www.indeed.co.uk/jobs?q=jenkins" -dump | grep  -E '(Jobs.*to)' | awk -F"of" '{print $2}' | awk -F" " '{print $1}'
