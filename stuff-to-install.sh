sudo apt update

# Syncthing
sudo apt install -y syncthing
systemctl --user enable syncthing.service
systemctl --user start syncthing.service

sudo snap install intellij-idea-ultimate --classic

# Git and GH - requires interactive login
sudo apt install -y git
sudo apt install -y gh
gh auth login

sudo apt autoremove -y
