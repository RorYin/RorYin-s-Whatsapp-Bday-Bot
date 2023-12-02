import requests

def dotask():
    url = "https://roryinswhatsappbdaybotwebapp.onrender.com/task" #use your own deployed url
    resp = requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'})
    print(resp)


if __name__ == '__main__':
    dotask()

