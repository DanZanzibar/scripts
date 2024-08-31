sudo apt update

sudo snap install emacs --classic

# Bash support
sudo apt install -y shellcheck
sudo snap install bash-language-server --classic

# Global Python Tools
sudo apt install -y python3-pip
sudo apt install -y pipx
pipx install poetry
pipx install pyinstaller

# Python support
sudo snap install pyright --classic

sudo apt install -y zeal

sudo apt autoremove -y
