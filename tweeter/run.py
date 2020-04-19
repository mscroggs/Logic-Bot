import subprocess
import os
p = subprocess.Popen(['pgrep', '-f', 'next_tautology.py'], stdout=subprocess.PIPE)
out, err = p.communicate()

if len(out.strip()) == 0:
    p = subprocess.Popen(["nice","-19","python3","next_tautology.py"])
    p.communicate()
