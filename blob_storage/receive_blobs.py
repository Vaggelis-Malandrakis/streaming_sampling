import subprocess
import glob
import os
import re
import time

regex_concise = r"N: \S+, Average: (\S+), Minimum: (\S+), Maximum: (\S+)"

def sync_with_azure():
    subprocess.call(
        "/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe  azcopy sync 'https://minestoracc2.blob.core.windows.net/working-container' . --recursive",
        shell=True, stdout=subprocess.DEVNULL)

def find_blobs_in_directory(scanned_file_list):
    new_blobs = []
    files = glob.glob("*.txt")
    for file in files:
        if file not in scanned_file_list:
            print('Found new file: ', file)
            new_blobs.append(file)
    return new_blobs

def delete_txt_files_from_directory():
    files = glob.glob("*.txt")
    for file in files:
        os.remove(file)

def get_concise_sampling_metrics(line):
    match_list = []
    matches = re.finditer(regex_concise, line, re.MULTILINE)
    for match in matches:
        for group in match.groups():
            match_list.append(float(group))
    return match_list

def read_file(pathfile):
    f = open(pathfile, "r")
    return str(f.read())

scanned_file_list = []
first_pass = True
current_avg = None
current_min = None
current_max = None

delete_txt_files_from_directory()
while True:
    sync_with_azure()
    temp_new_blobs = find_blobs_in_directory(scanned_file_list)
    scanned_file_list = scanned_file_list + temp_new_blobs
    for file in temp_new_blobs:
        line = read_file(file)
        temp_avg, temp_min, temp_max = get_concise_sampling_metrics(line)
        if first_pass:
            first_try = False
            current_avg = temp_avg
            current_min = temp_min
            current_max = temp_max
        else:
            current_avg = (current_avg + temp_avg) / 2
            current_min = (current_min + temp_min) / 2
            current_max = (current_max + temp_max) / 2
    print(current_avg, current_min, current_max)
    time.sleep(10)