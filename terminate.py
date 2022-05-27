import os,signal
cwd = os.getcwd()
parent=os.path.dirname(cwd)
with open(parent+'\web\\python\\pid.txt','r') as f:
    pid=f.read()
    os.kill(int(pid),signal.SIGABRT)

