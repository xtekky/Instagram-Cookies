import requests, re, random, string

def __int_to_base(x: int, base: int) -> str:
    base_36 = string.digits + string.ascii_letters
    
    if x < 0:
        sign = -1
    elif x == 0:
        return base_36[0]
    else:
        sign = 1
    x *= sign
    digits = []
    while x:
        digits.append(base_36[x % base])
        x = x // base
    if sign < 0:
        digits.append('-')
    digits.reverse()
    return "".join(digits)

def generate_x_mid() -> str:
    return "".join([__int_to_base(random.randint(2**29, 2**32), 36) for _ in range(8)])

def get_headers() -> dict:

    headers = {
        'authority': 'www.instagram.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    }

    libcommons_hash = re.findall(
        r'(?<=ConsumerLibCommons\.js\/)[a-z0-9]{12}', 
        requests.get(
            url = 'https://www.instagram.com/', 
            headers=headers
        ).text
    )[0]

    res = requests.get(
        url = f'https://www.instagram.com/static/bundles/es6/ConsumerLibCommons.js/{libcommons_hash}.js', 
        headers=headers
    ).text


    asbd_id = re.findall(
        r"ASBD_ID='(\d+)'", 
        res
    )[0]
    
    fbapp_id = re.findall(
        r"AppId='(\d+)'", 
        res
    )[0]


    data =  requests.get(
        url = (
            "https://"
            + "www.instagram.com"
        ),
        headers = headers
    ).text

    device_id = re.findall(
        r'(?<="device_id":")[A-Z0-9\-]{35,36}', 
        data
    )[0]

    crsf = re.findall(
        r'(?<="csrf_token":")[a-zA-Z0-9]{31,32}', 
        data
    )[0]

    rollout_hash = re.findall(
        r'(?<="rollout_hash":")[a-z0-9]{11,12}', 
        data
    )[0]
    
    
    __headers = {
        "X-Mid": generate_x_mid(),
        "X-CSRFToken": crsf,
        "X-IG-App-ID": fbapp_id,
        "X-ASBD-ID": asbd_id,
        "X-Web-Device-ID": device_id,
        "X-Instagram-AJAX": rollout_hash,
    }
    
    __headers["Cookie"] = f"csrftoken={__headers['X-CSRFToken']}; mid={__headers['X-Mid']}; ig_did={__headers['X-Web-Device-ID']}"
    
    return __headers
    
if __name__ == "__main__":
  print(get_headers())
