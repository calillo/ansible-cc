ansible-cc

## install

sudo pip install ansible requests google-auth

ssh-keygen -t rsa -b 4096 -C "ansible" -f ~/.ssh/ansible

## ansible

ansible-playbook -i inventories/dev playbooks/create_infra.yml -t create
ansible-playbook -i inventories/dev playbooks/install_docker_swarm.yml -t create
ansible-playbook -i inventories/dev playbooks/secure_docker_swarm.yml -t create

ansible-playbook -i inventories/dev site.yml -t create
ansible-playbook -i inventories/dev site.yml -t configure
ansible-playbook -i inventories/dev site.yml -t delete

## inventory

ansible-inventory -i inventories/dev --graph
ansible-inventory -i inventories/dev --list --yaml
ansible -i inventories/dev all -m ping

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

## Docker Swarm

docker stack deploy --compose-file docker-compose.yml app1
docker service ls
docker stack ps app1

## Molecule

pytest -v molecule/default/tests/test_default.py --hosts='ansible://localhost'

    # image: fiercely/centos7:systemd
    # privileged: true
    # pre_build_image: true
    # volume_mounts:
    #   - "/sys/fs/cgroup:/sys/fs/cgroup:rw"
    # command: "/usr/sbin/init"

## TODO
- provisiong with terraform
- set ansible ssh pub key on provisioning
