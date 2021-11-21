setup_server:
	ansible-playbook -i inventories/hosts.ini --extra-vars "@variables.yml"  deploy/setup.yml 
deploy_server:
	ansible-playbook -i inventories/hosts.ini --extra-vars "@variables.yml"  deploy/server.yml   
deploy_client:
	ansible-playbook -i inventories/hosts.ini --extra-vars "@variables.yml"  deploy/client.yml   
