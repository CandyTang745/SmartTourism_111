import requests
from bs4 import BeautifulSoup
import csv
import os
import time
import random

# 配置日志
#logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_scenic_spots(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        return [line.strip() for line in file.readlines()]

# 定义CSV文件路径
csv_file = 'scenic_spots_introduction1_5A.csv'

# 失败地名存储文件
FAILED_LOCATIONS_FILE = 'failed_locations_5A.txt'

def log_failed_location(location):
    """
    将失败的地名写入文件
    :param location: 失败的地名
    """
    with open(FAILED_LOCATIONS_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{location}\n")
#    logging.info(f"已记录失败的地名: {location}")
# 定义图片保存目录
image_dir = 'scenic_spots_images_5A'
if not os.path.exists(image_dir):
    os.makedirs(image_dir)


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Referer": "https://www.baidu.com/",
    "Connection": "keep-alive"
}
headers["Cookie"] = "BDUSS=G94MGxwemozd0pCWHhBQzB4QnVxb21QNW80ZlBpVm9MZm9UdEp5ekFoT042VTluSVFBQUFBJCQAAAAAAQAAAAEAAAB5LDNgzMfMx8zGX2NhbmR5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAI1cKGeNXChnZ; BDUSS_BFESS=G94MGxwemozd0pCWHhBQzB4QnVxb21QNW80ZlBpVm9MZm9UdEp5ekFoT042VTluSVFBQUFBJCQAAAAAAQAAAAEAAAB5LDNgzMfMx8zGX2NhbmR5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAI1cKGeNXChnZ; BAIDUID=61D3CEF16A94C207AD4D4A686CB91B29:FG=1; MAWEBCUID=web_dEIvUOqcMWEoPDsMJyodRcGUirkLMMsuEbbWfOOaHhjQShoWjs; PSTM=1740150363; BIDUPSID=26CB4D6974C0D40A59316FE53F1457B9; H_WISE_SIDS_BFESS=110085_633614_641171_641316_641591_643360_643292_643763_643837_644234_644348_644372_644353_644317_644238_644554_644626_644718; MCITY=-104%3A; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; H_PS_PSSID=60271_61027_62135_62325_62340_62346_62329_62368_62370_62420_62423_62476_62485; H_WISE_SIDS=60271_61027_62135_62325_62340_62346_62329_62368_62370_62420_62423_62476_62485; BDSFRCVID=QKIOJeC62iSr1aJJFe5jeYiUGfQUnxbTH6aoMtlNjFOw5pTTab8OEG0PCf8g0Kuh1ynoogKKX2OTHIIF_2uxOjjg8UtVJeC6EG0Ptf8g0x5; H_BDCLCKID_SF=JRKDoI8btKt3fP36q47o2t4OhgT22-usLm3A2hcH0KLKjfO4DtQkyxK8jf6-X4cP3KcI-RryKfb1MRjvXJOSX4IzXpttbp3nKCuO2h5TtUJTeCnTDMRhM5_-hxnyKMniynr9-pnYWlQrh459XP68bTkA5bjZKxtq3mkjbPbDfn02JKKu-n5jHjo-eaAD3q; delPer=0; PSINO=7; BAIDUID_BFESS=61D3CEF16A94C207AD4D4A686CB91B29:FG=1; BDSFRCVID_BFESS=QKIOJeC62iSr1aJJFe5jeYiUGfQUnxbTH6aoMtlNjFOw5pTTab8OEG0PCf8g0Kuh1ynoogKKX2OTHIIF_2uxOjjg8UtVJeC6EG0Ptf8g0x5; H_BDCLCKID_SF_BFESS=JRKDoI8btKt3fP36q47o2t4OhgT22-usLm3A2hcH0KLKjfO4DtQkyxK8jf6-X4cP3KcI-RryKfb1MRjvXJOSX4IzXpttbp3nKCuO2h5TtUJTeCnTDMRhM5_-hxnyKMniynr9-pnYWlQrh459XP68bTkA5bjZKxtq3mkjbPbDfn02JKKu-n5jHjo-eaAD3q; BA_HECTOR=2gaga5258k8k8g802l252h840chs0v1jt2bha23; ZFY=I3sdzl0hDAKmQ4SWnv7X3Pgkw2ib:AjjQYpQL8HasISc:C; BDRCVFR[pRAxDSK7ZeD]=mk3SLVN4HKm; ab_sr=1.0.1_ZmJlNTE0ZTdmZjAwMTI0MDgzZWU1MDhhNTg4ZjYyYzg1MGE5ZTZjZWQ5OTdmYjcwNTk0YTJiYmJjNjkwYTI2M2QwYzU0MzA1NTIzODEzZjQ5YjE4OWJhZjNiNWMyMDQ4M2M1ZWJlYjBkYjkwOTE1NjM4NDI0MWJiMzA0ZWIxNmYwNjY4MGY0Njc4MzNiMDMxNjNjODFmZjMzMjRjMGJjOA==; baikeVisitId=d3377822-121c-4402-adeb-054bdc8e3369"





# 加载景点列表
scenic_spots = load_scenic_spots('5A.txt')
# print(scenic_spots)


# 你的 ScraperAPI 密钥
API_KEY = '9192a759f9ffddded85ab50228465b69'





# 打开CSV文件，准备写入数据
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # 写入表头
    writer.writerow(['景区名称', '简介', '图片路径'])

    # 遍历景区列表，逐个爬取
    for spot in scenic_spots:
        # print(f'https://baike.baidu.com/item/{spot}')
        # 构建百度百科的URL
        url = f'https://baike.baidu.com/item/{spot}'

        # ScraperAPI 的端点
        # api_url = f'http://api.scraperapi.com?api_key={API_KEY}&url={url}'
        # print(api_url)
        payload = {'api_key': '9192a759f9ffddded85ab50228465b69', 'url': url}
        response = requests.get('https://api.scraperapi.com/', params=payload)

        # 检查请求是否成功
        if response.status_code == 200:
            # 解析HTML内容
            # 解析HTML内容
            soup = BeautifulSoup(response.text, 'html.parser')

            # 查找简介部分
            # para_WzwJ3 content_XwoLS MARK_MODULE\J-lemma-content
            summary = soup.find('div', class_='lemmaSummary_s9vD3 J-summary')
            details = soup.find('div', class_='J-lemma-content')
            if summary:
                # 获取简介文本
                introduction = summary.get_text(strip=True)
            else:
                introduction = "未找到简介"
            if details:
                # 获取简介文本
                details_text = details.get_text(strip=True)
            else:
                details_text = "未找到其他资料"
            # 拼接两部分内容
            full_introduction = introduction + " " + details_text
            # 查找图片
            images = soup.find_all('img', class_='picture_cV667')
            image_paths = []
            for i, img in enumerate(images):
                img_url = img['src']
                if img_url.startswith('http'):
                    try:
                        img_data = requests.get(img_url).content
                        img_name = f'{spot}_{i}.jpg'
                        img_path = os.path.join(image_dir, img_name)
                        with open(img_path, 'wb') as img_file:
                            img_file.write(img_data)
                        image_paths.append(img_path)
                    except Exception as e:
                        print(f"下载图片失败: {img_url}, 错误: {e}")

            # 将景区名称、简介和图片路径写入CSV文件
            writer.writerow([spot, full_introduction, ', '.join(image_paths)])
            print(f"已爬取: {spot}")

        elif response.status_code == 404:
            print(f"404错误：{spot}")
            log_failed_location(spot)
        else:
            print(f"请求失败: {spot}, 状态码: {response.status_code}")




print(f"数据已保存到 {csv_file}")

