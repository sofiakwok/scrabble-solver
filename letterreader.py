# import the necessary packages
from pytesseract import Output
import pytesseract
import argparse
import cv2
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# construct the argument parser and parse the arguments
"""ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image to be OCR'd")
args = vars(ap.parse_args())"""

# load the input image, convert it from BGR to RGB channel ordering,
# and use Tesseract to determine the text orientation
#image = cv2.imread(args["image"])
image = cv2.imread("images/A.png")
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
results = pytesseract.image_to_osd(rgb, output_type=Output.DICT)

# display the orientation information
print("[INFO] detected orientation: {}".format(
	results["orientation"]))
print("[INFO] rotate by {} degrees to correct".format(
	results["rotate"]))
print("[INFO] detected script: {}".format(results["script"]))


