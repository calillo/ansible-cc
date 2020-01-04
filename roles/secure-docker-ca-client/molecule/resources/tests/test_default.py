import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize('file_name, mode', [
  ('ca.pem', 0o0600),
  ('cert.pem', 0o0600),
  ('key.pem', 0o0400)
])
def test_ssl_files(host, file_name, mode):
    all_variables = host.ansible.get_variables()
    path = all_variables['docker_client_certs_path'] + '/' + file_name
    ssl_file = host.file(path)
    assert ssl_file.exists
    assert ssl_file.mode == mode


def test_openssl_verify(host):
    all_variables = host.ansible.get_variables()
    path = all_variables['docker_client_certs_path']

    cmd_s = ('openssl verify -ignore_critical -CAfile %s %s')
    cmd = host.run(cmd_s,
                   path + '/ca.pem',
                   path + '/cert.pem')
    assert cmd.rc == 0
