#!/bin/bash
tmux kill-session -t flask; 
cd project-technical-tigers
git fetch && git reset origin/main --hard
source python3-virtualenv/bin/activate
pip install -r requirements.txt
tmux new -s flask 'flask run --host=0.0.0.0'