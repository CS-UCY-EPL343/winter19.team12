# winter19.team12 Fitbit smart watch metrics monitoring and displaying in graphs.

Webserver Backend : Django framework which runs inside docker  
Website Frontend: Vue JS framework  
Mobile application: Fitbit SDK using javascript. Can be compiled and ran on a simulation or an actual fitbit smartwatch at https://studio.fitbit.com

# Running the server
Tested using ubuntu.  
First you will need to install docker and docker-compose:  
```
sudo apt-get update
sudo apt-get install docker
sudo apt-get install docker-compose
```

Then you will need to build the docker container:
```
cd winter19.team12
docker-compose build
```
If the error `ERROR: Couldn't connect to Docker daemon at http+docker://localunixsocket - is it running?` appears, try running `dockerd` command and retry building.  
Finally start the container using : `docker-compose up`

#Configuring apache server and making ssl certificate

```
sudo docker ps
```
Find the container id of the webserver  
Enter in docker with the id  
```
sudo docker exec -ti #id /bin/sh  	
```
Configure apache    
```
vim /etc/apache2/apache2.conf	//delete the row required denied all
vim /etc/apache2/sites-available/000-default.conf	//change the DNS name
```
Create ssl certificate  
```
certbot --apache	
```
Answer the questions with A,N,1,2  
Restart the apache  
```
apachectl restart
```
Configuring Quasar  


Enter container with id if not in the container of web
```
sudo docker exec -ti #id /bin/sh		
apt-get update
apt-get install npm
npm install npm@latest -g
npm install -g @quasar/cli
quasar dev& 
```







