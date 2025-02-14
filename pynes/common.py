import os, asyncio

#using this const for STDIN because weird things happen on windows
STDIN = 0
IS_WINDOWS = os.name == 'nt'

#turns out it's always \n on windows, \r\n was not found.
ENV_NL = "\n"# if not IS_WINDOWS else "\n"

def completedTask():
  res = asyncio.Future()
  res.set_result(None)
  return res