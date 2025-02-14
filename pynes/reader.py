import os, sys, msvcrt, asyncio
from typing import Iterable
from .common import *

class Reader:
  def __init__(self, file_descriptor_id:int=None, nix_max_read_buffer:int=1024):
    self.file_descriptor_id:int = file_descriptor_id
    self.nix_max_read_buffer:int = nix_max_read_buffer

  def create(self):
    if self.file_descriptor_id is None: self.file_descriptor_id = sys.stdin.fileno()

    readHandle = os.fdopen(self.file_descriptor_id, mode='r')

    if IS_WINDOWS: 
      #NOTES
      #msvcrt.get_osfhandle affects sys.stdin INDIRECTLY
      #msvcrt.get_osfhandle does not working within closure
      msvcrt.get_osfhandle(self.file_descriptor_id)

    def nix_read_factory():
      buffArr = bytearray(self.nix_max_read_buffer)
      buffArrCont = [buffArr]

      def readlines() -> Iterable:
        if readHandle.readable():
          while True:

            bytes_read = os.readv(readHandle.fileno(), buffArrCont)
            line = buffArr[:bytes_read].decode()
            if bytes_read == 0: break
            for l in line[:-1].split(ENV_NL):
              yield l

      return readlines

    def win_read_factory():
      def readlines() -> Iterable:
        for line in readHandle:
          yield line

      return readlines

    if IS_WINDOWS:
      return win_read_factory()
    else:
      return nix_read_factory()



  async def createAsync(self):
    
    if self.file_descriptor_id is None: self.file_descriptor_id = sys.stdin.fileno()
    readHandle = os.fdopen(self.file_descriptor_id, mode='r')

    if IS_WINDOWS: 
      #NOTES
      #msvcrt.get_osfhandle affects sys.stdin INDIRECTLY
      #msvcrt.get_osfhandle does not working within closure
      msvcrt.get_osfhandle(self.file_descriptor_id)

    async def nix_read_factory():
      buffArr = bytearray(self.nix_max_read_buffer)
      buffArrCont = [buffArr]

      async def readlines():
        if readHandle.readable():
          while True:
            
            bytes_read = asyncio.to_thread(lambda: os.readv(readHandle.fileno(), buffArrCont))
            line = buffArr[:bytes_read].decode()
            if bytes_read == 0: break
            for l in line[:-1].split(ENV_NL):
              yield l

      return readlines

    async def win_read_factory():
      
      async def readlines():
        loop = asyncio.get_running_loop()
        while True:
          line = await loop.run_in_executor(None, readHandle.readline)
          if not line:
            break
          yield line[:-1]#remove trailing \n

      return readlines

    if IS_WINDOWS:
      return await win_read_factory()
    else:
      return await nix_read_factory()

