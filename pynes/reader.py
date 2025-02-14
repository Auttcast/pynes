import os, sys
from typing import Iterable
from .common import *
import msvcrt

def create_reader(file_descriptor_id:int=None, nix_max_read_buffer=1024):
  if file_descriptor_id is None: file_descriptor_id = sys.stdin.fileno()

  #NOTES
  #msvcrt.get_osfhandle affects sys.stdin INDIRECTLY
  #msvcrt.get_osfhandle does not working within closure
  r = os.fdopen(file_descriptor_id, mode='r') if not IS_WINDOWS else msvcrt.get_osfhandle(STDIN)

  def nix_read_factory():
    buffArr = bytearray(nix_max_read_buffer)
    buffArrCont = [buffArr]

    def readlines() -> Iterable:
      if r.readable():
        while True:

          bytes_read = os.readv(r.fileno(), buffArrCont)
          line = buffArr[:bytes_read].decode()
          if bytes_read == 0: break
          for l in line.strip().split(ENV_NL):
            yield l

    return readlines

  def win_read_factory():
    
    def readlines() -> Iterable:
      for line in sys.stdin:
        yield line

    return readlines

  if IS_WINDOWS:
    return win_read_factory()
  else:
    return nix_read_factory()