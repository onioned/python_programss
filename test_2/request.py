import requests
r = requests.get('http://www.baidu.com')
print(r.content);
print(r.text);