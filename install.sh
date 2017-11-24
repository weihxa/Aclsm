#!/bin/bash
echo 'export PYTHONOPTIMIZE=1' >> /etc/profile
echo 'export C_FORCE_ROOT=1' >> /etc/profile
source /etc/profile
python manage.py makemigrations
python manage.py migrate
echo "from Integrated.models import UserProfile as User; User.objects.create_superuser('ACLSM', 'aclsm@aclsm.com', 'aclsm')" | python manage.py shell
echo '默认登录账号密码为：aclsm@aclsm.com/aclsm'