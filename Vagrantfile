BOX_IMAGE = "ubuntu/xenial64"
WORKER_COUNT = 0

MANAGER_IP_ADDRESS = "192.168.100.10"

Vagrant.configure("2") do |config|
 config.vm.box = BOX_IMAGE

  config.vm.define "dockermaster" do |subconfig|
    subconfig.vm.box = BOX_IMAGE
    subconfig.vm.hostname = "dockermaster"
    subconfig.vm.network :private_network, ip: MANAGER_IP_ADDRESS
    subconfig.vm.provider "virtualbox" do |m|
	m.memory = 2048
	m.cpus = 2
    end
  end

    config.vm.define "dockernode1" do |subconfig|
      subconfig.vm.box = BOX_IMAGE
      subconfig.vm.hostname = "dockernode1"
      subconfig.vm.network :private_network, ip: "192.168.100.20"
    end

    config.vm.define "dockernode2" do |subconfig|
      subconfig.vm.box = BOX_IMAGE
      subconfig.vm.hostname = "dockernode2"
      subconfig.vm.network :private_network, ip: "192.168.100.30"
    end

    config.vm.provider "virtualbox" do |vb|
      vb.memory = 1024
    end

  config.vm.provision "shell", inline: <<-SHELL
     echo "provisioning"
     apt-get install \
             apt-transport-https \
       ca-certificates \
       curl \
       software-properties-common

    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

    apt-key fingerprint 0EBFCD88
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

    apt-get update
    apt-get install -y docker-ce
    usermod -aG docker vagrant

  SHELL
end
