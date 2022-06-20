#!/bin/bash
#kill tmux sessions
pkill -9 tmux
#update repo
cd project-technical-tigers
git fetch && git reset origin/main --hard
source python3-virtualenv/bin/activate
pip install -r requirements.txt
#new tmux session
tmux new -d -s flask 'flask run --host=0.0.0.0'