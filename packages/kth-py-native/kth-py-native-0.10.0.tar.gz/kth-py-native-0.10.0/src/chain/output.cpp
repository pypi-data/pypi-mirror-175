#include <kth/py-native/chain/output.h>

#include <kth/capi.h>
#include <kth/py-native/utils.h>

#ifdef __cplusplus
extern "C" {
#endif

// kth_output_t kth_chain_output_construct(uint64_t value, kth_script_t script);
PyObject* kth_py_native_chain_output_construct(PyObject* self, PyObject* args){
    uint64_t py_value;
    PyObject* py_script;

    if ( ! PyArg_ParseTuple(args, "KO", &py_value, &py_script)) {
        return NULL;
    }

    kth_script_t script = (kth_script_t)get_ptr(py_script);

    kth_output_t res = kth_chain_output_construct(py_value, script);
    return to_py_obj(res);
}

// kth_output_t kth_chain_output_factory_from_data(uint8_t* data, uint64_t n);
PyObject* kth_py_native_chain_output_factory_from_data(PyObject* self, PyObject* args){
    char* py_data;
    int py_n;

    if ( ! PyArg_ParseTuple(args, "y#", &py_data, &py_n)) {
        return NULL;
    }

    kth_output_t res = kth_chain_output_factory_from_data((uint8_t*)py_data, py_n);
    return to_py_obj(res);
}

PyObject* kth_py_native_chain_output_is_valid(PyObject* self, PyObject* args){
    PyObject* py_output;

    if ( ! PyArg_ParseTuple(args, "O", &py_output)) {
        return NULL;
    }

    kth_output_t output = (kth_output_t)get_ptr(py_output);
    int res = kth_chain_output_is_valid(output);
    return Py_BuildValue("i", res);
}

PyObject* kth_py_native_chain_output_serialized_size(PyObject* self, PyObject* args){
    PyObject* py_output;
    int py_wire;

    if ( ! PyArg_ParseTuple(args, "Oi", &py_output, &py_wire)) {
        return NULL;
    }

    kth_output_t output = (kth_output_t)get_ptr(py_output);
    uint64_t res = kth_chain_output_serialized_size(output, py_wire);
    return Py_BuildValue("K", res);
}


PyObject* kth_py_native_chain_output_value(PyObject* self, PyObject* args){
    PyObject* py_output;

    if ( ! PyArg_ParseTuple(args, "O", &py_output)) {
        return NULL;
    }

    kth_output_t output = (kth_output_t)get_ptr(py_output);
    uint64_t res = kth_chain_output_value(output);
    return Py_BuildValue("K", res);
}


PyObject* kth_py_native_chain_output_signature_operations(PyObject* self, PyObject* args){
    PyObject* py_output;

    if ( ! PyArg_ParseTuple(args, "O", &py_output)) {
        return NULL;
    }

    kth_output_t output = (kth_output_t)get_ptr(py_output);
    uint64_t res = kth_chain_output_signature_operations(output);
    return Py_BuildValue("K", res);

}

PyObject* kth_py_native_chain_output_destruct(PyObject* self, PyObject* args){
    PyObject* py_output;

    if ( ! PyArg_ParseTuple(args, "O", &py_output)) {
        return NULL;
    }

    kth_output_t output = (kth_output_t)get_ptr(py_output);
    kth_chain_output_destruct(output);
    Py_RETURN_NONE;
}

PyObject* kth_py_native_chain_output_script(PyObject* self, PyObject* args){
    PyObject* py_output;

    if ( ! PyArg_ParseTuple(args, "O", &py_output)) {
        return NULL;
    }

    kth_output_t output = (kth_output_t)get_ptr(py_output);
    kth_script_t script = kth_chain_output_script(output);
    return to_py_obj(script);
}

/*
PyObject* kth_py_native_chain_output_hash(PyObject* self, PyObject* args){
    PyObject* py_output;

    if ( ! PyArg_ParseTuple(args, "O", &py_output)) {
        return NULL;
    }

    kth_output_t output = (kth_output_t)get_ptr(py_output);
     kth_hash_t res = kth_chain_output_hash(output);
    return PyByteArray_FromStringAndSize(res.hash, 32);

}
*/

/*
PyObject* kth_py_native_chain_output_index(PyObject* self, PyObject* args){
    PyObject* py_output;

    if ( ! PyArg_ParseTuple(args, "O", &py_output)) {
        return NULL;
    }

    kth_output_t output = (kth_output_t)get_ptr(py_output);
    uint32_t res = kth_chain_output_index(output);
    return Py_BuildValue("L", res);

}
*/

PyObject* kth_py_native_chain_output_to_data(PyObject* self, PyObject* args) {
    PyObject* py_output;
    int py_wire;

    if ( ! PyArg_ParseTuple(args, "Oi", &py_output, &py_wire)) {
        return NULL;
    }

    kth_output_t output = (kth_output_t)get_ptr(py_output);
    kth_size_t out_n;
    uint8_t* data = (uint8_t*)kth_chain_output_to_data(output, py_wire, &out_n);

    return Py_BuildValue("y#", data, out_n);
}

#ifdef __cplusplus
} //extern "C"
#endif
