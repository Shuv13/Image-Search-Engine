# import the necessary packages
from pyimagesearch.colordescriptor import ColorDescriptor
from pyimagesearch.searcher import Searcher
import argparse
import cv2
import os

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--index", required=True,
    help="Path to where the computed index will be stored")
ap.add_argument("-q", "--query", required=True,
    help="Path to the query image")
ap.add_argument("-r", "--result-path", required=True,
    help="Path to the result path")
args = vars(ap.parse_args())

# initialize the image descriptor
cd = ColorDescriptor((8, 12, 3))

# load the query image and check
query = cv2.imread(args["query"])
if query is None:
    raise ValueError(f"[ERROR] Cannot load query image: {args['query']}")

# describe the query
features = cd.describe(query)

# perform the search
searcher = Searcher(args["index"])
results = searcher.search(features)

# show the query image first
cv2.imshow("Query", query)
cv2.waitKey(0)

# loop over the results
for (score, resultID) in results:
    resultPath = os.path.join(args["result_path"], resultID)
    result = cv2.imread(resultPath)

    if result is None:
        print(f"[WARNING] Could not load result image: {resultPath}")
        continue

    cv2.imshow("Result", result)
    cv2.waitKey(0)
