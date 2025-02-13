from pynes.reader import create_reader

readline = create_reader()
for line in readline():
  print(f"got line: {line}")

