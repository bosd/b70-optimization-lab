#!/usr/bin/env python3
"""Kill processes whose full command line contains the given substring (never the calling shell)."""
import os, signal, subprocess, sys
pat = sys.argv[1]; me = os.getpid(); parent = os.getppid()
for line in subprocess.run(["ps", "-eo", "pid,args"], capture_output=True, text=True).stdout.splitlines()[1:]:
    pid, _, args = line.strip().partition(" ")
    if pat in args and int(pid) not in (me, parent) and "q38-kill-by-cmdline" not in args:
        os.kill(int(pid), signal.SIGTERM); print("kill", pid, args[:60])
