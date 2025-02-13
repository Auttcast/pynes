import os, sys
from typing import TextIO, Callable, Iterable
from .common import ENV_NL

def create_reader(file_descriptor_id:int=None, max_read_buffer=1024):
  if file_descriptor_id is None: file_descriptor_id = sys.stdin.fileno()

  r = os.fdopen(file_descriptor_id, mode='r')
  buffArr = bytearray(max_read_buffer)
  buffArrCont = [buffArr]

  def readlines() -> Iterable:
    if r.readable():
      while True:

        bytes_read = os.readv(r.fileno(), buffArrCont)
        line = buffArr[:bytes_read].decode()
        #print(f"line-len: {len(line)} bytes: {bytes_read} {buffArr[:bytes_read]}")
        #if line is None: break
        if bytes_read == 0: break
        for l in line.strip().split(ENV_NL):
          yield l

  return readlines
