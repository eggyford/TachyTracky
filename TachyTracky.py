import pip._vendor.requests as requests # API Calls for pulsoid
import time

#run pip install pycaw

from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume # Volume control

import ctypes # Mouse sens

import subprocess # App kill
import psutil

def main():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)

    controlVolume = True
    controlMouseSens = True
    controlAppKill = True

    APIKEY = "" # get key from https://pulsoid.net/ui/keys

    applicationName = "" # e.g. firefox.exe

    minHR = 60 # set heartrate for mins
    maxHR = 200 # set heartrate for maxs 
    minVol = 10 # set minimum volume (0-100)
    maxVol = 100 # set maximum volume
    minSens = 1 # set minimum mouse sens (1-20)
    maxSens = 20 # set maximum mouse sens

    url = "https://dev.pulsoid.net/api/v1/data/heart_rate/latest?response_mode=text_plain_only_heart_rate"
    headers = {
        "Authorization": "Bearer " + APIKEY,
        "Content-Type": "application/json"
    }

    while(True):
        response = requests.get(url, headers=headers)
        print("Status Code:", response.status_code)
        print("HR: ", response.text)
        heartrate = int(response.text)

        if controlVolume:
            computerVolume = rangeAdjust(minHR,maxHR,minVol,maxVol,heartrate)/100
            volume.SetMasterVolumeLevelScalar(computerVolume, None)
            print("Volume: ", round(volume.GetMasterVolumeLevelScalar() * 100))

        if controlMouseSens:
            mouseSens = round(rangeAdjust(minHR,maxHR,minSens,maxSens,heartrate))
            ctypes.windll.user32.SystemParametersInfoW(113, 0, mouseSens, 0)
            print("Sens: ", mouseSens)

        if controlAppKill and (heartrate > maxHR or heartrate < minHR) and checkProcessRunning(applicationName):
            print("Heartrate out of range! Killing app!")
            subprocess.call("TASKKILL /F /IM " + applicationName, shell=True)


        print()
        time.sleep(5)

def rangeAdjust(oldMin: int, oldMax: int, newMin: int, newMax: int, val: int):
    OldRange = (oldMax - oldMin)  
    NewRange = (newMax - newMin)
    NewValue = (((val - oldMin) * NewRange) / OldRange) + newMin

    if NewValue > newMax:
        return newMax
    if NewValue < newMin:
        return newMin
    return NewValue

def checkProcessRunning(name):
    for process in psutil.process_iter(['name']):
        if process.info['name'] == name:
            return True
    return False

main()