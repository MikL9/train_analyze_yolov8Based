import os


def validate(folder_path):
    # Get a list of all text files in the folder
    text_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    arr = [False] * 18

    # Process each text file
    for text_file in text_files:
        with open(os.path.join(folder_path, text_file), 'r') as f:
            # Read the lines of the text file
            lines = f.readlines()
            replace = False
            for i, line in enumerate(lines):
                first_element = line.split()[0]
                arr[int(first_element)] = True
                if line.strip().split()[0] == '5':
                    print(text_file)
                    # replace = True
                    # lines[i] = '7' + line.strip()[2:] + '\n'

        # if replace:
        #     with open(os.path.join(folder_path, text_file), 'w') as f:
        #         f.writelines(lines)

    for i, val in enumerate(arr):
        print(f"{i} - {val}")


if __name__ == "__main__":
    # print("train:")
    # validate("refactorLabels/train")
    # print("valid:")
    # validate("refactorLabels/valid")
    validate(r"C:\Users\1070PC\PycharmProjects\datasets\pothole_dataset_v8\train\labels")
