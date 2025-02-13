import os

IS_WINDOWS = os.name == 'nt'
ENV_NL = "\n" if not IS_WINDOWS else "\r\n"
