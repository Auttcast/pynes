import os, time, threading, asyncio, pytest
from ..reader import Reader
from ..writer import create_writer

'''
NOTE
cannot pytest on std io (redirects to pseudofile w/ no fileid)

testing file descriptors in multiple threads on windows does not work - async?
'''

# (rfd, wfd) = os.pipe2(os.O_CLOEXEC)
def getPipe(): return os.pipe()

@pytest.mark.asyncio
async def test_main():

  reads = []
  async def exec_reader(fd):
    readlines = await Reader(fd).createAsync()
    gen = readlines()
    async for line in gen:
      reads.append(line)

  writes = []
  async def exec_writer(fd):
    writeline = create_writer(fd)
    for i in range(1, 4):
      message = f"test {i}"
      writes.append(message)
      writeline(message)

    res = asyncio.Future()
    res.set_result(None)
    await res

  (rfd, wfd) = getPipe()
  t1 = asyncio.create_task(coro=exec_reader(rfd))
  t2 = asyncio.create_task(coro=exec_writer(wfd))
  await asyncio.gather(t1, t2)

  assert len(writes) == 3
  assert len(reads) == 3
  assert reads == writes

@pytest.mark.asyncio
async def test_main_delayed_start():

  reads = []
  async def exec_reader(fd):
    readlines = await Reader(fd).createAsync()
    gen = readlines()
    async for line in gen:
      reads.append(line)

  writes = []
  async def exec_writer(fd):
    writeline = create_writer(fd)
    await asyncio.sleep(1)
    for i in range(1, 4):
      message = f"test {i}"
      writes.append(message)
      writeline(message)

    res = asyncio.Future()
    res.set_result(None)
    await res

  (rfd, wfd) = getPipe()
  t1 = asyncio.create_task(coro=exec_reader(rfd))
  t2 = asyncio.create_task(coro=exec_writer(wfd))
  await asyncio.gather(t1, t2)

  assert len(writes) == 3
  assert len(reads) == 3
  assert reads == writes
