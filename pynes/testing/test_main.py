import os, time, threading
from ..reader import create_reader
from ..writer import create_writer

'''
NOTE
cannot pytest on std io (redirects to pseudofile w/ no fileid)

testing file descriptors in multiple threads on windows does not work
'''

# (rfd, wfd) = os.pipe2(os.O_CLOEXEC)
def getPipe(): return os.pipe()

def test_main():

  reads = []
  def exec_reader(fd):
    readlines = create_reader(fd)
    for line in readlines():
      reads.append(line)

  writes = []
  def exec_writer(fd):
    writeline = create_writer(fd)
    for i in range(1, 4):
      message = f"test {i}"
      writes.append(message)
      writeline(message)


  (rfd, wfd) = getPipe()
  rt = threading.Thread(target=lambda: exec_reader(rfd))
  wt = threading.Thread(target=lambda: exec_writer(wfd))
  rt.start()
  wt.start()
  rt.join()
  wt.join()

  assert len(reads) == 3
  assert reads == writes

def test_writer_delayed_start():

  reads = []
  def exec_reader(fd):
    readlines = create_reader(fd)
    for line in readlines():
      reads.append(line)

  writes = []
  def exec_writer(fd):
    time.sleep(1)
    writeline = create_writer(fd)
    for i in range(1, 4):
      message = f"test {i}"
      writes.append(message)
      writeline(message)


  (rfd, wfd) = getPipe()
  rt = threading.Thread(target=lambda: exec_reader(rfd))
  wt = threading.Thread(target=lambda: exec_writer(wfd))
  rt.start()
  wt.start()
  rt.join()
  wt.join()

  assert len(reads) == 3
  assert reads == writes
