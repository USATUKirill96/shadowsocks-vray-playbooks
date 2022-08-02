
[Here](docs/azure.md) there is an example of setting a  microsoft azure web server (eng thranslation is in progress)

# Script for automated deploy of Shadowsocks + v2ray on remote server. Also generates client configs for ios/android/pc

1. [About](#about)
2. [What's inside?](#tech-details)
3. [Before starting](#pre-setup)
4. [Local environment setup](#local-setup)
5. [Server configs](#server-setup)
6. [Deploy and tags](#deploy)
7. [Client setup](#client)
8. [Typical errors](#faq)


# About <a id="about"></a>
- [Shadowsocks](https://shadowsocks.org/en/index.html) - fast, secure, customizable proxy-server
- [v2ray](https://www.v2ray.com/en/#project-v-) - instrument for client-server communication

The script deploys Shadowsocks server and v2ray plugin. The connection is established through websocket(https), so you'll have to register a domain for your server  
  
Together these instruments form a secure and hard-to-track network for proxying and avoiding gouvernment restriction.

V2ray is known as a working way of passing the Great Chineese Firewall. Unlike VPN, your internet provider cannot track it that easy. It also minimizes speed vaste and mobile phone battery consumption.
**v2ray is not designed to secure the traffic**. It's main purpose is to avoid the gouvernment restrictions.

# What's inside? <a id="tech-details"></a>

- Server side:

  Long story short: docker is installed, ports opened, Nginx, Shadowsocks-rust and Certbot containers started. You can get more details from [Schema](docs/server-eng.png)

- Client side:

  Config.json for ss-local client and qr-code for mobile devices generated


# Before starting <a id="pre-setup"></a>

1. You need a vps server. Minimal possible configuration is enough, just check if the monthly bandwith limit is enough for you. Google, Amazon and Oracle provide free VM instances from month to life-long usage. You can check it [here](https://github.com/ripienaar/free-for-dev#major-cloud-providers)

2. You also need a domain name for the server. There are a lot of services with free domain names. [list](https://github.com/ripienaar/free-for-dev#dns), [the one I use](https://www.dnsexit.com/)

# Local environment setup <a id="local-setup"></a>

You need:
- Python 3.7
- Virtualenv
  
## Installing python 3.7 

### For windows:
  1. Download [Windows x86-64 executable installer](https://www.python.org/downloads/release/python-370/)
  2. Launch 
  3. Install

### Ubuntu linux
```bash
sudo apt update
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.7
```

### MacOS
```bash
brew install python@3.7
```

## virtualenv install
```bash
python3.7 -m pip install virtualenv
```

## Creating virtual environment and installing dependencies
In project directory type:
```bash
python3.7 -m virtualenv venv --python 3.7
source venv/bin/activate
pip install -r requirements.txt
```

Use `source venv/bin/activate' to activate virtual environment before deployment


# Server configuration <a id="server-setup"></a>

1. Duplicate file `variables.example.yml` and rename it into `variables.yml`. Modify it with your own values:

- user: username you use to login on the server
- host: domain you rented in the "Before starting" step
- email: email used for SSL keys generation
- proxy_password: proxy password, use something complicated
- method: encryption metod, you can let it be as in example
- local_port: local available port on your pc
- fast_open: true to make things faster. Works on linux kernel 3.1+
- endpoint: proxy endpoint, use whatever you want
- enable_firewall: yes to enable firewall on server after setup. If you have other projects on the server it may stop working

2. Duplicate `inventories/hosts.example.ini` and rename to `hosts.ini`. Modify it with your own values:

- server ansible_host= domain you registered in "Before starting" step

# Deploy and tags <a id="deploy"></a>

## Server deploy

Pre-setup requires docker and docker-compose to be installed on the server, ports 80 and 443 also must be open. You can do it automaticly, typing:

```bash
ansible-playbook -i inventories/hosts.ini --extra-vars "@variables.yml"  deploy/setup.yml  
```

Available tags: 

- disable-iptables - Flushes iptables config. Actual for the oracle cloud instances


After successful pre-setup deploy server and SSL-keys generator typing:

```bash
ansible-playbook -i inventories/hosts.ini --extra-vars "@variables.yml"  deploy/server.yml   
```

Available tags:

- nginx - deploy nginx config. Run it if you changed proxy server endpoint
- shadowsocks - Run it if you need to change proxy-server configs
- keys - SSL-keys generation service deploy. Run it if you changed domain

### tags:
type the command like

```bash
ansible-playbook -i inventories/hosts.ini --extra-vars "@variables.yml"  deploy/setup.yml --tags disable-iptables 
```
to list the tags

### Example

setup server
```bash
ansible-playbook -i inventories/hosts.ini --extra-vars "@variables.yml"  deploy/setup.yml  
```
flush iptables
```bash
ansible-playbook -i inventories/hosts.ini --extra-vars "@variables.yml"  deploy/setup.yml --tags disable-iptables 
```

deploy shadowsocks
```bash
ansible-playbook -i inventories/hosts.ini --extra-vars "@variables.yml"  deploy/server.yml   
```


## Client deploy

```bash
ansible-playbook -i inventories/hosts.ini --extra-vars "@variables.yml"  deploy/client.yml
```

Run it to generate the client config. In the `client-config` directory you'll be able to see the next files:
- shadowsocks-libev.config For ubuntu client
- config.json For windows and mac clients
- qrcode.png For android and ios cleints [Author](https://github.com/OriginCode/shadowsocks-libev-qrcode)

# Client setup<a id="client"></a>

## Ubuntu linux

```bash
sudo apt update
sudo apt install shadowsocks-libev
sudo apt install shadowsocks-v2ray-plugin
```

Copy client config to the ss-client root directory:
```bash
cp client-config/shadowsocks-libev.json /etc/shadowsocks-libev/config.json
```

Run server using command:
```bash
ss-local
```

## Android

Install [shadowsocks](https://play.google.com/store/apps/details?id=com.github.shadowsocks) and 
[v2ray](https://play.google.com/store/apps/details?id=com.github.shadowsocks.plugin.v2ray)

Press "add new" icon

![](docs/android.png)

and choose "scan qr code"

Use qr code from `client-config/qrcode.png`

## Windows
-Download the latest version of [shadowsocks](https://github.com/shadowsocks/shadowsocks-windows/releases) and unpack it. 
- Download the latest version of [v2ray](https://github.com/shadowsocks/v2ray-plugin/releases) and unpack it. Rename the file inside to v2ray.exe, save it to the shadowsocks directory
- Run Shadowsocks.exe, fill the fields the same as in client-config/shadowsocks-libev.json or just import it

## iOS
use Shadowrocket from appstore, scan qr code and enjoy

# Typical errors <a id="faq"></a>

## Oracle

Oracle has complicated iptables config which will not allow you to setup proxy that easy. Just add `disable-iptables` tag during server setup

## Provider-side firewalls

Check if the VPS provider has its own firewall and allow ports 80, 443 or disable it