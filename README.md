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
cd winter19.team12/fitbit_monitor/
docker-compose build
```
If the error `ERROR: Couldn't connect to Docker daemon at http+docker://localunixsocket - is it running?` appears, try running `dockerd` command and retry building.  
Finally start the container using : `docker-compose up`
