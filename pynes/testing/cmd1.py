from pynes.writer import Writer
from time import sleep

writeline = Writer().createStdIoWriter()

for i in range(1, 6):
  isEven = i % 2 == 0
  evenOrOdd = "even" if isEven else "odd"
  sleep(.2)
  writeline(f"message {i} {evenOrOdd}")
  print("whatever")
