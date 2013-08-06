import os
import sys
import platform
import shutil
import inspect

#
#def machine():
#    """Return type of machine."""
#    if os.name == 'nt' and sys.version_info[:2] < (2,7):
#        return os.environ.get("PROCESSOR_ARCHITEW6432", 
#               os.environ.get('PROCESSOR_ARCHITECTURE', ''))
#    else:
#        return platform.machine()
#
#def arch(machine=machine()):
#    """Return bitness of operating system, or None if unknown."""
#    machine2bits = {'AMD64': 64, 'x86_64': 64, 'i386': 32, 'x86': 32}
#    return machine2bits.get(machine, None)
#
#print (os_bits())

from fakebci import *

def create_so():
    base_dir = os.path.dirname(inspect.getabsfile(FakeBCI))
    boosted_bci = os.path.join(base_dir, 'boosted_bci.so')    
    if not os.path.exists(boosted_bci):
        if sys.platform == 'darwin':
            if platform.architecture()[0] == '64bit':
                shutil.copyfile(os.path.join(base_dir, 'boosted_bci_darwin_x86_64.so'), boosted_bci)
            else:
                raise NotImplementedError("32 bit OS X is currently untested")

try:
    from boosted_bci import greet
except:
    print "Platform specific bci files have not been created"
