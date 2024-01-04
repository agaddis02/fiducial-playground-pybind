c++
in the root directory:

`opencv = 4.8.1`
`fmt = 10.2.0`


- `mkdir build`
- `cd build/`
- `make`
- `cd app/`
- move the images from the root directory to `build/app` then run `./fiducial_tests`


python

change to the python-aruco-binding directory:

you still need the 2 libraries for c++ above

- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- `python setup.py build_ext --inplace` && `pip install .`
- `python test.py`
