import os,time
import threading

file_path = os.path.dirname(__file__) + '\\' + "temToTwitch.py"

def cmd_run():
    res = os.popen("python " + file_path)
    res.close()

threads = []  


num = 3
for i in range(num):
    t = threading.Thread(target=cmd_run)
    t.start()
    threads.append(t)
    time.sleep(25)
    
for w in threads:
    w.join()