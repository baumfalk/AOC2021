import os
import sys
print(os.listdir("./"))

for file in sorted(os.listdir("./")):
    if file.isdecimal():
        print(file)
        print("--------------------")
        os.chdir(f"{file}")
        os.system(f"python {file}.py")
        os.chdir(f"../")
        print()