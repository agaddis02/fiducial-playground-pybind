#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include <pybind11/stl_bind.h>
#include <pybind11/complex.h>
#include <pybind11/functional.h>
#include <pybind11/operators.h>
#include "aruco_nano.h"
#include "span_type_caster.h"
#include "mat_type_caster.h"
#include <opencv2/opencv.hpp>

namespace py = pybind11;

cv::Mat numpy_to_cvMat(py::array_t<unsigned char> input) {
    py::buffer_info buf = input.request();

    if (buf.ndim != 2 && buf.ndim != 3) {
        throw std::runtime_error("NumPy array must be either 2D or 3D");
    }

    int rows = static_cast<int>(buf.shape[0]);
    int cols = static_cast<int>(buf.shape[1]);
    int channels = (buf.ndim == 3) ? static_cast<int>(buf.shape[2]) : 1;

    // Assuming the input is an 8-bit unsigned char array
    return cv::Mat(rows, cols, CV_MAKETYPE(CV_8U, channels), buf.ptr);
}

PYBIND11_MODULE(aruco_module, m) {
    m.doc() = "pybind11 wrapper for the ArucoNano library";

    // Binding for std::vector<cv::Point2f>
    // std::bind_vector<std::vector<cv::Point2f>>(m, "VectorPoint2f");
        // Register the custom span type caster

    py::bind_vector<std::vector<cv::Point2f>>(m, "VectorPoint2f");

    // Register the custom span type caster as before
    py::class_<std::span<uint8_t, std::dynamic_extent>>(m, "SpanUInt8Dynamic");
    py::class_<std::span<const uint8_t, std::dynamic_extent>>(m, "SpanConstUInt8Dynamic");
    py::class_<cv::Mat>(m, "CvMat");

    m.def("numpy_to_cvMat", &numpy_to_cvMat, "Convert a NumPy array to cv::Mat");
    // Binding for the TagDicts class
    py::class_<aruconano::TagDicts>(m, "TagDicts")
        .def_readonly_static("APRILTAG_36h11", &aruconano::TagDicts::APRILTAG_36h11)
        .def_readonly_static("ARUCO_MIP_36h12", &aruconano::TagDicts::ARUCO_MIP_36h12);

    // Binding for the Marker class
    py::class_<aruconano::Marker>(m, "Marker")
        .def(py::init<>())
        .def_readwrite("id", &aruconano::Marker::id)
        .def("draw", &aruconano::Marker::draw)
        .def("estimatePose", &aruconano::Marker::estimatePose);

    // Binding for the MarkerDetector class
    py::class_<aruconano::MarkerDetector>(m, "MarkerDetector")
        .def_static("detect", &aruconano::MarkerDetector::detect);
        // .def_static("internal_detect", &aruconano::MarkerDetector::internalDetect)
        // .def_static("looksLikeProcessMarker", &aruconano::MarkerDetector::looksLikeProcessMarker)
        // .def_static("linearSampleImage", &aruconano::MarkerDetector::linearSampleImage)
        // .def_static("findMarkerId", &aruconano::MarkerDetector::findMarkerId)
        // .def_static("sideLengthOfMarker", &aruconano::MarkerDetector::sideLengthOfMarker);

    
}
