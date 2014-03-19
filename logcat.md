logcat
==================

### overriew

    doc: system/core/adb/transports.txt; system/core/adb/OVERVIEW.txt
![github](https://github.com/hongbinbao/android_debug_bridge/blob/master/adb.png?raw=true "github")

### android log

    The logging system consists of:
    a kernel driver and kernel buffers for storing log messages
    C, C++ and Java classes for making log entries and for accessing the log messages
    a standalone program for viewing log messages (logcat)
    ability to view and filter the log messages from the host machine (via eclipse or ddms)

### ring buffer

    test@test-OptiPlex-740-Enhanced:~$ adb logcat -g
    /dev/log/main: ring buffer is 256Kb (255Kb consumed), max entry is 5120b, max payload is 4076b
    /dev/log/system: ring buffer is 256Kb (154Kb consumed), max entry is 5120b, max payload is 4076b
    
    Buffer size is determined by the kernel, found in */drivers/staging/android/logger.c
    Which buffers are used and the size has changed with Android Versions. 
    Android 3.0 and newer also have a system buffer, and all four are 256kb.
    You have to recompile the kernel to change it.
    
### catch /dev/log/system, /dev/log/main
    adb logcat -v time -f /sdcard/dev.log -r 1024  -n 0 -d

### /dev/log
    root@android:/dev/log # ls
    events
    ksystem
    main
    radio
    system
