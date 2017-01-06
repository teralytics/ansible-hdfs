import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
   '.molecule/inventory').get_hosts('namenodes')


def test_hdfs_namenode_running(Service):
    service = Service('hdfs-namenode')

    assert service.is_running
    assert service.is_enabled


def test_hdfs_zkfc_running(Service):
    service = Service('hdfs-zkfc')

    assert service.is_running
    assert service.is_enabled


def test_hdfs_listening(Socket):
    socket = Socket('tcp://0.0.0.0:8020')
    assert socket.is_listening


def test_hdfs_web_listening(Socket):
    socket = Socket('tcp://0.0.0.0:50070')
    assert socket.is_listening
