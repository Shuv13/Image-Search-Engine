# import the necessary packages
from pyimagesearch.colordescriptor import ColorDescriptor
import argparse
import glob
import cv2
import os

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True,
    help="Path to the directory that contains the images to be indexed")
ap.add_argument("-i", "--index", required=True,
    help="Path to where the computed index will be stored")
args = vars(ap.parse_args())

# initialize the color descriptor
cd = ColorDescriptor((8, 12, 3))

# open the output index file for writing
with open(args["index"], "w") as output:
    # use glob to grab all image paths (jpg, jpeg, png, etc.)
    imagePaths = glob.glob(os.path.join(args["dataset"], "*.*"))

    for imagePath in imagePaths:
        # extract the image ID (filename only)
        imageID = os.path.basename(imagePath)

        # load the image
        image = cv2.imread(imagePath)
        if image is None:
            print(f"[WARNING] Could not read {imagePath}, skipping...")
            continue

        # describe the image
        features = cd.describe(image)

        # write the features to file
        features = [str(f) for f in features]
        output.write("{},{}\n".format(imageID, ",".join(features)))
