# Ansible Code Challenge

[![Build Status](https://travis-ci.com/calillo/ansible-cc.svg?branch=master)](https://travis-ci.com/calillo/ansible-cc)
[![GitHub tag](https://img.shields.io/github/tag/calillo/ansible-cc.svg)](https://github.com/calillo/ansible-cc/tags)

Ansible playbook script:
1. Provisioning two CentOS VMs on GCP
2. Mount 40GB dedicate disk on VMs
3. Install and configure Docker Swarm
4. Secure Docker Swarm cluster with TLS

## Requirements
- ansible
- ansible-galaxy

## Dependencies
```bash
pip install -r ansible-requirements.txt
ansible-galaxy install -r roles/requirements.yml
```

## Configuration
`inventories/dev/group_vars/all.yml`
```yaml
# number of manager nodes
num_manager: 1
# number of worker nodes
num_worker: 1
# gcp region, zone and vm type
zone: us-central1-a
region: us-central1
machine_type: f1-micro
# dedicated docker disk partition size
size_gb: 40

# path to local pki folder where ansible creare CA, client and server keys/certificates
pki_path: ~/github/ansible-cc/pki
# path to local docker TLS client folder
docker_client_certs_path: ~/.docker
# path to remote docker TLS server folder
docker_server_certs_path: /etc/docker/ssl
```

### GCP
Remeber to create and set your GCP json service account file for your project inside both files:
- `inventories/dev/group_vars/all.yml`
```yaml
gcp_project: <gcp_projcect_name>
gcp_cred_kind: serviceaccount
gcp_cred_file: <path_to_json_service_account_file>
```
- `inventories/dev/gcp.yml`
```yaml
projects:
  - <gcp_projcect_name>
...
auth_kind: serviceaccount
service_account_file: <path_to_json_service_account_file>
```

## Run
### Create and configure infrastructure
```bash
ansible-playbook -i inventories/dev site.yml -t create
```
### Configure/Reconfigure infrastructure
```bash
ansible-playbook -i inventories/dev site.yml -t configure
```
### Delete infrastructure
```bash
ansible-playbook -i inventories/dev site.yml -t delete
```

## Docker Swarm
Connecto to Docker using TLS
```bash
export DOCKER_HOST=tcp://<ip-master-node>:2376
export DOCKER_TLS_VERIFY=1

docker info
```
> Optional: if you don't use default `~./docker` folder
> ```bash
> export DOCKER_CERT_PATH=<your_certs_path_folder>
> ```

### Deploy sample application
```bash
docker stack deploy --compose-file deploy/docker-compose.yml app1
docker service ls
docker stack ps app1
```

## Testing
Developed roles tests are performed by Molecule using the Docker driver.
```bash
cd roles/secure-docker-ca-client
molecule test --all
```

```bash
cd roles/secure-docker-server
molecule test --all
```

## TODO
- provisiong with terraform
- set ansible ssh pub key on provisioning
- testing ci with tox

## Note

### Ansible
Create ansible key
```bash
ssh-keygen -t rsa -b 4096 -C "ansible" -f ~/.ssh/ansible
```
#### Inventory
```bash
ansible-inventory -i inventories/dev --graph
ansible-inventory -i inventories/dev --list --yaml
ansible -i inventories/dev all -m ping
```

### Molecule
```bash
pytest -v molecule/default/tests/test_default.py --hosts='ansible://localhost'
```