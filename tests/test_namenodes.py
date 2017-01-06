import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
   '.molecule/inventory').get_hosts('namenodes')


def test_hdfs_printTopology_command(Sudo, Command):
    with Sudo("hdfs"):
        c = Command("/usr/local/hadoop/bin/hdfs dfsadmin -printTopology")

        assert len(c.stdout.rstrip().split('\n')) == 4
        assert c.rc == 0


def test_hdfs_check_safemode_is_off(Sudo, Command):
    with Sudo("hdfs"):
        c = Command("/usr/local/hadoop/bin/hdfs dfsadmin -safemode get")

        assert len(c.stdout.rstrip().split('\n')) == 2
        for row in c.stdout.rstrip().split('\n'):
            assert row.find("OFF") != -1
        assert c.rc == 0


def test_hdfs_is_empty(Sudo, Command):
    with Sudo("hdfs"):
        c = Command("/usr/local/hadoop/bin/hdfs dfs -ls /")

        assert c.stdout.rstrip() == ''
        assert c.rc == 0


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
