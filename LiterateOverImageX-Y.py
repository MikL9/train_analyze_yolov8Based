import os
import re

folder_path = r'C:\Users\1070PC\PycharmProjects\datasets\pothole_dataset_v8\train\images'
pattern = re.compile(r'\d+')  # regular expression to match any sequence of digits

numbers = []
for filename in os.listdir(folder_path):
    match = pattern.search(filename)
    if match:
        number = int(match.group())
        numbers.append(number)

sorted_numbers = sorted(numbers)
print(sorted_numbers)
print(len(sorted_numbers))

folder_path = r'C:\Users\1070PC\PycharmProjects\datasets\pothole_dataset_v8\train\labels'
allowed_numbers = sorted_numbers
pattern = re.compile(r'image(\d+)\.txt')

for filename in os.listdir(folder_path):
    match = pattern.search(filename)
    if match:
        number = int(match.group(1))
        if number not in allowed_numbers:
            print(os.path.join(folder_path, filename))
            os.remove(os.path.join(folder_path, filename))
