import pip._vendor.requests as requests
import time
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

APIKEY = ""

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

    computerVolume = max((heartrate-60)/2, 10)/100
    volume.SetMasterVolumeLevelScalar(computerVolume, None)
    print("Volume: ", round(volume.GetMasterVolumeLevelScalar() * 100))

    time.sleep(5)
