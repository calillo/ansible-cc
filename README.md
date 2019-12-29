ansible-cc

## install

sudo pip install ansible requests google-auth

ssh-keygen -t rsa -b 4096 -C "ansible" -f ~/.ssh/ansible

## ansible

ansible-playbook -t create playbooks/create_vms.yml

ansible-playbook -i inventories/inventory_gcp.yml playbooks/install_docker_swarm.yml

ansible-playbook -t delete playbooks/create_vms.yml

## inventory

ansible-inventory --graph -i inventories/vm_gcp.yml

ansible-inventory --list -i inventories/vm_gcp.yml --yaml

ansible -i inventory all -m ping

# galaxy

ansible-galaxy install -r roles/requirements.yml

## TODO
- loop vm creation
- copy ansible ssh pub key
