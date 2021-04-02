import requests
from . import config

# def gen_sign(timestamp):
#     secret_enc = secret.encode('utf-8')
#     string_to_sign = f'{timestamp}\n{secret}'
#     string_to_sign_enc = string_to_sign.encode('utf-8')
#     hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
#     sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
#     print(sign)
#     return sign
    
def send_msg(content):
    # timestamp = round(time.time() * 1000)
    para = {
        'access_token': config.get('report.ding', 'token'),
        # 'timestamp': timestamp,
        # 'sing': gen_sign(timestamp)
    }
    data ={
        "msgtype": "link", 
        "link": {
            "text": content,
            "title": "点击查看详细报告", 
            "picUrl": "", 
            "messageUrl": config.get('report', 'allure_url')
        }
    }
    
    requests.post(config.get('report.ding', 'url'), params=para, json=data)

    


