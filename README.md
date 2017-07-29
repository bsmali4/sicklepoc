# sicklepoc

插件扫描器
1.优势
对作业调度做了优化，保持了并发量
2.不需要数据库
生成可视化模版
3.会对端口进行探测和扫描

##关于sicklepoc
早在去年，我就做了一款扫描器。包含对子域名的收集，邮件收集，爬虫检测漏洞模块之类的，只是没有公开。当我腾出精力来做sickle的时候，我对sickle的理解是poc扫描+web2.0爬虫。为了提高复用性，我决定把poc和crawler分开来，并且做成了分布式部署的模式。这样做带来的好处太明显了，支持无限台机器扫描，你的机器越多，面对众多扫描目标时，扫描起来也毫不费力。sicklepoc当然这只是一个sickle项目中的一部分。sicklepoc是一个单纯的poc扫描框架。现在poc扫描有很多，pocscan,scan-t,迅风之类的，太多太多。sicklepoc，你可以把它理解为一个插件扫描器。整个过程：输入目标->扫描->出报告。
##关于sickle
关于sickle，是一个集资产收集，poc，爬虫扫描的工具。插件式的扫描模式对于后期拓展漏洞检测能力帮助实在是太大了。分布式的部署可以大大提高扫描的速度，这个东西不会开源。不过sickle的衍生版flycat后期会开源。关于flycat详情可以参考http://www.codersec.net/2017/02/flycat%E7%B3%BB%E7%BB%9F%E7%9A%84%E9%9A%8F%E6%83%B3/ 由于第一版的flycat采用的是ssh框架，struts2漏洞太多了，在第二版的时候，我换成了springmvc，hibernate也换成了mybatis。
#安装方法
把整个项目拷到目录
centos的安装环境请运行SickleInstallCentos.bash

ubuntu的请运行SickleInstallUbuntu.bash
#功能
探测服务
扫描端口后调用插件扫描
#使用方法
![](http://i2.muimg.com/567571/e35d26f5919abd84.png)
target指定模式
1.列出可用插件  python main.py --list
2.target指定目标或者file指定目标
3.指定插件
4.指定扫描等级
5.是否开启debug模式
完整例子
python main.py --file target.txt --plugins tomcat,redis --level 4
这里要注意一个问题，一次扫描目标不要超过50个，由于发布的是sickepoc不带数据库版本，所以整个原理都是用的序列化对象存储，太多了，反序列化出报告的时候会很慢。sickle不会有这个问题，因为sickle是以mysql储存的。
#查看报告
所有的报告生成会在source/sicklepoc.html中

![](http://i1.piimg.com/567571/91a4c244d14e2d60.png)
![](http://i1.piimg.com/567571/7e0aa023b28bf7b6.png)
![](http://i4.buimg.com/567571/a7c5a89e392262ad.png)
![](http://i2.muimg.com/567571/0dd80726c1a6d24c.png)

#感想
如何优雅的写代码很重要，在开发sickle中用到了很多设计模式的东西，现在回过头来看，设计模式真的是很精妙。
如果有时间，我会把整个开发过程遇到的问题以及怎么去解决的分享出来。

#下载
https://github.com/bsmali4/sicklepoc
