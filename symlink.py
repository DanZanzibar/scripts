import shutil
import os
import argparse
import tomllib


filedir = os.getcwd()

filedir_basename = os.path.basename(filedir)
toml_file_name = filedir_basename + '.toml'
toml_path = os.path.join(filedir, toml_file_name)

with open(toml_path, 'rb') as file:
    toml_data = tomllib.load(file)

toml_general = toml_data['general']

parser = argparse.ArgumentParser(
    description='Symlink files in a directory to another directory.')
parser.add_argument('-s', '--symlinkdir', default=toml_general['symlink-dir'])
args = parser.parse_args()
symlinkdir = os.path.expanduser(args.symlinkdir)

ignore_files = ['.git', '.gitignore', toml_file_name, 'backup']
if 'ignore-files' in toml_general:
    ignore_files += toml_general['ignore-files']

special_locations = {}
if 'special-locations' in toml_data:
    toml_special = toml_data['special-locations']
    special_locations = {os.path.join(filedir, file): os.path.expanduser(address)
                         for file, address in toml_special.items()}

files_locations = {os.path.join(filedir, file): os.path.join(symlinkdir, file)
                   for file in os.listdir(filedir)
                   if file not in ignore_files and file not in special_locations}

files_locations.update(special_locations)

backupdir = os.path.join(filedir, "backup")
if not os.path.exists(backupdir):
    os.makedirs(backupdir)
    print('Making backup directory.')

for file, symlink in files_locations.items():
    if os.path.islink(symlink):
        os.remove(symlink)
        print(f'Existing symlink removed at {symlink}')

    elif os.path.exists(symlink):
        shutil.move(symlink, backupdir)
        print(f'Existing file backed up from {symlink}')

    os.symlink(file, symlink)
    print(f'Symlink created at {symlink}')
