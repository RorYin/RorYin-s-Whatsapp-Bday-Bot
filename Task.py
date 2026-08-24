import os

from config import BASE_DIR
from handler import check_work_anniversaries, checkbdays

if os.path.isdir("/home/RorYinBot2/mysite"):
    os.chdir("/home/RorYinBot2/mysite")
else:
    os.chdir(BASE_DIR)

log = checkbdays()
log2 = check_work_anniversaries()
try:
    print(log)
    print(log2)
except Exception:
    print("Something went wrong in Task.py")
