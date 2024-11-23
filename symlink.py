#!/usr/bin/python3

from os import mkdir, symlink, listdir, rmdir, remove
from os.path import join, basename, exists, expandvars, islink, isfile, isdir
from shutil import move


HOME = '/home/zan'
DOTS = join(HOME, 'dotfiles')
CONFIG = join(HOME, '.config')
BACKUP = join(DOTS, 'backup')
HOST_DIR = join(DOTS, expandvars('$HOSTNAME'))

SYMLINK_ALL_IN_DIRS = [
    (join(DOTS, 'home'), HOME),
    (join(DOTS, 'config'), CONFIG),
    (join(DOTS, 'xorg.conf.d'), '/etc/X11/xorg.conf.d'),
    (join(HOST_DIR, 'xorg.conf.d'), '/etc/X11/xorg.conf.d'),
    (join(DOTS, 'udev-rules'), '/etc/udev/rules.d')
]
SYMLINK_OTHERS = [
    (join(HOST_DIR, 'autorandr'), CONFIG),
    (join(HOST_DIR, '.Xresources'), HOME),
    (join(DOTS, 'herbstluftwm/autostart'), join(CONFIG, 'herbstluftwm')),
    (join(DOTS, 'gtk-3.0'), CONFIG)
]


def backup_or_remove(path: str) -> None:
    backup_path = join(BACKUP, basename(path))
    if islink(path):
        remove(path)
        print(f'Old link at {path} removed.')
    elif exists(path):
        if islink(backup_path) or isfile(backup_path):
            remove(backup_path)
            print(f'Old backup {backup_path} removed.')
        elif isdir(backup_path):
            rmdir(backup_path)
            print(f'Old backed up directory {backup_path} removed.')
        move(path, backup_path)
        print(f'Back created for {path}')
        

def backup_and_symlink(source: str, dest_dir: str) -> None:
    dest = join(dest_dir, basename(source))
    backup_or_remove(dest)
    symlink(source, dest)
    print(f'{dest} symlinked to {source}')

def symlink_all_in_dir(source_dir: str, dest_dir: str) -> None:
    if not exists(dest_dir):
        mkdir(dest_dir)
    for file_name in listdir(source_dir):
        source = join(source_dir, file_name)
        backup_and_symlink(source, dest_dir)


for source_dir, dest_dir in SYMLINK_ALL_IN_DIRS:
    symlink_all_in_dir(source_dir, dest_dir)

for source, dest_dir in SYMLINK_OTHERS:
    backup_and_symlink(source, dest_dir)
