#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <opencv2/opencv.hpp>

namespace pybind11 { namespace detail {

    template <> struct type_caster<cv::Mat> {
    public:
        PYBIND11_TYPE_CASTER(cv::Mat, _("numpy.ndarray"));

        // Convert cv::Mat to Python
        static handle cast(const cv::Mat &m, return_value_policy, handle defval) {
            std::string format = pybind11::format_descriptor<unsigned char>::format();
            if (m.channels() == 3) {
                format = "BGR";
            }
            // or handle other number of channels

            size_t H = m.rows;
            size_t W = m.cols;
            size_t C = m.channels();

            std::vector<size_t> shape;
            if (C == 1) {
                shape = {H, W}; // Grayscale image
            } else {
                shape = {H, W, C}; // Color image
            }

            std::vector<size_t> strides = {sizeof(unsigned char) * W * C, sizeof(unsigned char) * C, sizeof(unsigned char)};

            return pybind11::array(pybind11::buffer_info(
                m.data,                               /* Pointer to buffer */
                sizeof(unsigned char),                /* Size of one scalar */
                format,                               /* Python struct-style format descriptor */
                C == 1 ? 2 : 3,                       /* Number of dimensions */
                shape,                                /* Buffer dimensions */
                strides                               /* Strides (in bytes) for each index */
            )).release();
        }

        // Conversion from numpy to cv::Mat
        bool load(handle src, bool) {
            array b = reinterpret_borrow<array>(src);
            buffer_info info = b.request();

            int ndims = info.ndim;
            if (ndims != 2 && ndims != 3) {
                throw std::runtime_error("Number of dimensions must be 2 or 3");
            }

            int dtype;
            if (info.format == format_descriptor<uint8_t>::format()) {
                dtype = CV_8U;
            } else {
                throw std::runtime_error("Unsupported data type");
            }

            int rows = info.shape[0];
            int cols = info.shape[1];
            value = cv::Mat(rows, cols, dtype, info.ptr);
            return true;
        }
    };

}} // namespace pybind11::detail
