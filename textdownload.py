import requests, re
from bs4 import BeautifulSoup

def get_content(url):
    res = requests.get(url, timeout=500)  # 设置超时
    htmlcont = res.content.decode("gb2312", "ignore")
    # print(htmlcont)
    soupcont = BeautifulSoup(htmlcont, 'lxml')  # lxml解析器/效率高
    # 标题名字
    # name = soupcont.find_all('div', style='float:left;width:713px;padding-left: 0px; padding-top:14px;font-size:16px;')
    contents = soupcont.select('.noveltext')  # 筛选div获取内容部分
    # contentstr = contents[0].get_text()  # 直接获取文本内容 格式很乱
    contentstr = str(contents[0])  # 连带着标签等
    pattern = re.compile('.*?<br/>')  # 以br为结尾的
    conts = re.findall(pattern, contentstr)  # 返回的是列表 /不带括号 内容为字符串

    conts[0] = conts[0].lstrip()  # 去除左边多余空格
    conts[0] = '      '+conts[0]  # 为了好看再加几个
    for i in range(len(conts)):
        conts[i] = conts[i].replace('<br/>', '\n')  # 替换<br/>

    return conts

# https://m.jjwxc.net/my/login?login_mode=jjwxc 手机版登陆无验证码
response = requests.get('http://www.jjwxc.net/onebook.php?novelid=3354975')

names = []  # 章节名
urls = []  # 章节链接
nums = 0  # 章节数

# 章节
# text返回Unicode型
# content返回bytes型
html = response.content.decode("gb2312", "ignore")
#print(html)
soup = BeautifulSoup(html, 'lxml')  # lxml解析器/效率高
table = soup.find_all('table', class_='cytable')  # 筛选出目录区域
tr_bf = BeautifulSoup(str(table[0]), 'lxml')
a = tr_bf.find_all('a', itemprop='url')  # 筛选出章节链接,find_all返回集合，可遍历
for i in a:
    # print(i)
    names.append(i.string)
    # print(i.string)
    if i.get('href') != None:
        urls.append(i.get('href'))  # 获取章节链接（未入v部分）
        nums = nums+1

# 内容

for i in range(nums):
    #print(get_content(urls[i]))
    with open('小太后1.txt', 'a', encoding='utf-8') as f:
        f.write('第'+str(i+1)+'章  '+names[i] + '\n')
        f.writelines(get_content(urls[i]))
        f.write('\n\n\n\n')
#print(names[0])



