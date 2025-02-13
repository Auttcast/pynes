import os, sys
from .common import ENV_NL

def create_writer(file_descriptor_id:int=None):
  if file_descriptor_id is None: file_descriptor_id = sys.stdout.fileno()

  w = os.fdopen(file_descriptor_id, mode='w')

  def writeline(line:str):
    w.write(f"{line}{ENV_NL}")
    w.flush()
  return writeline
