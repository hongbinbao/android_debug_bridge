#!/usr/bin/python
# -*- coding:utf-8 -*- 

import subprocess
import threading
import time
import os
import Queue
import shlex
from os.path import exists
from os.path import join
from os.path import splitext
from os.path import dirname

ANDROID_LOG_SHELL = 'adb logcat -v time'
REPORT_TIME_STAMP_FORMAT = '%Y-%m-%d_%H:%M:%S'
PER_LOG_SIZE = 1024*1024*2 #5MB

def _mkdir(path):
    '''
    create directory as path
    '''
    if not exists(path):
        os.makedirs(path)
    return path

class OutputFile(file):

    def __init__(self, filename, mode='w+', maxsize=None):
        self.dirname = dirname(filename)
        self.root, self.ext = splitext(filename)
        self.size = 0
        if maxsize is not None and maxsize < 1:
            raise Exception('value of maxsize should be a positive number')
        self.maxsize = maxsize
        file.__init__(self, self._getfilename(), mode)


    def write(self, text):
        lentext =len(text)
        if self.maxsize is None or self.size+lentext <= self.maxsize:
            file.write(self, text)
            self.size += lentext
        else:
            self.close()
            file.__init__(self, self._getfilename(), self.mode)
            file.write(self, text)
            self.size += lentext

    def writelines(self, lines):
        for line in lines:
            self.write(line)

    def reporttime(self):
        '''
        return time stamp format with REPORT_TIME_STAMP_FORMAT
        '''
        return time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(time.time()))

    def _getfilename(self):
        if not exists(self.dirname): _mkdir(self.dirname)
        return join(self.dirname  ,'%s%s%s' % (self.reporttime(), '.log' ,self.ext))

    def close(self):
        file.close(self)
        self.size = 0


class LogHandler(object):
    def __init__(self, queue=None):
        self.__cache_queue = queue if queue else Queue.Queue()
        self.__logger_proc = None
        self.__cache_thread = None
    
    @property 
    def queue(self):
        return self.__cache_queue

    def start(self):
        self.__logger_proc = subprocess.Popen(shlex.split(ANDROID_LOG_SHELL),\
                                              stdout=subprocess.PIPE,\
                                              close_fds=True,\
                                              preexec_fn=self.check)
        self.__cache_thread = LogCacheWrapper(self.__logger_proc.stdout, self.__cache_queue)
        self.__cache_thread.start()

    def check(self):
        pass

    def available(self):
        if not self.__logger_proc or not self.__cache_thread:
            return False
        return self.__cache_thread.is_alive() and not self.__logger_proc.poll()

    def save(self, path):
        with open(path, 'w+') as f:
            for i in range(self.__cache_queue.qsize()):
               line = self.__cache_queue.get()
               f.write(line)

    def drop(self):
        self.__cache_queue.queue.clear()

class LogCacheWrapper(threading.Thread):
    def __init__(self, fd, queue):
        threading.Thread.__init__(self)
        self.daemon = True
        self.__fd = fd
        self.__queue = queue
        self.__stop = False

    def stop(self):
        self.__stop = True

    def run(self):
        for line in iter(self.__fd.readline, ''):
            self.__queue.put(line)

class LogWriter(threading.Thread):
    def __init__(self, queue, output):
        threading.Thread.__init__(self)
        #self.daemon = True
        self.__stop = False
        self.__queue = queue
        self.__output = output

    def run1(self):
        dirs = _mkdir('catlogs')
        f = join(dirs, '%s%s' % (reporttime(), '.log'))
        fd = open(f, 'w+')
        line = None
        while not self.__stop:
            line = self.__queue.get(block=True)
            if fd.tell() > PER_LOG_SIZE:
                fd.close()
                f = join(dirs, '%s%s' % (reporttime(), '.log'))
                fd = open(f, 'w+')
            else:
                fd.write(line)
        fd.close()

    def run(self):
        line = None
        while True:
            line = self.__queue.get(block=True)
            self.__output.write(line) 

cache_q = Queue.Queue()
outputfile = OutputFile('catlogs/log.txt', 'w+', 1024*1024)

handler = LogHandler(cache_q)
handler.start()
LogWriter(cache_q, outputfile).start()