import os
import shutil


def generate_numbers(string):
    start, end = map(int, string.split('-'))
    return range(start, end + 1)


def read_file(path):
    with open(path, 'r') as file:
        content = file.read()
        ranges = content.split(',')
        numbers = []
        for r in ranges:
            if '-' in r:
                numbers.extend(generate_numbers(r))
            else:
                numbers.append(int(r.strip()))

        print(numbers)
        return numbers


def delete_files(numbers):
    for number in numbers:
        filename = f"image{number}.jpg"
        path = f"RetestAll/images/{filename}"
        if os.path.exists(path):
            # os.remove(path)
            print(f"Deleted file {filename}")
        else:
            print(f"File {filename} not found")


def move_files(numbers):
    for number in numbers:
        filename = f"image{number}.jpg"
        source_path = f"RetestAll/images/{filename}"
        destination_path = f"RetestAll/to_del/{filename}"
        if os.path.exists(source_path):
            shutil.move(source_path, destination_path)
            print(f"Moved file {filename}")
        else:
            print(f"File {filename} not found")


def move_labels(numbers):
    for number in numbers:
        filename = f"image{number}.txt"
        source_path = f"RetestAll/labels2/{filename}"
        destination_path = f"RetestAll/labels3/{filename}"
        if os.path.exists(source_path):
            shutil.move(source_path, destination_path)
            print(f"Moved file {filename}")
        else:
            print(f"File {filename} not found")


if __name__ == "__main__":
    del_numbers = read_file(r"RetestAll\ToLabel\ToRemove.txt")
    move_files(del_numbers)
    # delete_files(del_numbers)
    move_numbers = read_file(r"RetestAll\ToLabel\toLabel.txt")
    # move_files(move_numbers)
    # move_labels(move_numbers)
