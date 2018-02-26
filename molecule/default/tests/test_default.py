import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/inventory').get_hosts('all')


def get(e, nodeName):
    arg = r"./property[name='{nodename}']".format(nodename=nodeName)
    return e.find(arg)[1].text


def test_hosts_file(File):
    f = File('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_hdfs_site(File):
    f = File('/usr/local/hadoop/etc/hadoop/hdfs-site.xml')

    import xml.etree.ElementTree
    e = xml.etree.ElementTree.fromstring(f.content_string)
    assert e.tag == 'configuration'
    assert get(e, 'dfs.nameservices') == 'cluster1'
    assert get(e, 'dfs.nameservice.id') == 'cluster1'
    assert set(get(e, 'dfs.ha.namenodes.cluster1').split(
        ',')) == set('hdfs1,hdfs2'.split(','))

    assert f.exists
    assert f.user == 'hdfs'
    assert f.group == 'hadoop'
    assert f.mode == 0o755


def test_core_site(File):
    f = File('/usr/local/hadoop/etc/hadoop/core-site.xml')

    import xml.etree.ElementTree
    e = xml.etree.ElementTree.fromstring(f.content_string)
    assert e.tag == 'configuration'
    assert get(e, 'fs.defaultFS') == 'hdfs://cluster1'
    assert set(get(e, 'ha.zookeeper.quorum').split(',')) == set(
        'hdfs1:2181,hdfs2:2181,hdfs3:2181'.split(','))

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
