import os, sys, asyncio
from .common import ENV_NL

class Writer:

  def __init__(self, file_descriptor_id:int=None):
    self.file_descriptor_id:int = file_descriptor_id

  def createStdIoWriter(self):
    writelineFunc = self.__createIoWriter()
    return writelineFunc

  def createStdErrWriter(self):
    '''only supported when file_descriptor_id is None'''
    writelineFunc = self.__createIoWriter(useStdErr=True)
    return writelineFunc

  def createStdIoWriterAsync(self):
    writelineFuncAsync = self.__createIoWriterAsync()
    return writelineFuncAsync
  
  def createStdErrWriterAsync(self):
    '''only supported when file_descriptor_id is None'''
    writelineFuncAsync = self.__createIoWriterAsync(useStdErr=True)
    return writelineFuncAsync

  def __setupWriter(self, useStdErr:bool):
    sysStream = None
    if self.file_descriptor_id is None:
      sysStream = sys.stdout.fileno() if not useStdErr else sys.stderr.fileno()

    fid = self.file_descriptor_id if self.file_descriptor_id is not None else sysStream
    writeHandle = os.fdopen(fid, mode='w')

    return writeHandle

  def __createIoWriter(self, useStdErr=False):

    writeHandle = self.__setupWriter(useStdErr)

    def writeline(line:str):
      writeHandle.write(f"{line}{ENV_NL}")
      writeHandle.flush()

    return writeline
    
  def __createIoWriterAsync(self, useStdErr=False):

    writeHandle = self.__setupWriter(useStdErr)

    def writeline(line:str):
      writeHandle.write(f"{line}{ENV_NL}")
      writeHandle.flush()

    return lambda line: asyncio.to_thread(lambda: writeline(line))
  