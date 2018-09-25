#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/9/25 8:44 PM
# @Author : maxu
# @Site : 
# @File : __init__.py.py
# @Software: PyCharm
class Movie:
    def __init__(self, title=None, rating_num=None):
        self.title = title
        self.rating_num = rating_num

    def toString(self):
        return {"title": self.title, "rating_num": self.rating_num}


def getMovieDetail(url):
    pass


# 获取每一页的
def getMovieList(url):
    import requests
    from bs4 import BeautifulSoup

    # 获取html源代码
    html = requests.get(url).text
    # 调用解析器 解析 html 源代码
    soup = BeautifulSoup(html, "html.parser")
    movies = soup.find('ol', class_="grid_view").find_all('li')
    moviesList = []
    for item in movies:
        title = item.find("span", class_="title").text
        rating_num = item.find("span", class_="rating_num").text
        movie = Movie(title=title, rating_num=rating_num)
        moviesList.append(movie)
    return moviesList


# 主函数
# __name__ python 基础里面讲的
if __name__ == '__main__':
    url = "https://movie.douban.com/top250?start="
    start = 0
    if start < 250:
        moviesList = getMovieList(url)
        start += 25
