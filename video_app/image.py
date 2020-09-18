# from lxml import etree
# import requests
#
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
# }
# for i in range(1, 11):
#     url = 'http://www.nipic.com/photo/lvyou/ziran/index.html?page=%d' % i
#     response = requests.get(url, headers=headers)
#     html = etree.HTML(response.text)
#     lis = html.xpath("//ul[@class='new-search-result-box clearfix']/li")
#     for li in lis:
#         image_url = li.xpath('.//img/@data-src')
#         if image_url:
#             with open('image_url.txt', 'a') as f:
#                 f.write(image_url[0] + '\n')
