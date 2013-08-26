from distutils.core import setup
import os
import shutil

packages = ['unlock', 
            'unlock.context', 'unlock.context.test',
            'unlock.controller', 'unlock.controller.test', 
            'unlock.model', 'unlock.model.test',
            'unlock.neural', 'unlock.neural.acquire', 'unlock.neural.classify', 
            'unlock.util', 'unlock.util.test',
            'unlock.view', 'unlock.view.test']

package_data = {
                'unlock' : ['conf.json', 'README.md'],
                'unlock.controller' : ['resource/analyzer.jpg', 'resource/Arrow.png', 'resource/ArrowSel.png', 'resource/emg-100x100.jpg', 'resource/emg.jpg', 'resource/IRCodes.txt', 'resource/LazerToggle.png', 'resource/LazerToggleS.png', 'resource/rsz_analyzer.jpg', 'resource/scope.png', 'resource/tv.png'],
                'unlock.context.test' : ['app-ctx.xml'], 
                 'unlock.model' : [],
# win-x86 libs find acquire-c++/boost/win-x86/lib | grep -v -e lib$  -e gd | sed s/^/\'/ | sed s/$/\',/
                'unlock.neural' : ['acquire-c++/boost/win-x86/lib/boost_atomic-vc110-mt-1_54.dll',
                            'acquire-c++/boost/win-x86/lib/boost_chrono-vc110-mt-1_54.dll',
                            'acquire-c++/boost/win-x86/lib/boost_context-vc110-mt-1_54.dll',
                            'acquire-c++/boost/win-x86/lib/boost_date_time-vc110-mt-1_54.dll',
                            'acquire-c++/boost/win-x86/lib/boost_filesystem-vc110-mt-1_54.dll',
                            'acquire-c++/boost/win-x86/lib/boost_graph-vc110-mt-1_54.dll',
                            'acquire-c++/boost/win-x86/lib/boost_iostreams-vc110-mt-1_54.dll',
                            'acquire-c++/boost/win-x86/lib/boost_locale-vc110-mt-1_54.dll',
                            'acquire-c++/boost/win-x86/lib/boost_log-vc110-mt-1_54.dll',
                            'acquire-c++/boost/win-x86/lib/boost_log_setup-vc110-mt-1_54.dll',
                            'acquire-c++/boost/win-x86/lib/boost_math_c99-vc110-mt-1_54.dll',
                            'acquire-c++/boost/win-x86/lib/boost_math_c99f-vc110-mt-1_54.dll',
                            'acquire-c++/boost/win-x86/lib/boost_math_c99l-vc110-mt-1_54.dll',
                            'acquire-c++/boost/win-x86/lib/boost_math_tr1-vc110-mt-1_54.dll',
                            'acquire-c++/boost/win-x86/lib/boost_math_tr1f-vc110-mt-1_54.dll',
                            'acquire-c++/boost/win-x86/lib/boost_math_tr1l-vc110-mt-1_54.dll',
                            'acquire-c++/boost/win-x86/lib/boost_prg_exec_monitor-vc110-mt-1_54.dll',
                            'acquire-c++/boost/win-x86/lib/boost_program_options-vc110-mt-1_54.dll',
                            'acquire-c++/boost/win-x86/lib/boost_python-vc110-mt-1_54.dll',
                            'acquire-c++/boost/win-x86/lib/boost_random-vc110-mt-1_54.dll',
                            'acquire-c++/boost/win-x86/lib/boost_regex-vc110-mt-1_54.dll',
                            'acquire-c++/boost/win-x86/lib/boost_serialization-vc110-mt-1_54.dll',
                            'acquire-c++/boost/win-x86/lib/boost_signals-vc110-mt-1_54.dll',
                            'acquire-c++/boost/win-x86/lib/boost_system-vc110-mt-1_54.dll',
                            'acquire-c++/boost/win-x86/lib/boost_thread-vc110-mt-1_54.dll',
                            'acquire-c++/boost/win-x86/lib/boost_timer-vc110-mt-1_54.dll',
                            'acquire-c++/boost/win-x86/lib/boost_unit_test_framework-vc110-mt-1_54.dll',
                            'acquire-c++/boost/win-x86/lib/boost_wave-vc110-mt-1_54.dll',
                            'acquire-c++/boost/win-x86/lib/boost_wserialization-vc110-mt-1_54.dll',
                            'acquire-c++/boost/win-x86/lib/neuralsignal-unit-tests.exe',
                            'acquire-c++/boost/win-x86/lib/neuralsignal-unit-tests.exp',
                            'acquire-c++/boost/win-x86/lib/neuralsignal.pyd',
                            'acquire-c++/boost/win-x86/lib/neuralsignal_win_x86.dll',
# mac os x libs find acquire-c++/boost/macosx-x86-64/lib | grep -v -e lib$  -e gd | sed s/^/\'/ | sed s/$/\',/ 
                            'acquire-c++/boost/macosx-x86-64/lib/libboost_prg_exec_monitor.a',
                            'acquire-c++/boost/macosx-x86-64/lib/libboost_python.a',
                            'acquire-c++/boost/macosx-x86-64/lib/libboost_system.a',
                            'acquire-c++/boost/macosx-x86-64/lib/libboost_test_exec_monitor.a',
                            'acquire-c++/boost/macosx-x86-64/lib/libboost_thread.a',
                            'acquire-c++/boost/macosx-x86-64/lib/libboost_unit_test_framework.a',
                            'acquire-c++/boost/macosx-x86-64/lib/neuralsignal_darwin_x86_64.so'],
                 'unlock.view' : ['bell-ring-01.mp3', 'unlock.png']}

setup(name='unlock', version='0.3.7', packages=packages, package_data=package_data,
      author='James Percent', author_email='james@shift5.net')
