# PiCentral

This is a new version of my [EZB](https://github.com/TinkerPal99/ZentraleProzessEinheit) using FLASK and a REST-API as 
well as a database.

Deploying is now much easier because of Docker, just build the images, run the docker-compose, set up the database and 
done :)

##Build images
You'll need docker for this ;) 


There are 2 images to build, one is the actual REST-API.

Path are relative from root

```bash
docker build -t mgmt MGMT
```

Then the second is to build the db-image

``` bash
docker build -t db database
```

##Run the application

Welp, just run the docker compose

```bash
docker-compose up
```

## The Database has to be set up
Stilllooking into autmating this one. Ideas welcome, but until then

1. open localhost:8080
2. log in with these credentials
    - system: MySQL
    - server: db
    - username: root
    - password: test
    - database: none
3. Now choose "SQL command" on the left handside and put in this
``` MySQL
CREATE DATABASE picentral;

USE picentral;

CREATE TABLE active_vehicles (id INT NOT NULL AUTO_INCREMENT,
name VARCHAR(20) NOT NULL,
PRIMARY KEY (id))

```

Now it's done and the whole application is up.

## What can I do ?
Welp, what you can do ? No idea, but for me this will be a central point for my PiFleet.
A crowd of diffrent drones and rover which will get and send information from/to this central point.

Of course the application will grow for this reason, but here are the endpoints you can reach so far.

```
vehicle administrator
Admin sst is for user acess, 
    GET /duty lists all vehicles that are currently in use
    GET /avail lists all available hardware informationsheets

Vehicle sst
    GET /ib/<modell> returns modell-hardware informationsheet and sets vehicle on active duty
    DELETE /ib/<modell takes modell from active duty
```

### What will come next ?
Of course I will add an interface to add or delete hardware informationsheets.
Also I'll write a more understandable documentation of the whole project and what I want to do.
Purpose of this project nevertheless will be to build something just because I can and want to try things out.
I am also looking into deploying this thing, maybe on a raspberry pi or an azure Cloudservice ...
And after that ? Well, I'll see ...