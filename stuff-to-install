sudo apt update

# Syncthing
sudo apt install -y syncthing
systemctl --user enable syncthing.service
systemctl --user start syncthing.service

# SSH
sudo apt install -y openssh-server
sudo systemctl start ssh.service
sudo systemctl enable ssh.service

# Converts .msg (Outlook) files to .eml via the 'msgconvert' command.
sudo apt install -y libemail-outlook-message-perl

# Intellij-IDEA
sudo snap install intellij-idea-ultimate --classic

# Git and GH - requires interactive login
sudo apt install -y git
sudo apt install -y gh
gh auth login

sudo apt autoremove -y
