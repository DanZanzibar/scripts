import shutil
from sys import argv

package, description = argv[1], argv[2]

shutil.copytree('/home/zan/sync-general/codehome/python/projects/skeleton/', f'/home/zan/sync-general/codehome/python/projects/{package}', ignore=shutil.ignore_patterns('.git'))
shutil.move(f'/home/zan/sync-general/codehome/python/projects/{package}/src/package/', f'/home/zan/sync-general/codehome/python/projects/{package}/src/{package}/')

with open(f'/home/zan/sync-general/codehome/python/projects/{package}/pyproject.toml') as file:
    file_text = file.read()
    file_text2 = file_text.replace('package_name', package)
    file_text3 = file_text2.replace('description_placeholder', description)

with open(f'/home/zan/sync-general/codehome/python/projects/{package}/pyproject.toml', 'w') as file:
    file.write(file_text3)
