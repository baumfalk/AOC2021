import os
import sys
print(os.listdir("./"))
import time


def run_all():
    cur_time = time.time()
    for file in sorted(os.listdir("./")):
        if file.isdecimal():
            print(file)
            print("--------------------")
            os.chdir(f"{file}")
            os.system(f"python {file}.py")
            os.chdir(f"../")
            print()
    print(time.time() - cur_time)
run_all()