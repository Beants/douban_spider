#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/9/25 8:44 PM
# @Author : maxu
# @Site : 
# @File : __init__.py.py
# @Software: PyCharm

from py2neo import Node, Graph, Relationship

graph = Graph('http://localhost:7474', username='neo4j', password='microxu1234')


class Movie:
    def __init__(self, title=None, rating_num=None, url=None, inq=None, year=None, country=None, type=None):
        self.title = title
        self.url = url
        self.inq = inq
        self.rating_num = rating_num
        self.year = year
        self.country = country
        self.type = type

    def toString(self):
        return {"title": self.title, "rating_num": self.rating_num, 'url': self.url, 'inq': self.inq, 'year': self.year,
                'country': self.country, 'type': self.type, }


def getMovieDetail(url):
    pass


# 获取每一页的
def getMovieList(url):
    import requests
    from bs4 import BeautifulSoup
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
        'Cookie': 'bid=2OUBnLbgwI8; douban-fav-remind=1; ll="108288"; __yadk_uid=qY6FqKpnzTULuWZTY6nVHfkaDKcG35d3; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1576823566%2C%22https%3A%2F%2Fblog.csdn.net%2FChen18125%2Farticle%2Fdetails%2F84101458%22%5D; _pk_ses.100001.4cf6=*; __utma=30149280.906741169.1576823567.1576823567.1576823567.1; __utmb=30149280.0.10.1576823567; __utmc=30149280; __utmz=30149280.1576823567.1.1.utmcsr=blog.csdn.net|utmccn=(referral)|utmcmd=referral|utmcct=/Chen18125/article/details/84101458; __utma=223695111.1356716386.1576823567.1576823567.1576823567.1; __utmb=223695111.0.10.1576823567; __utmc=223695111; __utmz=223695111.1576823567.1.1.utmcsr=blog.csdn.net|utmccn=(referral)|utmcmd=referral|utmcct=/Chen18125/article/details/84101458; ap_v=0,6.0; _pk_id.100001.4cf6=69f3ecc1bfb4bb41.1575270421.3.1576825044.1575272816.'}
    headers.pop('Cookie')
    # 获取html源代码
    html = requests.get(url, headers=headers).text
    # print('html',url,html)
    # 调用解析器 解析 html 源代码
    soup = BeautifulSoup(html, "html.parser")
    movies = soup.find('ol', class_="grid_view").find_all('li')
    moviesList = []

    for item in movies:
        title = [x.text.replace('\xa0', '').replace(' ', '').replace('/', '') for x in
                 item.find_all("span", class_="title")]
        rating_num = float(item.find("span", class_="rating_num").text)
        url = item.find("div", class_="hd").a['href']
        title += item.find("span", class_="other").text.replace('\xa0', '').replace(' ', '').replace("(港 / 台)",
                                                                                                     "(港\台)").split('/')
        title.remove('')

        inq = item.find("span", class_="inq").text
        note = item.find("div", class_="bd").p.text.replace('\xa0', '').split('\n')[2].split('/')
        year = int(note[0].replace('(中国大陆)', ''))
        country = note[1].split(' ')
        type = note[2].split(' ')
        print(year, country, type)

        movie = Movie(title=title, rating_num=rating_num, url=url, inq=inq, year=year, country=country, type=type)
        moviesList.append(movie)
        print(movie.toString())
    return moviesList


# 主函数
# __name__ python 基础里面讲的
def setDate():
    graph.delete_all()

    url = "https://movie.douban.com/top250?start="
    start = 0
    moviesList = []
    while start < 250:
        moviesList += getMovieList(url + str(start))
        start += 25
    print(moviesList.__len__())
    # moviesList=moviesList[:10]
    titles = []
    titles_r = []
    rating_nums = []
    urls = []
    inqs = []
    years = []
    countrys = []
    types = []
    for movie in moviesList:

        titles.append(movie.title[0])
        for i in movie.title[1:]:
            titles_r.append(i)
        rating_nums.append(movie.rating_num)
        urls.append(movie.url)
        inqs.append(movie.inq)
        years.append(movie.year)

        countrys += movie.country
        types += movie.type

    titles = list(set(titles))
    titles_r = list(set(titles_r))
    rating_nums = list(set(rating_nums))
    urls = list(set(urls))
    inqs = list(set(inqs))
    years = list(set(years))
    countrys = list(set(countrys))
    types = list(set(types))

    node_titles = [Node('电影名', name=x) for x in titles]
    node_titles_r = [Node('译名', name=x) for x in titles_r]
    node_rating_nums = [Node('评分', name=x) for x in rating_nums]
    node_urls = [Node('链接', name=x) for x in urls]
    node_inqs = [Node('评语', name=x) for x in inqs]
    node_years = [Node('年份', name=x) for x in years]
    node_countrys = [Node('国家', name=x) for x in countrys]
    node_types = [Node('类型', name=x) for x in types]

    def reg(nodes):
        for node in nodes:
            graph.create(node)

    reg(node_titles)
    reg(node_titles_r)
    reg(node_rating_nums)
    reg(node_urls)
    reg(node_inqs)
    reg(node_years)
    reg(node_countrys)
    reg(node_types)

    for movie in moviesList:
        root = node_titles[titles.index(movie.title[0])]
        for i in movie.title[1:]:
            r1 = Relationship(root, '又名', node_titles_r[titles_r.index(i)])
            graph.create(r1)
        r1 = Relationship(root, '评分为', node_rating_nums[rating_nums.index(movie.rating_num)])
        graph.create(r1)

        r1 = Relationship(root, '豆瓣链接为', node_urls[urls.index(movie.url)])
        graph.create(r1)

        r1 = Relationship(root, '评语为', node_inqs[inqs.index(movie.inq)])
        graph.create(r1)

        r1 = Relationship(root, '出版年份', node_years[years.index(movie.year)])
        graph.create(r1)
        for i in movie.country:
            r1 = Relationship(root, '出版国家', node_countrys[countrys.index(i)])
            graph.create(r1)

        for i in movie.type:
            r1 = Relationship(root, '类型', node_types[types.index(i)])
            graph.create(r1)


def setData2():
    graph.delete_all()

    url = "https://movie.douban.com/top250?start="
    start = 0
    moviesList = []
    while start < 250:
        moviesList += getMovieList(url + str(start))
        start += 25
    print(moviesList.__len__())
    # reg(node_titles)
    # reg(node_titles_r)
    # reg(node_rating_nums)
    # reg(node_urls)
    # reg(node_inqs)
    # reg(node_years)
    # reg(node_countrys)
    # reg(node_types)
    for movie in moviesList:
        temp = Node('moive', title=movie.title[0], title_r=movie.title[1:], rating_num=movie.rating_num, url=movie.url,
                    inq=movie.inq, year=movie.year, country=movie.country, type=movie.type)
        graph.create(temp)


if __name__ == '__main__':
    # a = Node('电影名')
    # relMatch = RelationshipMatcher(graph)
    #
    # for i in list(relMatch.match(r_type='year')):
    #     print(i)
    # setDate()
    # f1 = Node('电影名')
    # f2 = Node('国家')
    res=graph.run('MATCH p=(t2:`电影名`)-[r:`出版国家`]->(c1:`国家`),q= (t1:`电影名`)-[r:`出版国家`]->(c2:`国家`) where  t1.name=t2.name RETURN c1,c2  LIMIT 250').to_table()
    print(res)
# MATCH p=(t:`电影名`)-[r:country]->(c:`国家`),q= (x:`电影名`)-[r1:type]->() where   t.name=x.name RETURN p,q  LIMIT 250
# MATCH p=shortestpath((:`国家` {name:"美国"})-[*..100]-(:`国家`{name:"英国"}))RETURN p
# MATCH p=(a:`电影名`)-[r:`出版国家`]->(c:`国家`{name:"美国"}),(b:`电影名`)-[r1:`出版年份`]->(n:`年份`)  where n.name>2010  and a.name=b.name RETURN p
