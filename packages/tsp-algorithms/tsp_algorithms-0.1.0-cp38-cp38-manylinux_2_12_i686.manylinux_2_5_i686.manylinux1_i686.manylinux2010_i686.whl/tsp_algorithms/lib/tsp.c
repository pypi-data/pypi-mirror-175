#include <stdlib.h>
#include <Python.h>

#include "./include/nearest_neighbors.h"


// Wrap the nearest neighbor algorithm in a python function
static PyObject *method_nearest_neighbors(PyObject *self, PyObject *args) {

    /* Parse arguments */
    PyObject *cost_matrix;
    PyObject *row_cost_matrix;
    PyObject *cost;
    Py_ssize_t n;
    int i, j;

    if (!PyArg_ParseTuple(args, "O!", &PyList_Type, &cost_matrix)) {
        PyErr_SetString(PyExc_TypeError, "parameter must be a list.");
        return NULL;
    }
    n = PyList_Size(cost_matrix);

    // Read a list of list of floats
    float **cost_matrix_c = (float **)malloc(n * sizeof(float *));
    for (i = 0; i < n; i++) {
        row_cost_matrix = PyList_GetItem(cost_matrix, i);
        cost_matrix_c[i] = (float *)malloc(n * sizeof(float));
        for (j = 0; j < n; j++) {
            cost = PyList_GetItem(row_cost_matrix, j);
            if(!PyFloat_Check(cost)) {
                PyErr_SetString(PyExc_TypeError, "list items must be float.");
                return NULL;
            }
            cost_matrix_c[i][j] = PyFloat_AsDouble(cost);
        }
    }

    /* Call the C function */
    int *route = nearest_neighbors(cost_matrix_c, n);

    /* Convert the C array to a Python list */
    PyObject *py_route = PyList_New(n);
    for (i=0; i<n; i++) {
        PyList_SetItem(py_route, i, PyLong_FromLong(route[i]));
    }

    return py_route;
};



static PyMethodDef TSPMethods[] = {
    {"nn", method_nearest_neighbors, METH_VARARGS, "Python interface for calculating Nearest Neighbours solution to the TSP problem"},
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef tspmodule = {
    PyModuleDef_HEAD_INIT,
    "ctsp",
    "Python interface for calculating TSP solutions as a C library function",
    -1,
    TSPMethods
};

PyMODINIT_FUNC PyInit_ctsp(void) {
    return PyModule_Create(&tspmodule);
}