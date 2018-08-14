# Start with /usr/share/dict
cat /usr/share/dict/words > laywords.txt

# A nice archive: https://github.com/dwyl/english-words
git clone https://github.com/dwyl/english-words.git
cat english-words/*.txt >> laywords.txt

# WordNet
# Princeton University "About WordNet." WordNet. Princeton University. 2010.
wget http://wordnetcode.princeton.edu/3.0/WNdb-3.0.tar.gz
tar -xzvf WNdb-3.0.tar.gz
grep -hEo '^[^,% ]+' dict/index.* >> laywords.txt


# aspell words
wget http://downloads.sourceforge.net/wordlist/scowl-2018.04.16.tar.gz
grep -hEo '^[^ ]+' scowl-2018.04.16/final/* >> laywords.txt


# Convert to lowercase, sort, & dedupe
cat laywords.txt | tr '[:upper:]' '[:lower:]' | sort | uniq > laywordlist.txt
