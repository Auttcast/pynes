from pynes.reader import Reader

readline = Reader().create()
for line in readline():
  print(f"got line: {line}")

