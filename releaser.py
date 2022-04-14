

with open('version.txt', 'r') as file:
    print(f"Current version number is: {file.read()}")
    file.close()

new_version_number = input('Enter new version number: ')

with open('version.txt', 'w') as file:
    file.write(new_version_number)
    file.close()

