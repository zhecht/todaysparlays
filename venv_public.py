activate_this = '/home/zhecht/.virtualenvs/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys

# explicitly set package path
path = '/home/zhecht/todaysparlays/'
if path not in sys.path:
    sys.path.append(path)

import subprocess

subprocess.Popen(['python', '/home/zhecht/todaysparlays/controllers/update_public.py'] + sys.argv[1:])
