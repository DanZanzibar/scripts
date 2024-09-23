sudo apt update

sudo snap install emacs --classic

# Bash support
sudo apt install -y shellcheck
sudo snap install bash-language-server --classic

# PDF-tools and doc-toc dependencies
sudo apt install poppler-utils
sudo apt install -y fntsample
sudo apt install -y djview4

# Global Python Tools
sudo apt install -y python3-pip
sudo apt install -y pipx
pipx install poetry
pipx install pyinstaller
# maybe pylint?

# Python support
sudo snap install pyright --classic

# C language server
sudo apt install -y clangd
sudo apt install -y cmake

sudo apt install -y zeal

sudo apt autoremove -y
