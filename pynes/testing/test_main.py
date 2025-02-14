import os, asyncio, pytest, threading, time
from ..reader import Reader
from ..writer import Writer
from ..common import completedTask

'''
NOTE
cannot pytest on std io (redirects to pseudofile w/ no fileid), but can use custom fd
'''

#def getPipe(): return os.pipe2(os.O_CLOEXEC)
def getPipe(): return os.pipe()

#@pytest.mark.skipif(sys.platform == "win32", reason="Windows-only test")
def main_base(isDelayed:bool=False):

  reads = []
  def exec_reader(fd):
    readlines = Reader(fd).create()
    for line in readlines():
      reads.append(line)

  writes = []
  def exec_writer(fd):
    if isDelayed:
      time.sleep(1)
    writeline = Writer(fd).createStdIoWriter()
    for i in range(1, 4):
      message = f"test {i}"
      writes.append(message)
      writeline(message)

  (rfd, wfd) = getPipe()
  t1 = threading.Thread(target=lambda: exec_reader(rfd))
  t2 = threading.Thread(target=lambda: exec_writer(wfd))
  t1.start()
  t2.start()
  t1.join()
  t2.join()

  assert len(writes) == 3
  assert len(reads) == 3
  assert reads == writes

def test_main_base():
  main_base(isDelayed=False)

def test_main_base_delayed():
  main_base(isDelayed=True)


async def main_base_async(isDelayed:bool=False):

  reads = []
  async def exec_reader(fd):
    readlines = await Reader(fd).createAsync()
    gen = readlines()
    async for line in gen:
      reads.append(line)

  writes = []
  async def exec_writer(fd):
    if isDelayed:
      await asyncio.sleep(1)
    writelineAsync = Writer(fd).createStdIoWriterAsync()
    for i in range(1, 4):
      message = f"test {i}"
      writes.append(message)
      await writelineAsync(message)
  await completedTask()

  (rfd, wfd) = getPipe()
  t1 = asyncio.create_task(coro=exec_reader(rfd))
  t2 = asyncio.create_task(coro=exec_writer(wfd))
  await asyncio.gather(t1, t2)

  assert len(writes) == 3
  assert len(reads) == 3
  assert reads == writes

@pytest.mark.asyncio
async def test_main_base_async():
  await main_base_async(isDelayed=False)

@pytest.mark.asyncio
async def test_main_base_delayed_async():
  await main_base_async(isDelayed=True)
