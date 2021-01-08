[![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/TinkerPal99/PiCentral)

# PiCentral

This is a new version of my [ZPE](https://github.com/TinkerPal99/ZentraleProzessEinheit) using FLASK and a REST-API as 
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

Now build the datacollector
``` bash
docker build -t dtclltr datacollector
```
##Run the application

Well, just run the docker compose

```bash
docker-compose up
```

## The Database has to be set up
Still looking into autmating this one. Ideas welcome, but until then

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

CREATE TABLE active_vehicles (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(20) NOT NULL,
PRIMARY KEY (id))

CREATE TABLE collected_data (
    timeuuid INT NOT NULL,
    collector VARCHAR(20) NOT NULL,
    reading FLOAT,
PRIMARY KEY (timeuuid))

```

Now it's done and the whole application is up.

## What can I do ?
Welp, what you can do ? No idea, but for me this will be a central point for my PiFleet.
A crowd of diffirent drones and rover which will get and send information from/to this central point.

Of course the application will grow to achieve this goal, but here are the endpoints you can reach so far.
As seen in the docker-compose, the apis are only reachable through proxy. FOr this I use the dockerimage pottava/proxy

management

   Admin sst is for user acess, 
       GET /duty lists all vehicles that are currently in use
       GET /avail lists all available hardware informationsheets 
       GET /ib/add/<modell> add a new ib for <modell> here, in the moment, only json is supported
        Minimal IB like this, Multiple IBs can be added by one update
        If minimal IB is given, status will be set as inactive
```json
{
"mobile":{
        "Name": "xyz",
        "Status": "Inactive"
         }
}
```

   Vehicle sst
       GET /ib/<modell> returns modell-hardware informationsheet and sets vehicle on active duty
       DELETE /ib/<modell takes modell from active duty

datacollector
   
   POST /up upload data here, using following json-form
      ```
      {
      "collector": "postman",
      "reading": "36.0"
      }
      ```

   GET /data returns collected data


### What will come next ?
Of course I will add an interface to add or delete hardware informationsheets.
Also I'll write a more understandable documentation of the whole project and what I want to do.
Purpose of this project nevertheless will be to build something just because I can and want to try things out.
I am also looking into deploying this thing, maybe on a raspberry pi or an azure Cloudservice ...
And after that ? Well, I'll see ...