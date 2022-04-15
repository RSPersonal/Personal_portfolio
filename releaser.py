old_history_content = ''

with open('version.txt', 'r') as file:
    print(f"Current version number is: {file.read()}")
    file.close()

new_version_number = input('Enter new version number: ')

with open('version.txt', 'w') as file:
    file.write(new_version_number)
    file.close()

with open('history.txt', 'r') as file:
    old_history_content = file.read()
    file.close()

new_history_entry = input('Enter changelog entry: ')

with open('history.txt', 'w') as file:
    file.write(f"v{new_version_number}--{new_history_entry}")
    file.write('\n')
    file.write('----------------')
    file.write(old_history_content)
    file.close()
