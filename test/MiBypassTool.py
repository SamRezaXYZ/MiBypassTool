#!/usr/bin/python

version = "test"

import os

for lib in ['Cryptodome', 'requests']:
    try:
        __import__(lib)
    except ImportError:
        prefix = os.getenv("PREFIX", "")
        if "com.termux" in prefix:
            os.system('yes | pkg update')
        
        if lib == 'Cryptodome':
            if "com.termux" in prefix:
                cmd = 'pip install pycryptodomex --index-url https://offici5l.github.io/archives/plib/'
            else:
                cmd = 'pip install pycryptodomex'
        else:
            cmd = f'pip install {lib}'
        os.system(cmd)

import re, base64, requests, time, json, hmac, hashlib, random, urllib, urllib.parse, platform, shutil, subprocess, zipfile, stat, sys, io
from Cryptodome.Util.Padding import unpad
from base64 import b64encode, b64decode
from Cryptodome.Cipher import AES
from urllib.parse import urlparse

def dw(s):
    print("\ndownload platform-tools...\n")
    url = f"https://dl.google.com/android/repository/platform-tools-latest-{s}.zip"
    cd = os.path.join(os.path.dirname(__file__))
    fp = os.path.join(cd, os.path.basename(url))    
    urllib.request.urlretrieve(url, fp)    
    with zipfile.ZipFile(fp, 'r') as zip_ref:
        zip_ref.extractall(cd)   
    os.remove(fp)

up = os.path.join(os.getenv("PREFIX", ""), "bin", "tmibypass")

def dwt():
    os.system("curl https://raw.githubusercontent.com/offici5l/MiBypassTool/main/test/.install | bash")
    if not os.path.exists(up):
        shutil.copy(__file__, up)
        os.system(f"chmod +x {up}")
        exit()
    else:
        exit()

s = platform.system()
if s == "Linux" and os.path.exists("/data/data/com.termux"):
    try:
        result_adb = os.popen("adb --version").read()
        if "Android Debug" not in result_adb:
            dwt()
    except (FileNotFoundError, Exception):
        dwt()
    if not os.path.exists(up):
        shutil.copy(__file__, up)
        os.system(f"chmod +x {up}")
        print("\nuse command: \033[92mtmibypass\033[0m\n")
        exit()
    cmd = "adb"
    systemp = "t"
else:
    dir = os.path.dirname(__file__)
    fp = os.path.join(dir, "platform-tools")
    if not os.path.exists(fp):
        dw(s)
    cmd = os.path.join(fp, "adb")
    if s == "Linux" or s == "Darwin":
        st = os.stat(cmd)
        os.chmod(cmd, st.st_mode | stat.S_IEXEC)
    systemp = "o"

def CheckD(cmd):
    print("\nCheck if device is connected in normal mode...\n")
    while True:
        try:
            result = subprocess.run([cmd, "get-state"], capture_output=True, text=True, timeout=6)
        except subprocess.TimeoutExpired:
            continue
        if "device" in result.stdout:
            return True
    return False

checkd = CheckD(cmd)

if checkd:
    print("Device is connected \033[92mDone\033[0m\n")
else:
    print("Device is not connected exit...")
    exit()

os.popen(f"{cmd} logcat -c")

os.popen(f"{cmd} shell svc wifi disable")

os.popen(f"{cmd} shell svc data enable")

os.popen(f"{cmd} shell am start --activity-clear-task -a android.settings.APPLICATION_DEVELOPMENT_SETTINGS")

print("\n\033[92mNow bind your account in Mi Unlock status ...\033[0m\n")

account_bind_found = False

while True:
    process = subprocess.Popen(f"{cmd} logcat *:S CloudDeviceStatus:V -d", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    args_found = False
    headers_found = False
    for line in output.decode("utf-8").split('\n'):
        if "CloudDeviceStatus: args:" in line:
            args = line.split('args:')[1].strip()
            args_found = True
        if "CloudDeviceStatus: headers:" in line:
            headers = line.split('headers:')[1].strip()
            headers_found = True
        if args_found and headers_found:
            account_bind_found = True
            subprocess.run(f"{cmd} shell svc data disable", shell=True)
            break
    if account_bind_found:
        break

os.popen(f"{cmd} shell am force-stop com.android.settings")

try:
    headers = {"Cookie": re.search(r"Cookie=\[(.*)\]", AES.new(b'20nr1aobv2xi8ax4', AES.MODE_CBC, b'0102030405060708').decrypt(base64.b64decode(headers)).rstrip(b'\0').decode('utf-8')).group(1).strip(), "Content-Type": "application/x-www-form-urlencoded"}
    
except ValueError as e:
    print("\n\033[91mData decryption failed. Please downgrade system app.\033[0m\n")
    exit()

data = json.loads(unpad(AES.new("20nr1aobv2xi8ax4".encode("utf-8"), AES.MODE_CBC, "0102030405060708".encode("utf-8")).decrypt(base64.b64decode(args)), AES.block_size).decode("utf-8"))

# You can leave them or delete them, it will not affect sending the request
del aj["heartbeat_mode"]
del aj["imsi1"]
del aj["device"]
del aj["error_code"]
del aj["rom_version"]

response = requests.post("https://deviceapi.micloud.xiaomi.net/mic/binding/v1/identified/device/account", data=data, headers=headers)

data = json.loads(response.text)

if "code" in data:
    if data["code"] == 0:
        print("\n\033[92mLinked successfully\033[0m\n")
    else:
        for key, value in data.items():
            print(f"\n{key}: {value}")
else:
    print(data)


systemp == "o" and input("\nPress Enter to exit ...")