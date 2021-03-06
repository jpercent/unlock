// Copyright (c) Giang Nguyen, James Percent and Unlock contributors.
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

package testutil

import (
    "testing"
    "path/filepath"
    "os"
    "npl/bu/edu/util"
)
    
func Setup(t *testing.T) string {
    testDir,_ := filepath.Abs("./test")
    testFile,_ := filepath.Abs(testDir+"/testfile")

    // Delete unwanted files if exists
    isExist,err := util.CheckFileExists(testDir)
    if err != nil {
        t.Error(err)
    }
    if (isExist) {
        err = os.RemoveAll(testDir)
        if err != nil {
            t.Error(err)
        }
    }    
    err = os.Mkdir(testDir, 0755)
    if err != nil {
        t.Error(err)
    }
    
    return testFile
}

func Teardown(t *testing.T) {
    // Clean up test files
    testDir,_ := filepath.Abs("./test")
    err := os.RemoveAll(testDir)
    if err != nil {
        t.Error(err)
    }
}