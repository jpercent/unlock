
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

#ifndef PYTHON_SIGNAL_HPP
#define PYTHON_SIGNAL_HPP

#include <boost/python.hpp>
#include <vector>
#include <stdint.h>
#include <cstddef>
#include <iostream>
#include <fstream>


#include "Portability.hpp"
#include "ISignal.hpp"
#include "ITimer.hpp"

class DllExport PythonSignal
{
 public:
  PythonSignal(ISignal* pSignal, ITimer* pTimer);
  virtual ~PythonSignal();
  bool open(boost::python::list mac);
  bool init(size_t channels);
  size_t channels();
  bool start();
  size_t acquire();
  std::vector<int32_t> getdata(size_t samples);
  uint32_t elapsedMicroSecs();
  uint64_t timestamp();
  bool stop();
  bool close();
private:
    ISignal* mpSignal;
    ITimer* mpTimer;
    std::ofstream mReturnedDataLog;    
};

#endif