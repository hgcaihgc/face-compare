import os
import sys
import json
import base64
import requests
 
 
def encode_base64(file):
    with open(file,'rb') as f:
        img_data = f.read()
        base64_data = base64.b64encode(img_data)
        # print("base64_data的类型为", type(base64_data))
        # print(base64_data)
        # 如果想要在浏览器上访问base64格式图片，需要在前面加上：data:image/jpeg;base64,
        base64_str = str(base64_data, 'utf-8')  
        # print("base64_str的类型为", type(base64_str))
        return base64_str
 
 
def decode_base64(base64_data):
    with open('./base64.jpg','wb') as file:
        img = base64.b64decode(base64_data)
        file.write(img)
 


def get_access_token(api_key, secret_key):
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={0}&client_secret={1}'.format(api_key, secret_key)
    response = requests.get(host)
    if response:
        # print(response.json()["access_token"])
        return response.json()["access_token"]
    else:
        sys.exit("未获取到access_token")


def face_compare(img_path_1, img_path_2, api_key, secret_key):
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/match"
    access_token = get_access_token(api_key, secret_key)
    params = [
        {
            "image": encode_base64(img_path_1), 
            "image_type": "BASE64", 
            "face_type": "CERT", 
            "quality_control": "LOW"
        }, 
        {
            "image": encode_base64(img_path_2), 
            "image_type": "BASE64", 
            "face_type": "LIVE", 
            "quality_control": "LOW"
        }
    ]


    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/json'}
    response = requests.post(request_url, json=params, headers=headers)
    if response:
        print (response.json())


if __name__ == '__main__':
    img_path_1 = './single_photo.jpg'
    img_path_2 = './group_photo_2.jpg'
    api_key = "Go6nOePIw3fw9gd0vB6T2lte"
    secret_key = "3dIF838G0FGMu2Ou8sXsTMM5SaOAlfmS"
    face_compare(img_path_1, img_path_2, api_key, secret_key)




    
