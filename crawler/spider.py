import os
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

# 自定义请求头和Cookies
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://www.dianping.com/',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
}

cookies = {
    'fspop': 'test',
    '_lxsdk_cuid': '19081af2cc9c8-0b4e8652da6b03-19525637-16a7f0-19081af2cc9c8',
    '_lxsdk': '19081af2cc9c8-0b4e8652da6b03-19525637-16a7f0-19081af2cc9c8',
    '_hc.v': '96999a6c-94db-fdac-6371-1717f5aa36b7.1720162660',
    'WEBDFPID': 'uv16267750x856011xx58575y9xw6v5880918zu696697958217u70x4-2035522660377-1720162659602WAUMKAQ75613c134b6a252faa6802015be905511845',
    'ctu': '20b8de5248597d19185a1abd491db132204b7fae04830d0cab7fdcf97ce98aec',
    'Hm_lvt_602b80cf8079ae6591966cc70a3940e7': '1720162739',
    'HMACCOUNT': 'A63D8B58B289E3B6',
    'cy': '3',
    'cye': 'hangzhou',
    's_ViewType': '10',
    '_lx_utm': 'utm_source%3Dgoogle%26utm_medium%3Dorganic',
    'qruuid': '8504dba4-23bc-4546-a642-86822fc2a329',
    'dplet': '717c7a8750127c2c4c4720abd2749a74',
    'dper': '02027b2568bc2366846f46a87a31f5b7cc0a5100821b47f85159eb975ac6d818d695c648fb9a7efcd8f49bcd82dbe4fd4f8dc4796cb5483a33270000000050210000a06a179fc30910b1bccf71d2f9b53172916ea0ce37fc1e7f0be9c5ca5d98ae14c0dfcd57509c41adddc7b50a22866616',
    'll': '7fd06e815b796be3df069dec7836c3df',
    'ua': '%E7%82%B9%E5%B0%8F%E8%AF%844505657300',
    '_lxsdk_s': '190a104e01a-e48-c2d-19c%7C%7C109',
    'Hm_lpvt_602b80cf8079ae6591966cc70a3940e7': '1720688573'
}

# 爬取的商铺页面的URL
shop_url = 'https://www.dianping.com/hangzhou/ch10'

# 获取页面的HTML内容
def get_html_text(url):
    try:
        response = requests.get(url, headers=headers, cookies=cookies, timeout=20)
        response.raise_for_status()  # 检查响应状态
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except Exception as e:
        print(f"产生异常: {e}")
        return None

# 解析并提取商铺信息
def parse_shop_info(soup):
    main_reviews = soup.find_all(class_='shop-list')
    all_li_elements = []

    for review in main_reviews:
        li_elements = review.find_all('li')
        all_li_elements.extend(li_elements)

    shop_data = []
    for li in all_li_elements:
        shop_name = li.find('h4').text.strip() if li.find('h4') else 'N/A'
        shop_img = li.find('div', class_='pic').find('img')['src'] if li.find('div', class_='pic') and li.find('div', 'pic').find('img') else 'N/A'
        review_num = li.find('a', class_='review-num').find('b').text.strip() if li.find('a', 'review-num') and li.find('a', 'review-num').find('b') else 'N/A'
        mean_price = li.find('a', class_='mean-price').find('b').text.strip() if li.find('a', 'mean-price') and li.find('a', 'mean-price').find('b') else 'N/A'
        recommendations = [rec.text.strip() for rec in li.find_all('a', class_='recommend-click')]
        address_parts = li.find('div', class_='tag-addr').find_all('a') if li.find('div', 'tag-addr') else []
        address = ' | '.join(part.text.strip() for part in address_parts) if address_parts else 'N/A'
        comment_elements = li.find('div', class_='comment').find_all('span', class_='star') if li.find('div', 'comment') else []
        comment = len(comment_elements)

        shop_info = {
            'name': shop_name,
            'image': shop_img,
            'reviews': review_num,
            'price': mean_price,
            'recommendations': recommendations,
            'address': address,
            'comment': comment
        }
        shop_data.append(shop_info)
    return shop_data

# 保存数据到文件
def save_data(data):
    if not os.path.exists('大众点评'):
        os.makedirs('大众点评')

    df = pd.DataFrame(data)
    df.to_excel(os.path.join('大众点评', '店铺.xlsx'), index=False)
    df.to_csv(os.path.join('大众点评', '店铺.csv'), index=False)

# 主函数
def main():
    page = 1
    data = []

    while True:
        if page == 1:
            url = shop_url
        else:
            url = f'{shop_url}/p{page}'

        soup = get_html_text(url)
        if soup is None:
            break

        shop_data = parse_shop_info(soup)
        if not shop_data:
            break

        data.extend(shop_data)
        print(f"完成第{page}页的爬取，一共爬取{len(data)}条")

        page += 1
        print('等待10秒')
        time.sleep(10)

    save_data(data)
    print('完成')

if __name__ == '__main__':
    main()
