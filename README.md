# Team Aqua Project Repository

  *Project Website*: https://3.18.84.86/ (This is the deployed version of the product)
  
  *Team Website* : https://team-aqua.wixsite.com/aqua/

## Files

The deliverable files are in the respective deliverable folders numbered. The snapshots of the burndown chart and task board are in the **Burndown and Task Board** folder.

## Development

`client-server` contains the Angular pageserver (frontend) and `server` contains the Django server for endpoints and database connection to MongoDB (backend).

#### Prerequisites
Docker is installed and running.

### To launch the Angular Pageserver:

*In development configuration:*
```
cd client-server && docker-compose -f docker-compose.yml up -d client-dev
```

*In production configuration:*
```
cd client-server && docker-compose -f docker-compose.yml up -d client-prod
```

### To launch the Django Server:
```
cd server && docker-compose -f docker-compose.yml up -d server
```

## Documentation

`sd-site` contains the Docusaurus for documentation of backend and frontend components. 

#### Prerequisites

[yarn](https://classic.yarnpkg.com/en/docs/install/) is installed.

### To launch the documentation site:
```
cd sd-site && yarn start
```

## Deployment Instructions:

### Prerequisites:
Accounts must exist with the _Free Tier privileges_ on:
- Amazon Web Services(AWS)
- Mongodb atlas
- Dockerhub
- Docker latest stable version, nodejs v 12.6.2, angular CLI v 9.1.9, and python v 3.8.3 installed and working on your development machine
- an SSH client

### Create a new AWS EC2 Ubuntu instance:

access the LAUNCH INSTANCE WIZARD from: https://us-east-2.console.aws.amazon.com/ec2/v2/home?region=us-east-2#LaunchInstanceWizard:
or by going to the aws ec2 instance dashboard and selecting Launch Instance

Select Ubuntu 18.0.4 LTS as your operating system of choice, leave the default settings
*MAKE SURE TO KEEP THE API KEY GENERATED FOR THE INSTANCE AS YOU WILL NEED IT FOR SSH ACCESS*

return to the instance dashboard and move to the security groups heading for the instance which was just created
proceed to inbound rules -> edit inbound rules, allow the following inbound traffic:
HTTP from all sources
HTTPS from all sources
NFS from the default security group
if SSH is not already present allow it from all sources

### Whitelist the IP of the aws instance on mongodb atlas
    https://docs.atlas.mongodb.com/security-whitelist/

### Optionally, apply an elastic ip to your EC2 instance
This is done so that the instance's IP stays the same across restarts
Note that this will cost $0.01/hr for every hour that the elastic IP is not assigned to a running instance
    - from the ec2 dashboard click elastic ip
    - click allocate elastic ip, finish the process
    - go to your ec2 instance, select it
    - go to actions -> networking -> associate an elastic IP, associate the allocated ip with your instance
    - whenever you kill your instance, (not stop, restart, etc.) make sure to deallocate the ip to avoid charges

### How to access the instance from SSH:
* using PUTTY
    - download puttygen, convert the keyname.pem to keyname.ppk for putty's use
    - launch putty, enter the IP address of the instance into the host field
    - navigate to connections/ssh/auth in the Category window
    - click browse, find your keyname.ppk file
    - SAVE YOUR CONFIGURATION
    - open the connection
* using command line ssh client, you can use the given keyname.pem file. type the following:
```
ssh -i /path/my-key-pair.pem my-instance-user-name@my-instance-public-dns-name
```

### Initialize the Ubuntu instance with docker, nodejs, and python, mount EFS:
- ssh into the instance
- checkout the repository
- take the init script and move it to the ~ directory
- run the init script



### Restarting the EC2 instance
- go into the ec2 dashboard and restart the ec2 instance to allow the docker daemon to start

    if any errors occur with docker: here are steps for troubleshooting:
    https://docs.docker.com/config/daemon/#:~:text=Start%20the%20daemon%20using%20operating%20system%20utilities&text=The%20command%20to%20start%20Docker,Docker%20to%20start%20on%20boot.

### Build the docker images and push to dockerhub
firstly create a repository on your dockerhub account, 
login on your development machine login to docker to allow you access to your repositories
```
docker login
```

pull the git repo

run these commands from the _server_ folder
```
docker build -f Dockerfile -t dockerhubusername/dockerhubrepositoryname:latest-server
docker push dockerhubusername/dockerhubrepositoryname:latest-server
```

run these commands from the _client-server_ folder
```
docker build -f Dockerfile-prod -t dockerhubusername/dockerhubrepositoryname:latest-client
docker push dockerhubusername/dockerhubrepositoryname:latest-client
```

### Pull and launch the docker containers in headless mode with the appropriate ports exposed
SSH back into the aws instance, run the following commands
```
docker pull dockerhubusername/dockerhubrepositoryname:latest-client
docker pull dockerhubusername/dockerhubrepositoryname:latest-server
docker network create scdine
docker run -d -p 8000:8000 --name django --network scdine dockerhubusername/dockerhubrepositoryname:latest-server
docker run -d -p 443:443 -p 80:80 --name client --network scdine dockerhubusername/dockerhubrepositoryname:latest-client
```

