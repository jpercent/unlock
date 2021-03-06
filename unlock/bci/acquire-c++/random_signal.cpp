// Copyright (c) James Percent and Unlock contributors.
// All rights reserved.
// Redistribution and use in source and binary forms, with or without modification,
// are permitted provided that the following conditions are met:
//
//    1. Redistributions of source code must retain the above copyright notice,
//       this list of conditions and the following disclaimer.
//    
//    2. Redistributions in binary form must reproduce the above copyright
//       notice, this list of conditions and the following disclaimer in the
//       documentation and/or other materials provided with the distribution.
//
//    3. Neither the name of Unlock nor the names of its contributors may be used
//       to endorse or promote products derived from this software without
//       specific prior written permission.

// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
// ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
// WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
// DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
// ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
// (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
// LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
// ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
// SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#include "unlock_signal.hpp"
#include "RandomSignal.hpp"

using namespace boost::python;

PythonSignal* create_random_signal(ITimer* pTimer) {
  ISignal* pSignal = new RandomSignal();
  PythonSignal* pPythonSignal = new PythonSignal(pSignal, pTimer);
  return pPythonSignal;  
}

ITimer* create_timer() {
  ITimer* pTimer = new WinTimer();
  pTimer->start();
  return pTimer;
}

BOOST_PYTHON_MODULE(random_signal)
{
  class_<std::vector<int32_t> >("int32_vector")
        .def(vector_indexing_suite<std::vector<int32_t> >() );

  def("create_timer", create_timer, return_value_policy<manage_new_object>());
  def("create_random_signal", create_random_signal, return_value_policy<manage_new_object>());

  class_<TimerPythonWrap, boost::noncopyable>("ITimer", no_init)
    .def("start", pure_virtual(&ITimer::start))
    .def("elapsedCycles", pure_virtual(&ITimer::elapsedCycles))
    .def("elapsedMilliSecs", pure_virtual(&ITimer::elapsedMilliSecs))
    .def("elapsedMicroSecs", pure_virtual(&ITimer::elapsedMicroSecs))
    .def("getFrequency", pure_virtual(&ITimer::getFrequency))
    .def("getStartValue", pure_virtual(&ITimer::getStartValue))
    ;

  class_<PythonSignal>("PythonSignal", init<ISignal*, ITimer*>())
    .def("open", &PythonSignal::open)
    .def("init", &PythonSignal::init)
    .def("channels", &PythonSignal::channels)
    .def("start", &PythonSignal::start)
    .def("acquire", &PythonSignal::acquire)
    .def("getdata", &PythonSignal::getdata)
    .def("elapsedMicroSecs", &PythonSignal::elapsedMicroSecs)
    .def("timestamp", &PythonSignal::timestamp)
    .def("stop", &PythonSignal::stop)
    .def("close", &PythonSignal::close)
    ;

}

