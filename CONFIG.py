#!/usr/bin/env python
# encoding: utf-8
# Time    : 2/11/2019 4:08 PM
# Author  : Luzaofa

file_path = '/root/InstallScript/'

IPADDR = "192.168.XX.XX"

GATEWAY = "192.168.XX.1"
NETMASK = "255.255.255.0"

network_path = '/etc/sysconfig/network-scripts/'
yum_install_path = '/etc/yum.repos.d/'
yum_file_path = '/ConfigurationFile/yum/'
kernel_file_path = '/ConfigurationFile/kernel/'
key_install_path = '/etc/pki/rpm-gpg/'
sfu_file_path = '/ConfigurationFile/sfu/'
dns_path = '/etc/resolv.conf'

yum_packages_list = [
    'vim', 'python-pip', 'gcc', 'source-highlight', 'htop', 'stress', 'psmisc', 'rsync', 'at',
    'ntpdate', 'telnet', 'net-tools', 'ethtool', 'traceroute', 'perf', 'pciutils', 'tcpdump',
    'libpcap', 'libpcap-devel', 'python-devel', 'boost-python', 'boost-system',
]

pip_packages_list = ['--upgrade pip', 'ipython==5.5.0', 'numpy', 'psutil', 'gevent', 'greenlet', 'email']

network_list = [
    'TYPE="Ethernet"', 'PROXY_METHOD="none"', 'BROWSER_ONLY="no"', 'BOOTPROTO="static"',
    'DEFROUTE="yes"', 'IPV4_FAILURE_FATAL="no"', 'NAME="{net_name}"', 'DEVICE="{net_name}"', 'ONBOOT="yes"',
    'IPADDR="{0}"'.format(IPADDR), 'GATEWAY="{0}"'.format(GATEWAY), 'NETMASK="{0}"'.format(NETMASK)
]

dns_list = ['nameserver 210.22.70.3', 'nameserver 114.114.114.114']
