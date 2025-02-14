from pynes.core import Reader

readline = Reader().create()

for line in readline():
  print(f"got line: {line}")

