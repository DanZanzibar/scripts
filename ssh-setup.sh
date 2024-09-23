# Until I set up a bash function to get the computer name, this script is just for reading.

# Set up key using 'ecdsa' algorithm with 521 bit size.
ssh-keygen -t ecdsa -b 521

# Copy key to host machine.
ssh-copy-id -i .ssh/id_ecdsa.pub zan@ #host machine

# Once all keys are set up for clients, remove password auth on host.
sudo emacs -nw /etc/ssh/sshd_config
# Set the line 'Password Authentication no'.
