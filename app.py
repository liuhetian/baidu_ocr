import base64, urllib.parse, requests, json, os
os.environ['STREAMLIT_SERVER_ENABLE_STATIC_SERVING'] = 'true'

import streamlit as st

from functools import wraps
from pathlib import Path
path = Path('static')


def retry(max_attempts, delay):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempts + 1} failed. Retrying in {delay} seconds.")
                    attempts += 1
                    time.sleep(delay)
                    if attempts == max_attempts:
                        raise
        return wrapper
    return decorator


API_KEY = st.secrets.API_KEY  
SECRET_KEY = st.secrets.SECRET_KEY  

@retry(10, 1)
def main(image):
        
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/numbers?access_token=" + get_access_token()
    data = f'image={image}&detect_direction=false'
    headers = {
        'Content-Type': 'x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=data)
    return response.text

def analyze(response):
    res = json.loads(response)['words_result']
    for i in res:
        if len(a:=i['words']) == 25:
            tep = a[:-1]
        elif len(a:=i['words']) == 24:
            tep = a
    print(a, tep)        
    return tep
    
def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

st.header('ORC识别')

uploaded_file = st.file_uploader("Choose a file", type=['png', 'jpg'], accept_multiple_files=True)

if uploaded_file is not None:
    # To read file as bytes:
    if not isinstance(uploaded_file, list):
        bytes_data = uploaded_file.getvalue()
        base64_encoded = base64.b64encode(bytes_data).decode("utf8")
        # 进行URL安全编码
        url_encoded = urllib.parse.quote_plus(base64_encoded)
        #st.write(url_encoded)
        res = analyze(main(url_encoded))
        with open(path.joinpath(uploaded_file.name), 'wb') as f:
            f.write(bytes_data)
        st.write(res)
       
        with open('result.txt', 'r') as f:
            results = eval(f.read())
        results[uploaded_file.name] = res
        with open('result.txt', 'w') as f:
            f.write(str(results))
        st.write('已将一个文件的识别结果保存')
            
            
    else:
        new_results = {}
        for one_file in uploaded_file:
            bytes_data = one_file.getvalue()
            base64_encoded = base64.b64encode(bytes_data).decode("utf8")
            # 进行URL安全编码
            url_encoded = urllib.parse.quote_plus(base64_encoded)
            #st.write(url_encoded)
            res = analyze(main(url_encoded))
            with open(path.joinpath(one_file.name), 'wb') as f:
                f.write(bytes_data)
            new_results[one_file.name] = res
            st.write(one_file.name, res)
        with open('result.txt', 'r') as f:
            results = eval(f.read())
        results.update(new_results)
        with open('result.txt', 'w') as f:
            f.write(str(results))
        st.write('已将全部文件的识别结果保存')
            

    
st.divider()


