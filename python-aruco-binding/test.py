import cv2
import numpy as np
import time
from typing import Tuple, Callable, List, Dict, Any
import aruco_module as aruconano

# Load images
image_1829px = cv2.imread("image1.jpg")
image_3658px = cv2.imread("image1_2x_res.jpg")
image_1829px_gray = cv2.cvtColor(image_1829px, cv2.COLOR_BGR2GRAY)
image_3658px_gray = cv2.cvtColor(image_3658px, cv2.COLOR_BGR2GRAY)

# OpenCV ArUco dictionary and parameters setup
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
aruco_params = cv2.aruco.DetectorParameters()
aruco_params.adaptiveThreshConstant = 7
aruco_params.adaptiveThreshWinSizeMin = 7
aruco_params.adaptiveThreshWinSizeMax = 7

# Function to detect markers using ArUco v5
def aruco_v5_detect(inputMat: np.ndarray) -> float:
    start_time = time.time()
    dict_ = aruconano.TagDicts.APRILTAG_36h11
    # print(f"type of inputMat: {type(inputMat)}")
    # print(f"type of dict_: {type(dict_)}")
    # mat = aruconano.numpy_to_cvMat(inputMat)
    markers = aruconano.MarkerDetector.detect(inputMat, 10, dict_)
    detectElapsed = (time.time() - start_time) * 1000  # Convert to milliseconds
    return detectElapsed

# Function to run the test suite
def runTestSuite(parallel: bool, hires: bool, detectFunc: Callable[[np.ndarray], float], iters: int = 100) -> float:
    grayMat = image_3658px_gray if hires else image_1829px_gray
    cv2.setNumThreads(-1 if parallel else 0)

    times = [detectFunc(grayMat) for _ in range(iters)]
    # print(f"Times: {times}")

    return float(np.mean(times))

# Function to detect markers using OpenCV ArUco
def opencv_aruco_detect(inputMat: np.ndarray) -> float:
    # Check if the input image has 3 dimensions (i.e., is a color image)
    if inputMat.ndim == 3 and inputMat.shape[2] == 3:
        tmp = cv2.cvtColor(inputMat, cv2.COLOR_BGR2GRAY)
    else:
        tmp = inputMat.copy()

    start_time = time.time()
    _, _, _, = cv2.aruco.ArucoDetector(dictionary=aruco_dict, detectorParams=aruco_params).detectMarkers(tmp)
    detectElapsed = (time.time() - start_time) * 1000  # Convert to milliseconds
    return detectElapsed



# Define tests
testEntries: List[Dict[str, Any]] = [

	{"name":"aruco_v5", "hires":False, "opencv_parallel":False, "func":aruco_v5_detect},
	{"name":"aruco_v5", "hires":True,  "opencv_parallel":False, "func":aruco_v5_detect},
	{"name":"aruco_v5", "hires":False, "opencv_parallel":True,  "func":aruco_v5_detect},
	{"name":"aruco_v5", "hires":True,  "opencv_parallel":True,  "func":aruco_v5_detect},
	{"name":"opencv_aruco", "hires":False, "opencv_parallel":False, "func":opencv_aruco_detect},
	{"name":"opencv_aruco", "hires":True,  "opencv_parallel":False, "func":opencv_aruco_detect},
	{"name":"opencv_aruco", "hires":False, "opencv_parallel":True,  "func":opencv_aruco_detect},
	{"name":"opencv_aruco", "hires":True,  "opencv_parallel":True,  "func":opencv_aruco_detect}
]

# Run tests
for test in testEntries:
    imgSize = (image_3658px.shape[1], image_3658px.shape[0]) if test["hires"] else (image_1829px.shape[1], image_1829px.shape[0])
    print(f"Test - Detector: {test['name']}, Img: {imgSize[0]} x {imgSize[1]} Parallel: {'ON' if test['opencv_parallel'] else 'OFF'}")
    test['time'] = runTestSuite(test['opencv_parallel'], test['hires'], test['func'])
    print(f"Completed test {test['name']}. Mean: {test['time']:.4f}ms")
