import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize('file_name', [
  'ca.pem',
  'cert.pem',
  'key.pem'
])
def test_files(host, file_name):
    all_variables = host.ansible.get_variables()
    path = all_variables['docker_client_certs_path'] + '/' + file_name
    print(path)
    file = host.file(path)
    assert file.exists
