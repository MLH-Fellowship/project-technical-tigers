#!/bin/bash

#update repo
cd project-technical-tigers
git fetch && git reset origin/main --hard
source python3-virtualenv/bin/activate
pip install -r requirements.txt

#restarting service
systemctl restart myportfolio
