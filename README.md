# Aclsm
#### 基于ansible开发的ansible web管理工具，集成了cmdb，和系统信息展示功能。

##### 页面化ansible实现了文件推送，添加机器后自动添加ssh key认证等功能，cmdb部分通过在ansible中添加的机器自动收集硬件信息入库

##### 更新日志：

- 2017.12.15 增加了pyalbook(roles)执行功能，修复部分bug

* [部署文档](https://gitee.com/weihaoxuan/Aclsm/wikis/pages?title=1%E3%80%81%E9%83%A8%E7%BD%B2%E6%96%B9%E6%B3%95&parent=) 

##### 部署环境:

- centos6版本+python2.7+django1.8

- 数据库推荐使用mysql，不推荐使用sqllite(如果您仅简单体验可以使用)

- ansible被控制端需要安装libselinux-python,执行yum install libselinux-python -y

### 系统截图：

- 登陆

![登陆](https://gitee.com/weihaoxuan/images/raw/master/aclsm/login.jpg "login")

- 首页

![首页](https://gitee.com/weihaoxuan/images/raw/master/aclsm/index.jpg "首页")

- 添加机器

![添加机器](https://gitee.com/weihaoxuan/images/raw/master/aclsm/jiqi.jpg "添加机器")

- cmdb

![cmdb](https://gitee.com/weihaoxuan/images/raw/master/aclsm/cmdb.jpg "cmdb")

![cmdb](https://gitee.com/weihaoxuan/images/raw/master/aclsm/cmdb2.jpg "cmdb")

- 通知

![tongzhi](https://gitee.com/weihaoxuan/images/raw/master/aclsm/tonghzi.jpg "tongzhi")

#### 部署方法

* [部署文档](https://gitee.com/weihaoxuan/Aclsm/wikis/pages?title=1%E3%80%81%E9%83%A8%E7%BD%B2%E6%96%B9%E6%B3%95&parent=) 
