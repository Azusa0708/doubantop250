from lxml import etree
import requests
import csv
import os
import time

fp = open('doubanbook.csv', 'wt', newline='', encoding='utf-8')

writer = csv.writer(fp)
writer.writerow(('name', 'url',  'author', 'publisher', 'date', 'price', 'rate', 'comment'))

urls = ['https://book.douban.com/top250? start={}'.format(str(i)) for i in range(0,250,25)]

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36'
                 '(KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
}

for url in urls:
    html = requests.get(url, headers=headers)
    selector = etree.HTML(html.text)
    # 取大标签，以此循环
    infos = selector.xpath('//tr[@class="item"]')

    for info in infos:
        name = info.xpath('td/div/a/@title')[0]  # 书名
        url = info.xpath('td/div/a/@href')[0]  # 链接
        book_infos = info.xpath('td/p/text()')[0]   
        author = book_infos.split('/')[0]  # 作者
        publisher = book_infos.split('/')[-3]  # 出版社
        date = book_infos.split('/')[-2]  # 出版时间
        price = book_infos.split('/')[-1]  # 价格
        rate = info.xpath('td/div/span[2]/text()')[0]  # 评分
        comments = info.xpath('td/p/span/text()')  # 评语
        comment = comments[0] if len(comments) != 0 else "空"
        # 写入数据
        writer.writerow((name, url, author, publisher, date, price, rate,comment))

# 关闭csv文件
fp.close()


#def spider(num):
#    num =  num * 25
#    url = 'https://book.douban.com/top250?start=' + str(num)
#    html = requests.get(url)

for i in range(10):
    i *= 25
    url = 'https://book.douban.com/top250?start=' + str(i)
    html = requests.get(url,headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
})
    selector = etree.HTML(html.text)
    pic_url = selector.xpath('//a[@class="nbg"]/img/@src')
    for each in range(0, len(pic_url)):
        time.sleep(0.1)
        pic = requests.get(pic_url[each])
        print(each)
        f = open('E://pythonpic//' + str(i + each) + '.jpg', 'wb')
        f.write(pic.content)
        f.close()   #图片提取保存