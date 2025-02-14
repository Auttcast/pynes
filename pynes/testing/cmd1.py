from pynes.core import Writer
from time import sleep
Writer.createStdIoWriterAsync()
writeline = Writer().createStdIoWriter()
writeError = Writer().createStdErrWriter()

for i in range(1, 6):
  isEven = i % 2 == 0
  evenOrOdd = "even" if isEven else "odd"
  sleep(.2)
  if isEven:
    writeline(f"message {i} {evenOrOdd}")
  else:
    writeError(f"oops {i} {evenOrOdd}")
  print("whatever")
