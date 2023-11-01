import os
import natsort
import difflib

my_data = ['Архыз 0.5л газ', 'Архыз 0.5л негаз', 'Архыз 1.5л газ', 'Архыз 1.5л негаз', 'Архыз 5л негаз',
           'Псыж 0.45л газ', 'Псыж 1л газ', 'Архыз 0,75 л спорт негаз']


def get_stats(folder_path, log_name):
    i = 0
    global my_data
    # Get a list of all text files in the folder
    text_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    text_files = natsort.natsorted(text_files)
    arr = my_data
    log_folder = "logs"
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    log_file_name = "logs/prediction_analyze_" + log_name + ".txt"
    with open(log_file_name, "w") as error_log_predict:
        pass  # Open and immediately close the file to clear its contents
    error_log_predict = open(log_file_name, "w")

    # Process each text file
    for text_file in text_files:
        number_str = text_file[len("image"): -len(".jpg")]
        if i != int(number_str):
            error_log_predict.write(f"image{i}: no detections\n\n")
            i += 1
        with open(os.path.join(folder_path, text_file), 'r') as f:
            error_log_predict.write(f"image{i}:\n")
            info_arr = [0] * len(arr)
            # Read the lines of the text file
            lines = f.readlines()
            for j, line in enumerate(lines):
                first_element = line.split()[0]
                info_arr[int(first_element)] += 1
        result = ""
        for j in range(len(info_arr)):
            result += arr[j] + " - " + str(info_arr[j]) + "\n"
        error_log_predict.write(f"{result}\n")
        i += 1
    error_log_predict.close()


def print_diff(file1, file2, log_name):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        # Read the contents of the files into strings
        file1_contents = f1.read()
        file2_contents = f2.read()

    # Generate the diff
    diff = difflib.ndiff(file1_contents.splitlines(), file2_contents.splitlines())
    log_file_name = "logs/prediction_analyze_" + log_name + ".txt"
    error_log_predict = open(log_file_name, "w")
    # Print the diff
    difference_str = '\n'.join(diff)
    error_log_predict.write(f"{difference_str}")
    print(difference_str)
    error_log_predict.close()

def print_diff2(file1, file2, output_file, f_name1, f_name2):
    output_path = "logs/" + output_file
    with open(file1, "r") as f1, open(file2, "r") as f2, open(output_path, "w") as out:
        for line1, line2 in zip(f1, f2):
            if line1 != line2:
                out.write(line1.strip() + f" ({f_name1} = {line1.strip().split(' ')[-1]}, {f_name2} = {line2.strip().split(' ')[-1]})\n")
            else:
                out.write(line1)
    print(f"Output saved to {output_path}")



if __name__ == "__main__":
    # print("dotrain1000_v1:")
    # get_stats(r"AnalyzeData\low_ark+\labels", "low_ark+")
    print("dotrain1000+_v1:")
    get_stats(r"AnalyzeData\low_arkD+\labels", "low_arkD+")
    print_diff2(r"logs\prediction_analyze_low_ark+.txt", r"logs\prediction_analyze_low_arkD+.txt", "diff_low_ark+-low_arkD+.txt", "low_ark+", "low_arkD+")