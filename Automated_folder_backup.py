import os
import schedule
import datetime
import time
import shutil

source_dir = "E:/Personal Images"
destination_dir = "C:/Users/hp/Downloads"


def copy_folder(src, dest):
    today = datetime.date.today()
    dest_dir = os.path.join(dest, str(today))
    try:
        shutil.copytree(src, dest_dir)
        print(f"Folder has been copied to {dest_dir}")
    except FileExistsError:
        print(f"File already exists at location {dest}")

schedule.every().day.at("20:06").do(lambda:copy_folder(source_dir, destination_dir))

while True:
    schedule.run_pending()
    print("Running after every 60 seconds\n")
    time.sleep(60)