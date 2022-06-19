import subprocess
import os


def check_zoom():
    cmd = ["tasklist"]
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    result = proc.communicate()
    print(type(result))
    print(len(result))
    for res in result[0].splitlines():
        if "Zoom.exe" in res.decode('utf-8'):
            print(res)
            os.system("taskkill /im Zoom.exe")
            return


if __name__ == "__main__":
    target_exe = "Zoom.exe"
    check_zoom()
    check_zoom()
