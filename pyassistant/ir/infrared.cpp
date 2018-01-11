#include <wiringPi.h>
#include <iostream>
#include <sys/time.h>
#include <vector>
#include <math.h>
#include <unistd.h>
#include <Python.h>
using namespace std;


double getMoment()
{
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return ((double)(tv.tv_sec) * 1000000 + (double)(tv.tv_usec));
}

int getInterval(double t1, double t2)
{
    return (int)(t2-t1);
}

int getTime(int pin,int status,int max_wait)
{
    int count = 0;
    int interval = 10;
    int max = max_wait / interval;
    double start, end;

    start = getMoment();
    while( digitalRead(pin) == status )
    {
        delayMicroseconds(interval);
    	count++;
        //最大継続時間同じ状態が続いたら送信は終了していると判断
    	if(count > max){ break; }
    }
    end = getMoment();

    return getInterval(start, end);
}


void high(int hz,int on_time,int pin)
{
    float unit = (1.0f / (hz)) * 1000000;
    int duty_num = 1;
    int duty_denomi = 3;
    double duty_high = roundf((unit / duty_denomi) * duty_num);
    double duty_low = unit - duty_high;
    // パルス信号に変換して送信
    int count = on_time/unit;
    for(int i=0; i<count; i++)
    {
        digitalWrite(pin, 1); //high
        delayMicroseconds(duty_high);

        digitalWrite(pin, 0); //low
        delayMicroseconds(duty_low);
    }
}

void output(int pin,int hz,int on_time, int off_time)
{
    // 赤外線点灯
    high(hz,on_time,pin);

    // 赤外線消灯
    digitalWrite(pin, 0);
    delayMicroseconds(off_time);
}

vector<vector<int>> scan(int pin,int max_wait)
{
    // 受光モジュールは受光するとLOWになる
    /*
    if(!digitalRead(pin)){
        list data;
        return data;
    }*/
    vector<vector<int>> pulses;
    pinMode(pin, INPUT);
    if(wiringPiSetupGpio() == -1){
        cout<<"error wiringPi setup"<<endl;
        return pulses;
    }
    cout<<"waiting for infra read..."<<endl;
    // 送信が開始されるまで待機
    while( digitalRead(pin) ){}
    cout<<"scanning started!"<<endl;


    int off = 0;
    // 解析開始
    while(1){
        int on = getTime(pin,0,max_wait);
        int off = getTime(pin,1,max_wait);
        cout<<(".");
        vector<int> row = {on,off};

        pulses.push_back(row);
        if(off > max_wait){ break; }
        //最大継続時間同じ状態が続いたら送信は終了していると判断
    }
    cout<<""<<endl;
    cout<<"scanning finished"<<endl;

    return pulses;

}

void send(vector<vector<int>> data,int pin,int repeat,int hz)
{
    pinMode(pin, OUTPUT);
    if(wiringPiSetupGpio() == -1){
        cout<<"error wiringPi setup"<<endl;
        return;
    }
    // 送信（同じ情報をrepeat回送信する)
    for(int j=0; j<repeat; j++)
    {
        cout<<"send data "<<j<<"data size"<<data.size()<<endl;
        for(int i=0; i<data.size(); i++)
        {
            output(pin,hz,data[i][0],data[i][1]);
            cout<<data[i][0]<<" "<<data[i][1]<<endl;
        }
        usleep(50000);
    }
    cout<<"send complete"<<endl;
}

PyObject* vectorToList(const vector<vector<int>> &data) {
  PyObject* listObj = PyList_New( data.size() );
	for (int i = 0; i < data.size(); i++) {
	    vector<int> row = data[i];
	    PyObject* rowObj = PyList_New(row.size());
	    for(int j=0;j<row.size();j++){
	        PyObject *num = PyFloat_FromDouble( data[i][j]);
	        if (!num) {
                Py_DECREF(listObj);
                throw logic_error("Unable to allocate memory for Python list");
            }
            PyList_SET_ITEM(rowObj, j, num);
	    }
		PyList_SET_ITEM(listObj, i, rowObj);
	}
	return listObj;
}

vector<vector<int>> listToVector(PyObject* incoming) {
	vector<vector<int>> data;

    if (PyList_Check(incoming)) {
        for(Py_ssize_t i = 0; i < PyList_Size(incoming); i++) {
            vector<int> row;
            PyObject *row_val = PyList_GetItem(incoming, i);
            for(Py_ssize_t j = 0; j < PyList_Size(row_val); j++) {
                PyObject *value = PyList_GetItem(row_val, j);
                row.push_back( PyFloat_AsDouble(value) );
            }
            data.push_back(row);
        }
    } else {
        throw logic_error("Passed PyObject pointer was not a list or tuple!");
    }

	return data;
}


PyObject* infrared_scan(PyObject* self, PyObject* args){
    int pin;
    int max_wait;
    if (!PyArg_ParseTuple(args, "ii", &pin, &max_wait))
		return NULL;
    vector<vector<int>> data = scan(pin,max_wait);
    return vectorToList(data);
}

PyObject* infrared_send(PyObject* self, PyObject* args){
    int pin;
    int repeat;
    int hz;
    PyObject* data;
    if (!PyArg_ParseTuple(args, "Oiii",&data, &pin, &repeat,&hz))
		return NULL;
    vector<vector<int>> data_vec = listToVector(data);
    send(data_vec,pin,repeat,hz);
    return Py_BuildValue("");
}

static PyMethodDef methods[] = {
	{"scan", (PyCFunction)infrared_scan, METH_VARARGS},
	{"send", (PyCFunction)infrared_send, METH_VARARGS},
    {NULL},
};

static PyModuleDef infrared_module = {
    PyModuleDef_HEAD_INIT,
    "superfastcode",                        // Module name as Python sees it
    "Provides some functions, but faster",  // Module description
    0,
    methods                   // Structure that defines the methods
};

PyMODINIT_FUNC PyInit_infrared() {
    return PyModule_Create(&infrared_module);
}


int main(){
    vector<vector<int>> data = scan(29,40000);
    cout<<data.size()<<endl;

    return 0;
}