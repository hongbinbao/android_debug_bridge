#!/usr/bin/python
# -*- coding:utf-8 -*- 

import os, socket
import subprocess
import shlex
#adb = adb()
#adb = adb('/usr/bin/adb')
#adb = adb('sdk/platform-tools/adb')
LOCATION_NOT_FOUND_EXCEPTION = '%s not found.'

def is_executable(exe):
    '''
    return True if program is executable.
    '''
    return os.path.isfile(exe) and os.access(exe, os.X_OK)

def find_exetuable(program):
    '''
    return the absolute path of executable program if the program available.
    else raise Exception.
    '''
    program_path, program_name = os.path.split(program)
    if program_path:
        if is_executable(program):
            return program
    else:
        for path in os.environ['PATH'].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_executable(exe_file):
                return exe_file
    raise Exception(LOCATION_NOT_FOUND_EXCEPTION % program)
    return None

ADB_PORT = 5037

class Error(Exception):
  pass

class AdbError(Error):
  pass

class AdbQuit(Error):
  """Signals that the device connection must quit."""

def start_server():
    adb = find_exetuable('adb')
    cmd = '%s %s' %(adb, 'start-server')
    system_call(cmd)

def kill_server():
    adb = find_exetuable('adb')
    cmd = '%s %s' %(adb, 'kill-server')
    system_call(cmd)

def system_call(cmd):
    with open('abd.log', 'w+') as log:
        process = subprocess.Popen(shlex.split(cmd), stdout=log, stderr=subprocess.STDOUT, close_fds=True)
        process.wait()

class AdbClient(object):
  """Python client for the adb server using socket interface."""

  def __init__(self, exe=None):
    self.__exe = exe
    self.__version = int(self.HostQuery("host:version"), 16)

  @property 
  def version(self):
    return self.__version

  def _Connect(self):
    '''
    connect local adb server
    return the socket instance of connection
    '''
    retries = 3
    while retries:
      try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', ADB_PORT))
      except socket.error:
        start_server()
        retries -= 1
      else:
        return sock
    else:
      raise AdbError('Could not connect to server.')

  def DoCommand(self, sock, cmd):
    '''
    encode the command content size to hex value
    send to adb server
    check the response of adb server
    if response is not OKAY raise exception with the fail message content and close the socket
    '''
    #convert an integer to a hexadecimal string
    #adb protcol [hex size + content]
    #cmd = '000chost:version'
    cmd = "%04x%s" % (len(cmd), cmd)
    sock.sendall(cmd)
    try:
      self._CheckStatus(sock)
    except AdbError:
      sock.close()
      raise

  def Connect(self, cmd):
    sock = self._Connect()
    self.DoCommand(sock, cmd)
    return sock

  def HostQuery(self, cmd):
    sock = self._Connect()
    self.DoCommand(sock, cmd)
    size = int(sock.recv(4), 16)
    print size
    resp = sock.recv(size)
    sock.close()
    print resp
    return resp

  def _CheckStatus(self, sock):
    '''
    get adb server response.
    the first 4 byte of socket is the OKAY or FAIL flag.
    if FAIL the follow 4 bytes in socket is the hex size of fail msg content size.
    if FAIL or other not wanted value then raise exception to caller.
    '''
  	#each request get 4 byte response msg. OKAY OR FAIL
  	#if FAIL . followed by hex size of msg
  	#convert hex string to integer
  	#>>> int('0x10AFCC', 16)
    #1093580
    #>>> hex(1093580)
    #'0x10afcc'
  	#
    stat = sock.recv(4)
    print stat
    if stat == "OKAY":
      return True
    elif stat == "FAIL":
      size = int(sock.recv(4), 16)
      val = sock.recv(size)
      raise AdbError(val)
    else:
      raise AdbError("Bad response: %r" % (stat,))

  def GetDevices(self):
    dm = DeviceManager()
    resp = self.HostQuery("host:devices")
    for n, line in enumerate(resp.splitlines()):
      parts = line.split("\t")
      if self.__version >= 19:
        device = AdbDeviceClient(n+1, parts[0], parts[1],
            self.__version)
      else:
        device = AdbDeviceClient(int(parts[0]), parts[1], parts[2], 
            self.__version)
      dm.Add(device)
    return dm

  def GetDevice(self, identifier=1):
    try:
      return self.GetDevices()[identifier]
    except (KeyError, IndexError):
      raise AdbError("Could not get device with identifier %r." % (identifier,))

  def Kill(self):
    sock = self.Connect("host:kill")
    sock.close()


adb = AdbClient()

print adb.version



##test 
#print find_exetuable('adb')#
#print find_exetuable('/usr/bin/adb')
#print find_exetuable('android-sdk-linux/platform-tools/adb')