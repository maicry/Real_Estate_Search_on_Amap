from bs4 import BeautifulSoup
import requests
import csv
import time
import lxml

def main():
    # 待爬取的网址
    url = "https://bj.58.com/pinpaigongyu/pn/{page}/?minprice=2000_4000"
    # 定义请求头，防止被反爬
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'
    }
    # 用于存储爬取的数据
    csv_file = open("house.csv", "w", encoding="utf-8")
    csv_writer = csv.writer(csv_file, delimiter=',')
    # 爬取20页数据
    for page in range(0, 20):
        page += 1
        print("正在爬取第" + str(page) + "页信息........")
        print("URL: ", url.format(page=page))
        # 等待3秒，防止被拒绝访问
        time.sleep(3)
        response = requests.get(url.format(page=page),headers=headers)
        response.encoding = 'utf-8'
        html = BeautifulSoup(response.text,features="lxml")
        # 选择到房源信息对应的html标签
        house_list = html.select(".list > li")
        for house in house_list:
            house_title = house.select("img")[0]["alt"]
            house_url = house.select("a")[0]["href"]
            house_info_list1 = house_title.split('-')

            # 如果第二列是公寓名或者社区则取第一列作为地址
            if "公寓" in house_info_list1[0] or "社区" in house_info_list1[0]:
                house_info_list2 = house_info_list1[0].split(' ')
                house_info_list2 = house_info_list2[0].replace('【','')
                house_info_list2 = house_info_list2.replace('】', '｜')
            else:
                house_info_list2 = house_info_list1[0]
            print(house_info_list2 + " " + house_url)

            house_location = house_info_list2.replace('｜',' ')
            house_info_list = house_location.split(' ')
            print(house_info_list)

            house_url = "https://bj.58.com" + house_url
            # 有些房源信息长度不够，需要判断，防止报错
            if len(house_info_list) <= 1:
                house_info_list.insert(1, "暂无数据")
            # 写入csv文件
            csv_writer.writerow([house_info_list[1], house_url])
    csv_file.close()


if __name__ == '__main__':
    main()