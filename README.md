ansible-cc

## install

sudo pip install ansible requests google-auth

ssh-keygen -t rsa -b 4096 -C "ansible" -f ~/.ssh/ansible

## ansible

ansible-playbook -t create playbooks/create_vms.yml
ansible-playbook -i inventories/inventory_gcp.yml playbooks/install_docker_swarm.yml
ansible-playbook -t ca-client playbooks/secure_docker_swarm_local.yml
ansible-playbook -i inventories/inventory_gcp.yml -t server playbooks/secure_docker_swarm_remote.yml
ansible-playbook -i inventories/inventory_gcp.yml -t install playbooks/secure_docker_swarm_remote.yml

ansible-playbook -t delete playbooks/create_vms.yml

## inventory

ansible-inventory --graph -i inventories/vm_gcp.yml

ansible-inventory --list -i inventories/vm_gcp.yml --yaml

ansible -i inventory all -m ping

# galaxy

ansible-galaxy install -r roles/requirements.yml

# secure

openssl genrsa -out ca-key.pem 4096
openssl req -x509 -new -nodes -key ca-key.pem -days 10000 -out ca.pem -subj '/CN=Docker CA'

openssl genrsa -out client-key.pem 2048
openssl req -new -key client-key.pem -out client-cert.csr -subj '/CN=docker-client' -config client.cnf
openssl x509 -req -in client-cert.csr -CA ca.pem -CAkey ca-key.pem -CAcreateserial -out client-cert.pem -days 365 -extensions v3_req -extfile client.cnf

openssl genrsa -out manager1-key.pem 2048
openssl req -new -key manager1-key.pem -out manager1-cert.csr -subj '/CN=docker-server' -config manager1.cnf
openssl x509 -req -in manager1-cert.csr -CA ca.pem -CAkey ca-key.pem -CAcreateserial -out manager1-cert.pem -days 365 -extensions v3_req -extfile manager1.cnf

openssl genrsa -out worker1-key.pem 2048
openssl req -new -key worker1-key.pem -out worker1-cert.csr -subj '/CN=docker-server' -config worker1.cnf
openssl x509 -req -in worker1-cert.csr -CA ca.pem -CAkey ca-key.pem -CAcreateserial -out worker1-cert.pem -days 365 -extensions v3_req -extfile worker1.cnf

{
    "hosts": ["unix:///var/run/docker.sock", "tcp://0.0.0.0:2376"],
    "tlscacert": "/etc/docker/ssl/ca.pem",
    "tlscert": "/etc/docker/ssl/cert.pem",
    "tlskey": "/etc/docker/ssl/key.pem",
    "tlsverify": true
}

export DOCKER_HOST=tcp://34.70.109.143:2376
export DOCKER_TLS_VERIFY=1
export DOCKER_CERT_PATH=~/github/ansible-cc/pki/client

## TODO
- loop vm creation
- copy ansible ssh pub key
