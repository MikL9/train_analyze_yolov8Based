from ultralytics import YOLO
import cv2
import os
import numpy as np
import torch

model = YOLO("models/low_arkhyzF2.pt")
image_folder = "../inference_data/ideal100"  # change this to your folder path
images = []
error_log = open("logs/files_error_log.txt", "a")  # open text file for writing
j=0
num_files = len([f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))])

print("Number of files in the folder:", num_files)

def prepare_files():
    global j
    error_status = False
    j_max = j+50
    # get a sorted list of files in the image folder
    file_list = sorted(os.listdir(image_folder), key=lambda x: int(x.split("image")[1].split(".jpg")[0]))
    for file in file_list:
        if file.endswith(".jpg"):
            try:
                # extract the image number from the file
                # image_num = int(file.split("image")[1].split(".jpg")[0])
                # if j <= image_num <= j_max:
                img_path = os.path.join(image_folder, file)
                # read image with OpenCV
                img = cv2.imread(img_path)
                if img is None:
                    raise IOError  # raise an error if the image is not read successfully
                # convert OpenCV image to numpy array
                img_array = np.array(img)
                # append to images list
                images.append(img_array)
            except (IndexError, ValueError, IOError):
                error_status = True
                print(f"Unable to read image {file}")
                error_log.write(f"Unable to read image {file}\n")

    error_log.close()  # close text file when done
    j = j_max
    if not error_status:
        print("Preparation completed with no errors!")
    else:
        print("errors was saved to files_error_log.txt")


def predict_image():
    results = model.predict(source=images, stream=True, save=True, save_conf=True, conf=0.5, retina_masks=True)
    error_log_predict = open("logs/prediction_error_log.txt", "a")
    for result in results:
        boxes = result.boxes.data
        if boxes.shape[0] == 0:
            error_log_predict.write(f"no detections :{j}:\n")
    error_log_predict.close()
    torch.cuda.empty_cache()


if __name__ == "__main__":
    prepare_files()
    predict_image()