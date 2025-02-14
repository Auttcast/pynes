from pynes.writer import create_writer

writeline = create_writer()

for i in range(1, 6):
  isEven = i % 2 == 0
  evenOrOdd = "even" if isEven else "odd"
  writeline(f"message {i} {evenOrOdd}")
