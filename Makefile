setup_server:
	ansible-playbook -i inventories/hosts.ini --extra-vars "@variables.yml"  deploy/setup.yml 

flush_iptables:
	ansible-playbook -i inventories/hosts.ini --extra-vars "@variables.yml"  deploy/setup.yml --tags disable-iptables 

deploy_server:
	ansible-playbook -i inventories/hosts.ini --extra-vars "@variables.yml"  deploy/server.yml   

prepare_ssh:
	ansible-playbook -i inventories/hosts.ini --extra-vars "@variables.yml"  deploy/client.yml --tags prepare_ssh   

deploy_client:
	ansible-playbook -i inventories/hosts.ini --extra-vars "@variables.yml"  deploy/client.yml   
