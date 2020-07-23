#create mount point for EFS
sudo mkdir efs

#upgrade apt/apt-get, add deadsnakes for python install
sudo apt install
sudo apt upgrade
sudo apt install software-properties-common
sudo add-apt-repository --yes ppa:deadsnakes/ppa
sudo apt-get install --upgrade


#install python and set correct python version
sudo apt install python3.8
sudo update-alternatives  --set python /usr/bin/python3.8

#install nvm and node.js 12.16.2
sudo apt install curl
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.11/install.sh | bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion" 
sudo nvm install 12.16.2

#install docker engine
sudo apt-get update

sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
	
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

sudo apt-get install docker-ce docker-ce-cli containerd.io

#manage docker perms
sudo groupadd docker
sudo usermod -aG docker $USER

#install docker-compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.26.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
