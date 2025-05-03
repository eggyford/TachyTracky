import pip._vendor.requests as requests
import time
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


def main():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)

    APIKEY = "1adce522-edca-48ba-b4e1-212552bca6eb"

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

        computerVolume = rangeAdjust(60,200,10,100,heartrate)/100
        volume.SetMasterVolumeLevelScalar(computerVolume, None)
        print("Volume: ", round(volume.GetMasterVolumeLevelScalar() * 100))

        time.sleep(5)

def rangeAdjust(oldMin: int, oldMax: int, newMin: int, newMax: int, val: int):
    OldRange = (oldMax - oldMin)  
    NewRange = (newMax - newMin)
    NewValue = (((val - min) * NewRange) / OldRange) + newMin
    return NewValue

main()