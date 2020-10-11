import requests
from fake_useragent import UserAgent

ua = UserAgent(verify_ssl=False)

headers = {
    'user-agent': ua.random,
    'referer': 'https://shimo.im/login?from=home'
}

login_url = 'https://shimo.im/lizard-api/auth/password/login'

user_name = '1260101013@qq.com'
password = '12345678'

response = requests.post(login_url, data={'email': user_name, 'mobile': '+86undefined', 'password':password}, headers=headers)
print(response.text)