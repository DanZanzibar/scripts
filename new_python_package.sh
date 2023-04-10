#!/bin/bash
read -p "Name of new package?: " package
read -p "Short description of package?: " description
python3 ~/scripts/new_package.py $package "$description"
cd ~/codehome/python/projects/$package
git init
git add *
git add .gitignore
git commit -m 'initial commit'