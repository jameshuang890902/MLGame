#!/bin/zsh
for ((i=1;i<=5;i++))
do
# python MLGame.py -1 -r -f 500  -i rule.py  arkanoid EASY 1
python MLGame.py -1 -r -f 800  -i data_final.py  arkanoid EASY 1
python MLGame.py -1 -r -f 800  -i data_final.py  arkanoid EASY 2
python MLGame.py -1 -r -f 800  -i data_final.py  arkanoid EASY 3
python MLGame.py -1 -r -f 800  -i data_final.py  arkanoid NORMAL 1
python MLGame.py -1 -r -f 800  -i data_final.py  arkanoid NORMAL 2
python MLGame.py -1 -r -f 800  -i data_final.py  arkanoid NORMAL 3
done