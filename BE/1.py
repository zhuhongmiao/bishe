# https://api.swatchon.com/api/mall/v1/search/qualities?page=1
# https://api.swatchon.com/api/mall/v1/qualities/55402

# 1. 获取所有数据
# 2. 将数据写入csv文件
# 3. 将数据写入数据库

import requests
import json
from tqdm import tqdm
import pandas as pd
import os

MAX_PAGE = 394

def getDetail(id):
    url = f"https://api.swatchon.com/api/mall/v1/qualities/{id}"    
    response = requests.request("GET", url)
    data = response.json()
    return data

def getOnePage(page):
    url = f"https://api.swatchon.com/api/mall/v1/search/qualities?page={page}"    
    response = requests.request("GET", url)
    datas = response.json()['items']
    return datas

def current_status_to_file(status, filename='status.json'):
    with open(filename, 'w') as f:
        json.dump(status, f)
        f.close()
    print(f'{status["current_page"]},has done.')

def get_status_from_file(filename='status.json'):
    try:
        with open(filename, 'r') as f:
            status = json.load(f)
            f.close()
        print(f"Current status loaded from {filename}")
        return status
    except FileNotFoundError:
        print(f"{filename} not found.")
        return None

def write_data_to_csv(data, filename='data.csv'):
    if os.path.exists(filename):
        old_data = pd.read_csv(filename)
        combined_data = pd.concat([old_data, pd.DataFrame(data)], ignore_index=True)
        combined_data.to_csv(filename, index=False)
    else:
        pd.DataFrame(data).to_csv(filename, index=False)

def main():
    status = get_status_from_file()
    current_page = status['current_page']+1 if status else 1
    for page in range(current_page, MAX_PAGE + 1):
        print(f'Processing page {page}...')
        datas = getOnePage(page)
        current_page_data = []
        for data in tqdm(datas):
            detail = getDetail(data['id'])
            current_page_data.append({
                'id':detail['id'],
                'title':detail['title'],
                'category_name':detail['categories'][0]['name'],
                'category_id':detail['categories'][0]['id'],
                'weight':detail['metric']['weight'],
                'country':detail['store']['country']['name'],
                'price':detail['qualityPriceTagGroups']['standardOrder']['qualityPriceTags'][0]['salePriceBeforeDiscount'],
                'pattern':detail['patterns'][0]['name']
            })
        print(current_page_data)
        write_data_to_csv(current_page_data)
        current_status_to_file({'current_page': page})


if __name__ == "__main__":
    main()

