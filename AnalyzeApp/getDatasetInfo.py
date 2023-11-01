import os
import tkinter as tk
from tkinter import filedialog, messagebox
import re
extended_info = []

def validate_dataset(folder_path):
    labels = get_labels(folder_path + "/labels.txt")
    result_dict_t = validate(labels, folder_path + "/train/labels")
    result_dict_v = validate(labels, folder_path + "/valid/labels")

    return result_dict_t, result_dict_v

def get_labels(file_path):
    label_array = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            label_array.append(line.strip())

    return label_array

def validate(labels, folder_path):
    global extended_info
    text_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    arr = [0] * len(labels)
    result_dict = {}
    extended_arr = [[] for _ in range(len(labels))]

    for text_file in text_files:
        with open(os.path.join(folder_path, text_file), 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                first_element = line.split()[0]
                arr[int(first_element)] += 1
                if text_file not in extended_arr[int(first_element)]:
                    extended_arr[int(first_element)].append(text_file)

    for i in range(len(labels)):
        result_dict[labels[i]] = arr[i]

    extended_res = {}
    for i, label in enumerate(labels):
        extended_res[label] = extended_arr[i]
    extended_info.append(extended_res)

    return result_dict


def browse_button():
    global input_path
    input_path = filedialog.askdirectory()
    path_label.config(text="Selected Folder: " + input_path)

def show_result():
    global extended_info
    try:
        result_dict_t, result_dict_v = validate_dataset(input_path)

        result_t = "\n".join([f"{key} = {value}" for key, value in result_dict_t.items()])
        result_v = "\n".join([f"{key} = {value}" for key, value in result_dict_v.items()])

        messagebox.showinfo("Results", f"Result_dict_t:\n{result_t}\n\nResult_dict_v:\n{result_v}")

        #SAVE STATS TO FILE
        folder_name = os.path.basename(os.path.normpath(input_path))
        output_file = folder_name + ".txt"
        with open(output_file, "w") as file:
            file.write("Result_Train:\n")
            for key, value in result_dict_t.items():
                file.write(f"{key} = {value}\n")

            file.write("\nResult_Valid:\n")
            for key, value in result_dict_v.items():
                file.write(f"{key} = {value}\n")

        messagebox.showinfo("Output", f"Output saved to {output_file}")

        #SAVE EXTENDED STATS TO FILE
        output_file_extended = folder_name + "_extendedStats.txt"
        with open(output_file_extended, "w") as file:
            file.write("Result_Train:\n\n")
            for key, value in extended_info[0].items():
                file.write(f"{key} = {value}\n\n")

            file.write("\nResult_Valid:\n\n")
            for key, value in extended_info[1].items():
                file.write(f"{key} = {value}\n\n")

        messagebox.showinfo("Output_EXTENDED", f"Output extended stats saved to {output_file_extended}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def rename(refactor = False):
    try:
        i = 0
        if refactor:
            max_img = find_max_number_in_filenames()
            i = max_img + 1
        img_name = "image"
        pattern = r'image(\d+)\.jpg'

        for filename in os.listdir(input_path):
            if not re.match(pattern, filename):
                new_filename = f'{img_name}{i}.{filename.split(".")[-1]}'
                os.rename(os.path.join(input_path, filename), os.path.join(input_path, new_filename))
                i += 1

        if refactor:
            messagebox.showinfo("Rename", f"Reset done in {input_path}")
        else:
            messagebox.showinfo("Rename", f"Rename done in {input_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def find_max_number_in_filenames():
    max_img = None
    pattern = r'image(\d+)\.jpg'

    for filename in os.listdir(input_path):
        match = re.match(pattern, filename)
        if match:
            current_number = int(match.group(1))
            if max_img is None or current_number > max_img:
                max_img = current_number

    return max_img

def confirm_rename(refactor = False):
    result = messagebox.askyesno("Confirmation", "Are you sure you want to rename the files?")
    if result:
        if refactor:
            rename(True)
        else:
            rename()

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Application")
    window.minsize(width=400, height=200)

    title_label = tk.Label(window,
                           text="Выберите папку с датасетом, включающую в себя файл labels.txt, папку train/lables и valid/labels")
    title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    browse_button = tk.Button(window, text="Browse", command=browse_button)
    browse_button.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)

    path_label = tk.Label(window, text="Selected Folder: ")
    path_label.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

    show_result_button = tk.Button(window, text="Show Result", command=show_result)
    show_result_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    rename_button = tk.Button(window, text="Rename files(start)", command=confirm_rename)
    rename_button.grid(row=3, column=0, padx=10, pady=10)

    reset_button = tk.Button(window, text="Reset files(add)", command=lambda: confirm_rename(True))
    reset_button.grid(row=3, column=1, padx=10, pady=10)

    window.mainloop()


