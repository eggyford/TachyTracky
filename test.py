import pip._vendor.requests as requests
import time
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


def main():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)

    APIKEY = ""
    minHR = 60 # set heartrate for minimum volume
    maxHR = 200 # set heartrate for maximum volume 
    minVol = 10 # set minimum volume
    maxVol = 100 # set maximum volume

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


        computerVolume = rangeAdjust(minHR,maxHR,minVol,maxVol,heartrate)/100
        volume.SetMasterVolumeLevelScalar(computerVolume, None)
        print("Volume: ", round(volume.GetMasterVolumeLevelScalar() * 100))

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