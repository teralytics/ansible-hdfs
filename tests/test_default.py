import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
   '.molecule/inventory').get_hosts('all')


def test_hosts_file(File):
    f = File('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_hdfs_site(File):
    f = File('/usr/local/hadoop/etc/hadoop/hdfs-site.xml')

    assert f.exists
    assert f.user == 'hdfs'
    assert f.group == 'hadoop'
    assert f.contains('<value>cluster1</value>')


def test_core_site(File):
    f = File('/usr/local/hadoop/etc/hadoop/core-site.xml')

    assert f.exists
    assert f.user == 'hdfs'
    assert f.group == 'hadoop'
    assert f.mode == 0o755


def test_hdfs_datanode_running(Service):
    service = Service('hdfs-datanode')

    assert service.is_running
    assert service.is_enabled


def test_zookeeper_running(Service):
    service = Service('zookeeper')

    assert service.is_running
    assert service.is_enabled


def test_hdfs_journal_running(Service):
    service = Service('hdfs-journalnode')

    assert service.is_running


def test_hdfs_datanode_web_listening(Socket):
    socket = Socket('tcp://0.0.0.0:50075')
    assert socket.is_listening
