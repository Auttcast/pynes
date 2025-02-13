import os, sys
from typing import Iterable
from .common import ENV_NL, IS_WINDOWS

def create_reader(file_descriptor_id:int=None, nix_max_read_buffer=1024):
  if file_descriptor_id is None: file_descriptor_id = sys.stdin.fileno()
  r = os.fdopen(file_descriptor_id, mode='r')

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
    pass
    #
    # buffArr = bytearray(nix_max_read_buffer)
    #
    # def readlines() -> Iterable:
    #   if r.readable():
    #     while True:
    #
    #       bytes_read = os.read(r.fileno())
    #       line = buffArr[:bytes_read].decode()
    #       if bytes_read == 0: break
    #       for l in line.strip().split(ENV_NL):
    #         yield l
    #
    # return readlines

  if IS_WINDOWS:
    return win_read_factory()
  else:
    return nix_read_factory()