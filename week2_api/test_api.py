import requests

# 用百度测试，国内稳定
response = requests.get("https://www.baidu.com")
print("状态码:", response.status_code)
print("返回长度:", len(response.text), "字符")