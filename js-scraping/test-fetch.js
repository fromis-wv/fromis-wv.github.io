member_id =
{
    'gyuri': 'db56036fc59a94a9ef617261c90c783f'
    'hayoung': '67b4c6fb2220ac6705aa97046f3503a1'
    'jiheon': '5fb309bc7489a576484431ba8338807e'
}

// https://weverse.io/fromis9/artist/1-59426

id = member_id['gyuri']

wmsgpad = int(time.time() * 1000)

wmd = base64.b64encode(hmac.HMAC(key, f'{api_path[:255]}{wmsgpad}'.encode(), digestmod=hashlib.sha1).digest()).decode()

request = "https://global.apis.naver.com/weverse/wevweb/comment/v1.0/member-db56036fc59a94a9ef617261c90c783f/comments?after=1724044750739&fieldSet=memberCommentsV1&sortType=LATEST&appId=be4d79eb8fc7bd008ee82c8ec4ff6fd4&language=en&os=WEB&platform=WEB&wpf=pc&wmsgpad=1734256826457&wmd=DKHyL2ZgUb5M0kdPcc7DrenBZxc%3D"

response = await fetch(request, {
  "headers": {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIwMTVmNzg5NGRlNzk0YzJmOWM0N2I2YmNjMmUwMTM0Nzo4OSIsInN1YiI6IjIzYmEyZmUxZGU0YzRjOTM4MjAwYTg2MWQ2OGZiYTZlMDEwIiwiaWF0IjoxNzM0MTgxNDE2LCJleHAiOjE3MzQ0NDA2MTYsImlzcyI6Imh0dHBzOi8vYWNjb3VudGFwaS53ZXZlcnNlLmlvIiwiYXVkIjoiaHR0cHM6Ly9hY2NvdW50YXBpLndldmVyc2UuaW8iLCJ2ZXIiOjIsImNsaWVudF9pZCI6IndldmVyc2UiLCJwbGF0Zm9ybSI6IldFQiIsInNvY2lhbC5wcm92aWRlciI6IkdPT0dMRSIsInNvY2lhbC51aWQiOjE0NDQ4Njg2fQ.8aS_it0r85mNt6HnospB8kbDBT9W_5-f4SiE6zu6CT0",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "wev-device-id": "25057b37-b262-4392-be76-10767c22eee5",
    "wev-open-community": "A"
  },
  "referrer": "https://weverse.io/",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "include"
});
