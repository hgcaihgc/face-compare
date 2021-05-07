import os
import sys
import base64
import requests
 
 
def encode_base64(file):
    with open(file,'rb') as f:
        img_data = f.read()
        base64_data = base64.b64encode(img_data)  # 此时为bytes类型的数据，将编码后的数据转换为字符串，直接str(base64_data)，字符串前还是会有'b'，可以str(base64_data, ‘utf-8’) 去掉字符串前面的"b"
        # 如果想要在浏览器上访问base64格式图片，需要在前面加上：data:image/jpeg;base64
        base64_str = str(base64_data, 'utf-8')  
        return base64_str
 
 
def decode_base64(base64_data):
    with open('./base64.jpg','wb') as file:
        img = base64.b64decode(base64_data)
        file.write(img)
 

def get_access_token(api_key, secret_key):
    """获取Access Token"""
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={0}&client_secret={1}'.format(api_key, secret_key)
    response = requests.get(host)
    if response:
        # print(response.json()["access_token"])
        return response.json()["access_token"]
    else:
        sys.exit("未获取到access_token")


def face_compare(img_1, img_2, api_key, secret_key):
    """人脸比对"""
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/match"
    access_token = get_access_token(api_key, secret_key)
    params = [
        {
            "image": encode_base64(img_1), 
            "image_type": "BASE64", 
            "face_type": "CERT", 
            "quality_control": "LOW"
        }, 
        {
            "image": encode_base64(img_2), 
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


def face_detection(img, api_key, secret_key):
    """人脸检测"""
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
    params = {
        "image":encode_base64(img), 
        "image_type":"BASE64", 
        "face_field":"faceshape,facetype",
        "max_face_num": 6,
        "face_type":"LIVE"
        }
    access_token = get_access_token(api_key, secret_key)
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/json'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        print (response.json())


def create_group(api_key, secret_key, group_name):
    """创建用户组"""
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/group/add"
    params = {"group_id":group_name}
    access_token = get_access_token(api_key, secret_key)
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/json'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        print (response.json())


def face_register(api_key, secret_key, group_name, user_name, user_info, img):
    """人脸注册，同时建立用户组、用户"""
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/add"
    params = {
        "image":encode_base64(img),
        "image_type":"BASE64",
        "group_id":group_name,
        "user_id":user_name,
        "user_info":user_info,
        "quality_control":"LOW",
        "liveness_control":"NORMAL"
        }
    access_token = get_access_token(api_key, secret_key)
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/json'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        print (response.json())


def face_search(api_key, secret_key, group_name, img):
    """人脸搜索"""
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/search"
    params = {
        "image":encode_base64(img),
        "image_type":"BASE64",
        "group_id_list":group_name,
        "max_user_num":6,
        "quality_control":"LOW",
        "liveness_control":"NORMAL"
        }
    access_token = get_access_token(api_key, secret_key)
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/json'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        print (response.json())


if __name__ == '__main__':
    img = './group_photo.jpg'
    api_key = "Go6nOePIw3fw9gd0vB6T2lte"
    secret_key = "3dIF838G0FGMu2Ou8sXsTMM5SaOAlfmS"
    # face_compare(img_1, img_2, api_key, secret_key)
    # face_detection(img, api_key, secret_key)
    # face_register(api_key, secret_key, "friend", "hgc", "胡", img)
    face_search(api_key, secret_key, "friend_mc", img)
