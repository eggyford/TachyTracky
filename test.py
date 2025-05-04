import pip._vendor.requests as requests # API Calls for pulsoid
import time

import ctypes # Mouse sens

#run pip install pycaw

from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume # Volume control

def main():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)

    controlVolume = True
    controlMouseSens = True

    APIKEY = "1adce522-edca-48ba-b4e1-212552bca6eb"
    minHR = 60 # set heartrate for minimum volume
    maxHR = 200 # set heartrate for maximum volume 
    minVol = 10 # set minimum volume (0-100)
    maxVol = 100 # set maximum volume
    minSens = 1 # set minimum mouse sens (1-100)
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

main()