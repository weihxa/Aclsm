#!/bin/bash
echo '初始化数据库表和登陆账户'
python manage.py makemigrations
python manage.py migrate
echo "from Integrated.models import UserProfile as User; User.objects.create_superuser(username='ACLSM', email='aclsm@aclsm.com', password='aclsm.com')" | python manage.py shell
echo '默认登录账号密码为：aclsm@aclsm.com/aclsm.com'
