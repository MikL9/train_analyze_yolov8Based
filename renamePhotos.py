import os

i = 0
j = 0


def rename(folder_path):
    global i
    prev_filename = ""
    for filename in os.listdir(folder_path):
        base_name, extension = os.path.splitext(filename)
        # if prev_filename != base_name:
        #     i += 1
        prev_filename = base_name
        new_filename = f'image{i}.{filename.split(".")[-1]}'
        print(new_filename)
        os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))
        i += 1


def renameToPredict(folder_path):
    global j
    for filename in os.listdir(folder_path):
        new_filename = f'image{i}.{filename.split(".")[-1]}'
        os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))
        j += 1


if __name__ == "__main__":
    rename(r"C:\Users\1070PC\PycharmProjects\ultralytics\inference_data\ice1")
    # print("train:")
    # rename(r"C:\Users\1070PC\PycharmProjects\datasets\pothole_dataset_v8\train\refactor")
    # print("valid:")
    # rename(r"C:\Users\1070PC\PycharmProjects\datasets\pothole_dataset_v8\valid\refactor")
