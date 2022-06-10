import subprocess
import psutil

# for proc in psutil.process_iter():
#     print("----------------------")
#     print("プロセスID:" + str(proc.pid))
#     try:
#         print("実行モジュール：" + proc.exe())
#         print("コマンドライン:" + str(proc.cmdline()))
#         print("カレントディレクトリ:" + proc.cwd())
#     except psutil.AccessDenied:
#         print("このプロセスへのアクセス権がありません。")


# cmd = 'tasklist'
# proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

# for line in proc.stdout:
#   print(line.decode('utf-8'))


cmd = ["ls"]
proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
result = proc.communicate()
print(result)
