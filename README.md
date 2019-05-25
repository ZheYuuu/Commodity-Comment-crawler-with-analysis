# Commodity-Comment-crawler-with-analysis
京东天猫商品评论爬取及分析系统，该系统能实时响应使用者需求抓取对应商品相关信息，并进行后续分析。<br>
整体采用DjangoMTV进行架构，在前端引入Vue以单组件模式来设计响应式布局的template，在后端仍以Django-View为基础，配置Django自带路由映射进行渲染。
爬取模块使用scrapyd部署scrapy，并用Django的standalone模式来唤起爬虫进程。
分析模块完成分词、清洗筛选等一系列操作后，使用tf-idf算法进行关键词提取，同时借助gensim进行LDA建模分析，提取潜在主题。
前后端的数据交互使用Axios实现。数据库采用Mysql，数据抓取存储至Mysql数据库使用adbapi异步多线程提高效率。
## 部署运行
* 进入GraduationProject/setting.py，进行数据库配置
* 进入项目，运行Django本地服务器：
```python manage.py runserver```
* 运行Scrapyd服务：
```scrapyd```
* 进入spiderApp/JDSpider，部署scrapy项目原型：
```scrapyd JD -p JDSpider```
## 环境需求
|名称|版本|作用|
|--|--|--|
|Django|2.0.4|搭建系统整体框架
|vue|2.6.10|完善系统前端
|axios|0.18.0|前后端数据交互
|beautifulsoup4|4.6.0|解析获取DOM元素
|gensim|3.2.0|生成LDA主题模型
|jieba|0.39|分词与关键词提取
|pandas|0.22.0|数据处理
|numpy|1.16.3|数据处理
|Scrapy|1.3.3|爬虫任务搭建
|scrapyd|1.2.0|爬虫任务部署调度
|Twisted|18.9.0|网络引擎
|mysql|5.5.18|数据存储



