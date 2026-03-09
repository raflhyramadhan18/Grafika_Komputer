# Using "with" statement to read from the file
with open('tips.csv', 'r') as file:
    content = file.read()
print(content)
