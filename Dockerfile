FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN apt-get update
RUN apt-get install -y apt-utils vim curl apache2 apache2-utils
RUN apt-get -y install certbot python-certbot-apache
RUN apt-get -y install python3 libapache2-mod-wsgi-py3
RUN apt-get -y install python3-pip
RUN ln /usr/bin/pip3 /usr/bin/pip
RUN pip install django ptvsd
RUN mkdir /code
COPY . /code/
RUN chown -R :www-data /code
ADD ./demo_site.conf /etc/apache2/sites-available/000-default.conf
ADD ./demo_site.conf /etc/apache2/sites-available/000-default-le-ssl.conf
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
CMD ["apache2ctl", "-D", "FOREGROUND"]
