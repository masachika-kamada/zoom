import subprocess


cmd = ["tasklist"]
proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
result = proc.communicate()
print(type(result))
print(len(result))
for res in result[0].splitlines():
    if "Zoom.exe" in res.decode('utf-8'):
        print(res)
