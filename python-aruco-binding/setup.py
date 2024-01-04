import sys
import subprocess
import os

from setuptools import setup, Extension, Command
from setuptools.command.build_py import build_py
from typing import List, Tuple
from pybind11.setup_helpers import Pybind11Extension, build_ext

# Retrieve OpenCV configuration
def get_opencv_info() -> Tuple[List[str], List[str], List[str]]:
    try:
        opencv_cflags = subprocess.check_output("pkg-config --cflags opencv4", shell=True).decode().strip()
        opencv_libs = subprocess.check_output("pkg-config --libs opencv4", shell=True).decode().strip()
    except subprocess.CalledProcessError:
        sys.exit("Error: OpenCV not found")

    include_dirs = [flag[2:] for flag in opencv_cflags.split() if flag.startswith("-I")]
    library_dirs = [flag[2:] for flag in opencv_libs.split() if flag.startswith("-L")]
    libraries = [flag[2:] for flag in opencv_libs.split() if flag.startswith("-l")]

    return include_dirs, library_dirs, libraries

class GenerateStub(Command):
    description = "Generate Python stub file for autocomplete"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        module_name = "aruco_module"
        subprocess.check_call(['stubgen', '-m', module_name])
        # Move the generated .pyi file to the right location if needed
        os.rename(os.path.join("out", f"{module_name}.pyi"), f"{module_name}.pyi",)

class CustomBuildExt(build_ext):
    def run(self):
        build_ext.run(self)  # First, run the original build_ext command
        self.run_command("generate_stub")  # Then, generate the .pyi stub file

opencv_include_dirs, opencv_library_dirs, opencv_libraries = get_opencv_info()

__version__ = "1.0.0"

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
    cmdclass={
        "build_ext": CustomBuildExt,
        "generate_stub": GenerateStub,
    },
    zip_safe=False,
    python_requires=">=3.11",  # Adjust as per your Python version
)
