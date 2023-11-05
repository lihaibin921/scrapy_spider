# scrapy_spider 项目
本项目仅本人练习使用
## 项目结构说明   
本项目为scrapy项目   
+ datas: csv文件存储
+ local_html: 本地html测试用
+ log: 日志文件
+ py_test: python方法测试 , 无大用
+ scrapy_spider: scrapy结构
  + spiders : Spider文件, 数据解析逻辑
    + bili_* B站爬虫逻辑
  + spiders_test : 测试用
  + utils : 工具类
  + items.py : 数据模型
  + pipelines.py : 主要是存储逻辑 , DB操作
  + settings.py : 设置
+ sql : mysql DDL

---

## bilibili爬虫
>文件说明   
> scrapy_spider/spiders下
>>**bili_user_spider.py**   
> 用户基本信息爬虫  
> 优点: 信息比较全 , 缺点: 限流严重
> 
> >**bili_live_user_spider.py**  
> 主播信息爬虫   
> 优点: 几乎不限流 , 自带粉丝数 , 缺点: 信息量少
> 
> >**bili_user_cards_spiders.py**   
> 用户信息批量爬虫   
> 优点: 几乎不限流, 量大速度快 , 缺点: 几乎无缺点   
> 综合以上3个程序可以较好完成人口普查任务
> 
> >**bili_user_follow_spider.py**   
> 用户关注数, 粉丝数爬虫    
> 比较重要的数据, 但是完全没有访问限制挺离谱的
> 
>> **bili_user_readme.md**  
> 用户相关接口文档   
> 参考文档: [哔哩哔哩-api收集](https://github.com/SocialSisterYi/bilibili-API-collect)

---
### User-Agent
使用fake_useragent
    
    from user_agent import UserAgent
    
    ua = UserAgent()
    ua.chrome # 获得一个随机的chrome浏览器ua