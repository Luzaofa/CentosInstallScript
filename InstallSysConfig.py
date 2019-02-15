#!/usr/bin/env python
# encoding: utf-8
# Time    : 2/11/2019 2:32 PM
# Author  : Luzaofa

import os
import time
import logging
import CONFIG
from SendEmail import Main


class SysConfig(object):

    def __init__(self):
        '''初始化配置'''
        self.file_path = CONFIG.file_path
        self.network_path = CONFIG.network_path
        self.yum_install_path = CONFIG.yum_install_path
        self.network_list = CONFIG.network_list
        self.yum_file_path = CONFIG.yum_file_path
        self.kernel_file_path = CONFIG.kernel_file_path
        self.key_install_path = CONFIG.key_install_path
        self.sfu_file_path = CONFIG.sfu_file_path
        self.dns_path = CONFIG.dns_path
        self.dns_list = CONFIG.dns_list
        self.yum_packages_list = CONFIG.yum_packages_list
        self.pip_packages_list = CONFIG.pip_packages_list

    def log(self, fileName, mass):
        '''日志'''
        os.chdir(self.file_path)
        logging.basicConfig(filename=fileName, format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
        logging.info(mass)

    # with open(fileName, 'a+') as f:
    #    Mass = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ' - INFO - ' + mass + '\n'
    #    f.write(Mass)

    def get_path_files(self, path):
        '''返回某文件夹下的文件'''
        os.chdir(path)
        files = os.popen('ls').readlines()
        answer = []
        for file in files:
            answer.append(file.strip())
        return answer

    def write_mass_to_file(self, path, seq):
        '''将信息写入文件中'''
        with open(path, 'r+') as f:
            f.seek(0)
            f.truncate()
            mass = [i + '\n' for i in seq]
            f.writelines(mass)

    def yum_install(self):
        '''yum云源更改'''
        print '正在安装yum源....'
        self.log('installLog.txt', '正在安装yum源。。。。')
        os.chdir(self.file_path)
        yum_install_path = self.yum_install_path
        yum_file_path = os.getcwd() + self.yum_file_path
        key_install_path = self.key_install_path

        os.chdir(yum_install_path)
        if not os.path.exists(yum_install_path + 'bak'):
            os.mkdir('bak')
        os.system('mv *.repo bak')
        os.chdir(yum_file_path)
        yum_cp = 'cp *.repo {0}'.format(yum_install_path)
        os.system(yum_cp)
        files = self.get_path_files(yum_install_path)
        if files != ['bak', 'CentOS-Base-ustc.repo', 'epel-testing-ustc.repo', 'epel-ustc.repo']:
            print 'yum复制失败！'
            self.log('installLog.txt', 'yum复制失败！{0}'.format(files))
            return 0
        os.system('yum makecache fast')  # 更改原来yum源
        self.log('installLog.txt', 'yum安装成功！{0}'.format(files))

        os.chdir(yum_file_path.replace('yum', 'key'))
        key_cp = 'cp RPM-GPG-KEY-EPEL-7.ustc {0}'.format(key_install_path)
        os.system(key_cp)
        self.log('installLog.txt', 'key复制成功！{0}'.format(key_cp))
        key_install = 'mv RPM-GPG-KEY-EPEL-7.ustc RPM-GPG-KEY-EPEL-7'
        os.chdir(key_install_path)
        os.system(key_install)
        self.log('installLog.txt', 'key安装成功！{0}'.format(key_install))

    def count_kernel(self):
        '''返回当前kernel信息'''
        answer = os.popen('yum list installed | grep kernel').readlines()
        answers = []
        for file in answer:
            answers.append([i for i in file.strip().split(' ') if i != ''])
        return answers

    def pip_conf(self):
        '''pip映射'''

        '''
        [global]
        index-url = http://pypi.douban.com/simple #豆瓣源，可以换成其他的源
        trusted-host = pypi.douban.com            #添加豆瓣源为可信主机，要不然可能报错
        disable-pip-version-check = true          #取消pip版本检查，排除每次都报最新的pip
        timeout = 120
        '''
        os.chdir('/root/')
        try:
            os.system('mkdir .pip')
        except:
            pass
        os.chdir('/root/.pip/')
        os.system('ln -s ../pip.conf ./')

    def kernel_install(self):
        '''kernel安装'''
        print '正在安装kernel....'
        self.log('installLog.txt', '正在安装kernel。。。。')
        os.chdir(self.file_path)
        kernel_file_path = os.getcwd() + self.kernel_file_path
        answers = self.count_kernel()
        for k in answers:
            if k[0] == 'kernel-headers.x86_64' or k[0] == 'kernel-devel.x86_64':
                os.system('yum -y remove {0}'.format(k[0]))

        kernel_rpm = ['kernel-devel-3.10.0-693.el7.x86_64.rpm', 'kernel-headers-3.10.0-693.el7.x86_64.rpm']
        for k in kernel_rpm:
            os.chdir(kernel_file_path)
            install_mass = 'yum -y install {0}'.format(k)
            os.system(install_mass)
            self.log('installLog.txt', '正在安装：{0}'.format(install_mass))

        new_kernel = self.count_kernel()
        if len(new_kernel) != 5:
            return 0
        print 'kernel安装成功！'
        for info in new_kernel:
            self.log('installLog.txt', 'kernel安装成功！{0}'.format(info))

    def check_yum_install(self, package):
        '''检测yum安装是否完成'''
        mass = 'yum -y install {0}'.format(package)
        files = os.popen(mass).readlines()
        if 'already' in str(files) or 'Finished' in str(files) or 'Complete' in str(files):
            ans = '{p}安装成功！'.format(p=package)
        elif 'sfutils' in package:  # 二次安装会报错，但实际已经安装成功
            ans = '{p}安装成功！'.format(p=package)
        else:
            ans = '{p}安装失败！'.format(p=package)
        self.log('installLog.txt', ans)
        print ans

    def yum_packages_install(self):
        '''yum包安装'''
        os.chdir(self.file_path)
        self.log('installLog.txt', '正在进行yum包安装。。。。')
        packages = self.yum_packages_list
        for p in packages:
            mass = 'yum -y install {0}'.format(p)
            os.system(mass)
            self.check_yum_install(p)
        # sfutils安装
        os.chdir(os.getcwd() + self.sfu_file_path)
        install_mass = 'yum -y install {0}'.format('sfutils-6.0.3.1001-1.x86_64.rpm')
        os.system(install_mass)
        self.check_yum_install('sfutils-6.0.3.1001-1.x86_64.rpm')

    def pip_packages_install(self):
        '''pip包安装'''
        packages = self.pip_packages_list
        self.log('installLog.txt', '正在进行pip包安装。。。。')
        for p in packages:
            mass = 'pip install {0}'.format(p)
            os.system(mass)
            files = os.popen(mass).readlines()
            if 'already' in str(files) or 'Finished' in str(files):
                ans = '{p}安装成功！'.format(p=p)
            else:
                ans = '{p}安装失败！'.format(p=p)
            print ans
            self.log('installLog.txt', ans)

    def network_scripts(self):
        '''配置IP地址、网关、子网掩码'''
        print '正在配置网络...'
        self.log('installLog.txt', '正在配置网络。。。。')
        os.chdir(self.network_path)
        files = os.popen('ls').readlines()
        get_network_names = os.popen('ip a').readlines()
        for up_name in get_network_names:
            if 'state UP qlen 1000' in up_name.strip():
                network_name = up_name.split(':')[1].strip()
                break
        new_network_list = []
        for net_name_ in self.network_list:
            mass = net_name_
            if '{net_name}' in net_name_:
                mass = net_name_.format(net_name=network_name)
            new_network_list.append(mass)

        for i in files:
            if 'ifcfg-{0}'.format(network_name) in i.strip():
                filepath = os.getcwd() + '/' + i.strip()
                self.write_mass_to_file(filepath, new_network_list)
                for info in new_network_list:
                    self.log('installLog.txt', info)
                break
        os.system('ifup {0}'.format(network_name))  # 网卡重启

    def dns_config(self):
        '''DNS配置'''
        filepath = self.dns_path
        self.write_mass_to_file(filepath, self.dns_list)
        for info in self.dns_list:
            self.log('installLog.txt', info)
        self.log('installLog.txt', '网络配置成功！')
        print '网络配置成功！'

    def logic(self):
        '''
        业务逻辑
        :param mass:
        :return:
        '''
        self.network_scripts()  # IP、网关、子网掩码
        self.dns_config()  # DNS配置
        self.kernel_install()  # kernel安装
        self.yum_install()  # yum安装
        self.pip_conf()  # pip源更改
        self.yum_packages_install()  # yum第三方包安装
        self.pip_packages_install()  # pip第三方包安装

    def main(self):
        '''
        主入口
        :return:
        '''
        start = time.time()
        try:
            os.remove('installLog.txt')
        except:
            pass
        self.logic()
        end = time.time()
        os.system('cp installLog.txt ../')
        os.system('mv installLog.txt SendEmail/Enclosure/')
        os.chdir(self.file_path)
        print('业务处理总耗时：%s 秒！' % (end - start))


if __name__ == '__main__':
    print 'Start！'
    demo = SysConfig()
    demo.main()

    Email = Main.Email()
    Email.sand_mail()
    time.sleep(5)
    Email = Main.Email()
    Email.sand_mail()
    os.system('rm -r ../InstallScript')
    print 'END'
