#include <Python.h>

static unsigned int _accumulate(unsigned int n)
{
  unsigned int sum = 0;
  unsigned int i = 0;

  for(; i <= n; i++)
    sum += i;

  return sum;
}

static PyObject *accumulate(PyObject* self, PyObject* args)
{
  unsigned int n = 0;

  // 类型解析参考 https://docs.python.org/3/c-api/arg.html#c.PyArg_ParseTuple
  if(!PyArg_ParseTuple(args, "i", &n))
    return NULL;

  return Py_BuildValue("i", _accumulate(n));
}

static PyMethodDef accuMethods[] =
{
  {"accumulate", accumulate, METH_VARARGS, "Calculate the accumulation of n"},
  {NULL, NULL, 0, NULL}

};

static PyModuleDef accuModule =
{
  PyModuleDef_HEAD_INIT,
  "accuModule",                   // module name
  "accumulate module description",// module description
  -1,
  accuMethods
};


// 仅有的非 static 函数，对外暴露模块接口，PyInit_name 必须和模块名相同
// only one non-static function
PyMODINIT_FUNC PyInit_accuModule(void)
{
  return PyModule_Create(&accuModule);
}

