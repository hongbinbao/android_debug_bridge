note for logcat
==================

### overriew

![github](https://github.com/hongbinbao/android_debug_bridge/blob/master/log.png?raw=true "github")

### android system and application log
    access node on device file system:
    /dev/log/main
        An Android application includes the android.util.Log class, and uses methods of this class to write messages of different priority into the log.
    
    /dev/log/events
        Event logs messages are created using android.util.EventLog class, which create binary-formatted log messages.
    
    /dev/log/radio
        radio and phone-related information
    
    /dev/log/system
        Many classes in the Android framework utilize the system log to keep their messages separate from (possibly noisy) application log messages. These programs use the android.util.Slog class, with its associated messages.
    
### kernel log
    /proc/kmsg

### buffer size

    test@test-OptiPlex-740-Enhanced:~$ adb logcat -g
    /dev/log/main: ring buffer is 256Kb (255Kb consumed), max entry is 5120b, max payload is 4076b
    /dev/log/system: ring buffer is 256Kb (154Kb consumed), max entry is 5120b, max payload is 4076b
    
    Buffer size is determined by the kernel, found in */drivers/staging/android/logger.c
    Which buffers are used and the size has changed with Android Versions. 
    Android 3.0 and newer also have a system buffer, and all four are 256kb.
    You have to recompile the kernel to change it.
    
### catch /dev/log/system, /dev/log/main to sdcard
    adb logcat -v time -f /sdcard/dev.log -r 1024  -n 0 -d


