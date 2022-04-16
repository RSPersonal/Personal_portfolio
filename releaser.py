import os
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

from homepage.models import VersionHistory

old_history_content = ''

with open('version.txt', 'r') as file:
    print(f"Current version number is: {file.read()}")
    file.close()

new_version_number = input('Enter new version number: ')

with open('version.txt', 'w') as file:
    file.write(new_version_number)
    file.close()
    if VersionHistory.objects.filter(id=1).exists():
        version_history_object = VersionHistory.objects.get(id=1)
        version_history_object.version_number = new_version_number
        version_history_object.save()
    else:
        new_version_number_entry = VersionHistory(id=1, version_number=new_version_number)
        new_version_number_entry.save()

with open('history.txt', 'r') as file:
    old_history_content = file.read()
    file.close()

new_history_entry = input('Enter changelog entry: ')
date = datetime.now()
current_date = date.strftime("%Y-%m-%d")
with open('history.txt', 'w') as file:
    file.write(f"v{new_version_number}--{current_date}--{new_history_entry}")
    file.write('\n')
    file.write('----------------')
    file.write('\n')
    file.write(old_history_content)
    file.close()
