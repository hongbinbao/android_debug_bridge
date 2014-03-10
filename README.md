android_debug_bridge
====================

adb related 

=================

### model

    doc: system/core/adb/transports.txt; system/core/adb/OVERVIEW.txt
![github](https://github.com/hongbinbao/android_debug_bridge/blob/master/adb.png?raw=true "github")

### conponment

    1: adb/adb.exe: command-line client sdk/platform-tools/adb
    2: adb server: 
    3: adbd: /sbin/adbd
    4: service
       local service: adbd
       host service:  adb server
    
