from setuptools import setup, Extension
from pybind11.setup_helpers import Pybind11Extension, build_ext
import sys
import subprocess

# Retrieve OpenCV configuration
def get_opencv_info():
    try:
        opencv_cflags = subprocess.check_output("pkg-config --cflags opencv4", shell=True).decode().strip()
        opencv_libs = subprocess.check_output("pkg-config --libs opencv4", shell=True).decode().strip()
    except subprocess.CalledProcessError:
        sys.exit("Error: OpenCV not found")

    include_dirs = [flag[2:] for flag in opencv_cflags.split() if flag.startswith("-I")]
    library_dirs = [flag[2:] for flag in opencv_libs.split() if flag.startswith("-L")]
    libraries = [flag[2:] for flag in opencv_libs.split() if flag.startswith("-l")]

    return include_dirs, library_dirs, libraries

opencv_include_dirs, opencv_library_dirs, opencv_libraries = get_opencv_info()

__version__ = "0.0.1"

# Define the extension module
ext_modules = [
    Pybind11Extension(
        "aruco_module",
        ["aruco/aruco.cpp"],
        define_macros=[("VERSION_INFO", __version__)],
        extra_compile_args=['-std=c++20'],
        include_dirs=opencv_include_dirs,
        library_dirs=opencv_library_dirs,
        libraries=opencv_libraries,
    ),
]

setup(
    name="aruco_module",
    version=__version__,
    author="Adam Gaddis",
    author_email="adam@robochargers.io",
    description="A Python binding for Aruco module using pybind11",
    long_description="",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    python_requires=">=3.11",  # Adjust as per your Python version
)
