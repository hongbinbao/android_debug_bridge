android_debug_bridge
====================

adb related 

=================

### model

    doc: system/core/adb/transports.txt; system/core/adb/OVERVIEW.txt
![github](https://github.com/hongbinbao/android_debug_bridge/blob/master/adb.png?raw=true "github")

### componment

    1: adb/adb.exe:
        executable command-line client
        locate adb server
        send adb command to adb server
        sdk/platform-tools/adb
    2: adb server: 
        running on HOST
        detect device connect/remove
        transfer data between adb/adb.exe and host service and android service.
    3: adbd:
        daemon running on android device/emulator
        connect with adb server
        provide android device service from adb/adb.exe
        /sbin/adbd
    4: service
       local service: adbd
       host service:  adb server
    
