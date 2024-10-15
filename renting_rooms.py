import requests
import csv
from lxml import etree


def main():
    csvfilepath = 'crawl.csv'
    getData(csvfilepath)


def getData(csvfilepath):
    head = {
        "Cookie": "f=n; commontopbar_new_city_info=556%7C%E6%B4%9B%E9%98%B3%7Cluoyang; commontopbar_ipcity=luoyang%7C%E6%B4%9B%E9%98%B3%7C0; userid360_xml=63226CD4C488B4612A7CCA415FEE6165; time_create=1661081634551; id58=CocIJ2LOv3m4X1fRhY/DAg==; aQQ_ajkguid=3EDCDC81-7B5E-4F6F-8C2F-7DABDAFD1348; sessid=ABBD4809-9E9F-45ED-95C1-862EEAFB53D7; ajk-appVersion=; ctid=556; fzq_h=91e3ec8f25dd1406bc61b2a97f769b73_1658489614032_98fa3aa955c544e78ef3d56396c75d7b_47896385561765975701177718252511739399; 58tj_uuid=94e99d7b-f5fd-490e-9527-8d4e7244e894; new_uv=1; utm_source=; spm=; init_refer=; als=0; 58home=luoyang; f=n; new_session=0; xxzl_cid=44f564fa5d724ccd91387882f148211b; xzuid=fbd94eca-007c-4a45-b357-3f5c108e2646",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 SLBrowser/8.0.0.7062 SLBChan/103"
    }
    city = input("请输入你要查看的城市: ")
    page = input("请属于你要查询的页数: ")

    headers = ['名字', '地址', '介绍', '价格']
    with open(csvfilepath, 'w', encoding='utf-8', newline='') as f:
        f_csv = csv.writer(f)  # 创建csv.writer对象
        f_csv.writerow(headers)

    for i in range(1, int(page) + 1):
        baseurl = "https://{0}.lianjia.com/zufang/pg{1}".format(city, i)
        print("Crawling page {0}.........".format(i))
        req = requests.get(baseurl, headers=head)
        req_xpath = etree.HTML(req.text)

        # 获取名字
        housename = req_xpath.xpath('//h3[@class="property-content-title-name"]/@title')
        # print(housename)

        # 获取价格
        houseprice = req_xpath.xpath('//p[@class="property-price-average"]/text()')
        # print(houseprice)

        # 获取房地产名称
        # done
        houseName = req_xpath.xpath('//p[@class="content__list--item--title"]/text()')
        # print(houseName)

        # 获取房地产地段
        houseaddress = req_xpath.xpath('//p[@class="property-content-info-comm-address"]/span[@data-v-5d17340e]/text()')
        # print(houseaddress)
        Houseaddress = []
        for k in range(0, len(houseaddress), 3):
            for j in range(k + 3, len(houseaddress), 3):
                houseaddress1 = "-".join(houseaddress[k:j])
                Houseaddress.append(houseaddress1)
                break
        # print(Houseaddress)

        # csv文件保存
        rows = zip(houseName, Houseaddress, housename, houseprice)
        with open(csvfilepath, 'a', encoding='utf-8', newline='') as f:
            f_csv = csv.writer(f)  # 创建csv.writer对象
            for row in rows:
                f_csv.writerow(row)
    print("Completed!")


if __name__ == '__main__':
    main()
