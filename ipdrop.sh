myip=$(ip a | grep inet | grep wlan0 | awk -F" " '{print $2}')
sudo tcpdump -n -i wlan0 -c 5 | grep -oP "\b(?:\d{1,3}\.){3}\d{1,3}\b" |sort -n | uniq | grep -v $myip > ip.txt

while read ip
do sudo iptables -I INPUT 1 -s $ip/32 -m state --state NEW -j DROP
done < ip.txt

