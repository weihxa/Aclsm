# Aclsm

host_key_checking = False

export PYTHONOPTIMIZE=1


echo "from Integrated.models import UserProfile as User; User.objects.create_superuser('ACLSM', 'aclsm@aclsm.com', 'aclsm')" | python manage.py shell

python manage.py celery worker -c 5 -B --loglevel=info