from bs4 import BeautifulSoup  # 导入网页解析库
import requests  # 导入网页请求库
import time  # 导入时间库
import pandas as pd  # 导入数据处理库

headers = {
    'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2;.NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; InfoPath.3; .NET4.0C; .NET4.0E)',
    'Accept': 'image/webp,image/*,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'http://www.baidu.com/link?url=_andhfsjjjKRgEWkj7i9cFmYYGsisrnm2A-TN3XZDQXxvGsM9k9ZZSnikW2Yds4s&amp;amp;wd=&amp;amp;eqid=c3435a7d00006bd600000003582bfd1f',
    'Connection': 'keep-alive'}
page = ('pg')
hlist = []


def generate_city_url(user_in_city):
    """
    功能为根据所选城市生成访问的 url
    :param user_in_city: 选择的城市
    :return: 需要访问的 url
    """
    city_url = 'https://' + user_in_city + '.fang.lianjia.com/loupan/'
    return city_url


def html_content(url):
    """
    功能为根据需要访问的 url 访问页面并提取内容
    :param url: 需要访问的 url
    :return: 页面信息
    """
    page = ('pg')
    for i in range(1, 2):  # 获取1-100页的数据
        if i == 1:  # 第一页
            i = str(i)
            a = (url + page + i + '/')
            r = requests.get(url=a, headers=headers)
            print(a)
            html_info = r.content
        else:  # 后续页
            i = str(i)
            a = (url + page + i + '/')
            print(a)
            r = requests.get(url=a, headers=headers)
            html2 = r.content
            html_info = html_info + html2
        time.sleep(2)  # 加延时，防止返回超时
    return html_info


def list_info(html_info):
    """
    功能为根据页面信息提取有用的房屋信息
    :param html_info: 页面信息
    """
    soup = BeautifulSoup(html_info, 'html.parser')  # 解析 html 页面内容
    houses = soup.find_all(
        'div', attrs={'class': 'resblock-desc-wrapper'})  # 提取房屋的全部信息

    for house in houses:  # 遍历每一个房子的信息
        property_info = house.find(
            "div", attrs={"class": "resblock-name"})  # 楼盘信息
        property_name = property_info.a.get_text()  # 楼盘名称
        proterty_tag = property_info.find_all("span")  # 楼盘标签
        property_type = proterty_tag[0].get_text()  # 楼盘类型
        sales_status = proterty_tag[1].get_text()  # 销售状态
        location = house.find(
            "div", attrs={"class": "resblock-location"}).get_text()  # 位置信息
        rooms = house.find(
            "a", attrs={"class": "resblock-room"}).get_text()  # 房型
        area = house.find(
            "div", attrs={"class": "resblock-area"}).get_text()  # 面积
        tag = house.find(
            "div", attrs={"class": "resblock-tag"}).get_text()  # 标签
        price_info = house.find(
            "div", attrs={"class": "resblock-price"})  # 价格信息
        unit_price = price_info.find(
            "div", attrs={"class": "main-price"}).get_text()  # 单价
        total_price = price_info.find("div", attrs={"class": "second"})  # 总价
        if total_price is not None:  # 有总价
            total_price = total_price.get_text()
        else:  # 没有总价
            total_price = "暂无"
        h = {'property_name': property_name,
             'property_type': property_type,
             'sales_status': sales_status,
             'location': location.replace("\n", ""),
             'rooms': rooms.replace("\n", ""),
             'area': area,
             'tag': tag,
             'unit_price': unit_price,
             'total_price': total_price}
        hlist.append(h)


if __name__ == '__main__':
    user_in_city = input('输入抓取城市：')  # sz 表示深圳
    url = generate_city_url(user_in_city)  # 根据所选城市生成访问的 url
    print(url)
    hlist.append(
        {'property_name': "楼盘名称",
         'property_type': "物业类型",
         'sales_status': "销售状态",
         'location': "位置",
         'rooms': "房型",
         'area': "面积",
         'tag': "标签",
         'unit_price': "单价",
         'total_price': "总价"})
    html_info = html_content(url)  # 根据需要访问的 url 访问页面并提取内容
    list_info(html_info) # 根据页面信息提取有用的房屋信息
    house_info = pd.DataFrame(hlist,
                              columns=['property_name',
                                       'property_type',
                                       'sales_status',
                                       'location',
                                       'rooms',
                                       'area',
                                       'tag',
                                       'unit_price',
                                       'total_price'])
    house_info.to_csv('链家房源.csv', index=False, encoding="utf_8_sig")
