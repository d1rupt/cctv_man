import json
import cv2

def read_config():
    try:
        with open('./config/cameras.json', 'r') as f:
            js = json.load(f)
    except:
        js = []
    return js
def list_cameras_ids():
    skip = []
    js = read_config()
    for i in js:
        if "idchoice" in i.keys():
            skip.append(int(i["idchoice"]))
    arr = []
    for index in range(10):
        if index not in skip:
            print(f"TRYING INDEX{index}")
            try:
                cap = cv2.VideoCapture(index)
                if cap.read()[0]:
                    print("ok")
                    arr.append(index)
                print("releasing")
                cap.release()
                print("done")
            except:
                pass
    print("retyrn")
    return arr


print(read_config())