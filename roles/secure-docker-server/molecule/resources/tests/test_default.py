import pytest
import os
import json
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_service(host):
    service = host.service('docker')

    assert service.is_running
    assert service.is_enabled


@pytest.mark.parametrize('file_name, mode', [
  ('ca.pem', 0o0600),
  ('cert.pem', 0o0600),
  ('key.pem', 0o0400)
])
def test_ssl_files(host, file_name, mode):
    all_variables = host.ansible.get_variables()
    path = all_variables['docker_server_certs_path'] + '/' + file_name
    ssl_file = host.file(path)
    assert ssl_file.exists
    assert ssl_file.mode == mode


def test_ssl_folder(host):
    all_variables = host.ansible.get_variables()
    path = all_variables['docker_server_certs_path']

    cert_dir = host.file(path)
    assert cert_dir.is_directory
    assert cert_dir.mode == 0o0700


def test_openssl_verify(host):
    all_variables = host.ansible.get_variables()
    path = all_variables['docker_server_certs_path']

    cmd_s = ('openssl verify -ignore_critical -CAfile %s %s')
    cmd = host.run(cmd_s,
                   path + '/ca.pem',
                   path + '/cert.pem')
    assert cmd.rc == 0


def test_daemon_json(host):
    all_variables = host.ansible.get_variables()
    path = all_variables['docker_server_certs_path']

    daemon_json = host.file('/etc/docker/daemon.json')
    assert daemon_json.is_file
    assert daemon_json.mode == 0o0600

    daemon = json.loads(daemon_json.content_string)

    assert 'tcp://0.0.0.0:2376' in daemon['hosts']
    assert daemon['tls']
    assert path + '/cert.pem' == daemon['tlscert']
    assert path + '/key.pem' == daemon['tlskey']
    assert path + '/ca.pem' == daemon['tlscacert']
    assert daemon['tlsverify']


def test_systemd_override(host):
    override_path = '/etc/systemd/system/docker.service.d'
    override_dir = host.file(override_path)

    assert override_dir.is_directory
    assert override_dir.mode == 0o0755

    override_file_path = os.path.join(override_path, 'override.conf')
    override_path = host.file(override_file_path)

    assert override_path.is_file
    assert override_path.mode == 0o0644


def test_docker_tls_verify(host):
    all_variables = host.ansible.get_variables()
    path = all_variables['docker_server_certs_path']
    hostname = all_variables['inventory_hostname']

    cmd_s = ('docker --tlsverify --tlscacert=%s --tlscert=%s '
             '--tlskey=%s -H=%s:2376 version')
    cmd = host.run(cmd_s,
                   path + '/ca.pem',
                   path + '/cert.pem',
                   path + '/key.pem',
                   hostname)
    assert cmd.rc == 0
