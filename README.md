## HDFS

### Introduction
This role installs HDFS on Ubuntu/Debian Linux servers.

### Role dependencies
* The role requires java and zookeeper to be installed, configured and running.

### Example 

```yml
- hosts: hadoop_hosts
  become: True
  roles:
  - hdfs
```

For an example inventory please check the [inventory](https://github.com/teralytics/ansible-hdfs/blob/master/inventory) file.

If ```hdfs_ssh_fence``` is set to ```true``` the playbook has to be run with the ```-K``` option of ansible-playbook!


### Configuration
This role supports two different modes of installation:

* Single Namenode with Secondary Namenode
* Two Namenodes in HA mode

The number of *namenodes* specifies the mode. If two namenodes are specified HDFS will be installed in an HA fashion.


For documentation details of HDFS please refer to the official [Hadoop documentation](http://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/HdfsUserGuide.html).

#### Preparation of your Inventory
This role makes use of groups to figure out which server needs which installation. The groups are listed below:

* namenodes
* datanodes
* secondarynamenode (Single NN setup only)
* zookeeper_hosts (High availability mode only)
* journalnodes (High availability mode only)

Alternatively variables like ```hdfs_namenodes``` can be overwritten (see [defaults/main.yml](https://github.com/teralytics/ansible-hdfs/blob/master/defaults/main.yml)).

#### Important variables:
The following gives a list of important variables that have to be set for a specific deployment. Most variables can be set in *group_vars* or *host_vars*.

* ```hdfs_cluster_name```: Name of your cluster
* ```hdfs_parent_dir```: Where to install HDFS to
* ```hdfs_version```: Hadoop version to use
* ```hdfs_tmpdir```: Where to write HDFS tmp files
* ```hdfs_namenode_dir_list```: Files of namenodes
* ```hdfs_datanode_dir_list```: Files of datanodes
* ```hdfs_namenode_checkpoint_dir_list```: Files of secondary namenode
* ```hdfs_distribution_method```: Should tar.gz be 'downloaded', 'local_file' or 'compile' install?
* ```hdfs_bootstrap```: Should the cluster be formatted? (If you have an already existing installation this option is not recommended)

For more configuration variables see the documentation in [defaults/main.yml](https://github.com/teralytics/ansible-hdfs/blob/master/defaults/main.yml).

#### Additional HDFS configuration
Additional configuration to ```hdfs-site.xml``` and ```core-site.xml``` can be added by overwriting the following variables:

- ```hdfs_site_additional_properties```
- ```core_site_additional_properties```

#### Description of playbooks
This section gives a brief description on what each playbook does. 

##### Native (experimental)
CURRENTLY ONLY WORKS WITH Ubuntu 14.04. (16.04. has a newer protobuf version and compilation fails)

This playbook will compile hadoop on server *hdfs_compile_node* to enable [hadoop native libraries](http://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/NativeLibraries.html) (Compression codecs and [HDFS Short-Circuit Local Reads](http://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/ShortCircuitLocalReads.html)).
This playbook will install the development tools necessary to be able to compile hadoop. (Download and compilation may take a while depending on you internet connection and server power (10-20 min))

To activate this playbook enable set ```hdfs_distribution_method``` to ```compile```.

Known issues: 

* Sometimes the git download fails for the first time. Just run it again.

Options:

* ```hdfs_compile_node```: Server to compile on
* ```hdfs_compile_from_git```: True if it should download the latest version from github.com
* ```hdfs_compile_version```: Version to download from github (tags usable by e.g. 'tags/rel/release-2.7.2' or 'HEAD')
* ```hdfs_fetch_folder```: Local folder to download the compiled tar to.

##### base
This playbook installs the hadoop binaries and creates links for easy usage.

##### config
This playbook writes the configuration files.

##### user
This playbook will create a user ```hdfs_user```, generate an ssh-key for it, distribute the key and register all servers in known_hosts file of each other. 

##### ssh_fence
This playbook sets up SSH access for the ```hdfs_user``` between the namenode servers. Used if an SSH fence is the preferred method as fencing method. (See [HA Documentation](https://hadoop.apache.org/docs/r2.7.2/hadoop-project-dist/hadoop-hdfs/HDFSHighAvailabilityWithQJM.html))

##### namenode
This playbook writes configuration files needed only by the namenode, creates folder and sets up services for namenode and zkfc.

##### datanode
This playbook creates the folders specified in ```hdfs_datanode_dir_list``` and registers the hdfs-datanode service.

##### journalnode
This playbook will install the journal node service.

##### secondarynamenode
This playbook will install and register hdfs-secondarynamenode service.

##### bootstrap_ha
This playbook bootstraps a cluster in HA mode

##### bootstrap_spof
This playbook bootstraps a cluster in SPOF mode. (One namenode and one secondary namenode)

### Testing
The tests are run using [molecule](https://github.com/metacloud/molecule) and a docker container.

##### Requirements:
- Docker
- molecule (pip module)
- docker-py (pip module)

#### Running tests

From the root folder run ```molecule test```.

### License
Apache 2.0

### Author information

- Bertrand Bossy
- Florian Froese
- Laurent Hoss 
