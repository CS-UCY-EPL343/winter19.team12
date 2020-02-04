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
RUN apt-get -y install npm
WORKDIR /code/fitbit_frontend
RUN npm install npm@latest -g
RUN npm install -g @quasar/cli
RUN npm install @amcharts/amcharts4
RUN npm install axios
RUN npm install
WORKDIR /code
COPY sites-available /etc/apache2/sites-available/
ADD letsencrypt.tar.gz /etc
RUN a2enmod ssl
# RUN a2ensite /etc/apache2/sites-available/ssl.conf
RUN sed -i '/Require all denied/d' /etc/apache2/apache2.conf
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
WORKDIR /etc/apache2/sites-available
RUN a2ensite ssl.conf
WORKDIR /code
CMD ["apache2ctl", "-D", "FOREGROUND"]
