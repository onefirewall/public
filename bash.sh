rm -rf clean_elastic.py
rm -rf match_syslog_ofa.py 
wget https://raw.githubusercontent.com/onefirewall/public/master/clean_elastic.py
wget https://raw.githubusercontent.com/onefirewall/public/master/match_syslog_ofa.py
ls -ls
python3 clean_elastic.py
