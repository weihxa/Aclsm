#!/bin/bash

######配置区#######

mysqlusername='root'
mysqlpassword='123456'
mysqlip=127.0.0.1
###################

echo '设置环境变量'
echo 'export PYTHONOPTIMIZE=1' >> /etc/profile
echo 'export C_FORCE_ROOT=1' >> /etc/profile
source /etc/profile


echo '开始创建数据库及账户'
sed -i.bak "s/100.100.100.100/$mysqlip/" xbmanIntegrated/settings.py
mysql -h $mysqlip -u$mysqlusername -p$mysqlpassword  <<EOF 2>/dev/null
    CREATE DATABASE aclsm CHARACTER SET utf8 COLLATE utf8_general_ci;
    grant all privileges on aclsm.* to aclsm@* identified by 'aclsm.com';
    flush privileges;
EOF
echo '初始化数据库表和登陆账户'
python manage.py makemigrations
python manage.py migrate
echo "from Integrated.models import UserProfile as User; User.objects.create_superuser('ACLSM', 'aclsm@aclsm.com', 'aclsm.com')" | python manage.py shell
echo 'mysql登录账号密码为：aclsm/aclsm.com'
echo '默认登录账号密码为：aclsm@aclsm.com/aclsm.com'
