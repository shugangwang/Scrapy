# Scrapy

## 1 何谓爬虫

爬虫用于提取网页的特定信息。也叫做网页蜘蛛。

## 2 requests 库

requests 是用于网页请求的库。

## 3 BeautifulSoup 库

BeautifulSoup 是用于网页解析库的库。

### 3.1 正则表达式

适用于简单数据的匹配，如果匹配内容较复杂，正则表达式写起来会很绕，同时页面内容稍微变化，正则就会失效。

### 3.2 Lxml

Lxml 是专门用来解析 XML 格式文件的库，该模块用 C 语言编写，解析速度很快，和正则表达式速度差不多，但是提供了 XPath 和 CSS 选择器等定位元素的方法

### 3.3 Beautiful Soup

这是一个 Python 实现的解析库，相比较于前两种来说，语法会更简单明了一点，文档也比较详细。唯一的一点就是运行速度比前两种方式慢几倍，当数据量非常大时相差会更多。

## 4 爬虫例程

01 爬取链家网站房产信息 [lianjia](https://github.com/shugangwang/Scrapy/blob/master/01lianjia)