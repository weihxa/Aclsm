#Version 0.1
FROM centos
MAINTAINER weihxa
#ADD CentOS7-Base-163.repo /etc/yum.repos.d/CentOS-Base.repo
#RUN yum clean all && yum makecache
RUN yum -y install epel-release && yum install -y python-pip && yum install -y gcc libffi-devel python-devel openssl-devel
#WORKDIR /
#RUN yum install -y git
#RUN git clone https://git.oschina.net/weihaoxuan/xbman-Integrated.git
#ADD pip.conf ~/.pip/pip.conf
RUN pip install Django==1.8.3
RUN pip install python-jenkins==0.4.13
RUN pip install ansible==1.9.6
RUN pip install celery==3.1.17
RUN pip install django-celery==3.1.17
RUN pip install gunicorn
VOLUME /xbman-Integrated /xbman-Integrated
CMD cd /xbman-Integrated && gunicorn  -w 2 xbman-Integrated.wsgi:application -b 0.0.0.0:8080 --reload --log-level=INFO --timeout=100
EXPOSE 8080