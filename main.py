import nmap
import threading
import time
import os
# os.environ["http_proxy"] = "http://127.0.0.1:30809"
# os.environ["https_proxy"] = "http://127.0.0.1:30809"

nm = nmap.PortScanner()


class Smdk(threading.Thread):

    def __init__(self, ip, qsdk, jsdk):
        threading.Thread.__init__(self)
        # 检查是否有错误，assert函数
        # assert isinstance(port_max, int) and isinstance(qsdk, int)
        self.ip = ip
        self.qsdk = qsdk
        self.jsdk = jsdk

    def run(self):
        jg = nm.scan(self.ip, self.qsdk+'-'+self.jsdk, '-sS')
        # print(nm.scaninfo()['tcp'])
        self.clsj(jg)

    def clsj(self, item):
        for x in item['scan'][self.ip]['tcp'].items():
            xx = 'ip：%s  端口：%-5s  状态：%-15s  服务：%s' % (
                self.ip, x[0], x[1]['state'], x[1]['name'])
            print(xx)
            # 写入文件
            # if xx:
            #     try:
            #         with open(f'{self.ip}.txt', 'a', encoding='utf-8') as f:
            #             f.write((xx) + '\n')
            #     except:
            #         time.sleep(0.1)
            if x[1]['state'] == 'open':
                opendict.append(xx)
            else:
                blockdict.append(xx)
            jg.append(xx)
        # print(f'ip：{ip}扫描完成！')
        print('--------------------------------------------------------------')


def mwzx():
    if ((int(jsdk) - int(qsdk)) % num) == 0:
        xrsj()
        # pass
    else:
        # print('末尾执行!')
        f = Smdk(ip, str(int(jsdk) - ((int(jsdk) - int(qsdk)) % num)+1),
                 str(jsdk))
        f.start()
        f.join()
        xrsj()


def xrsj():
    opendict1 = sorted(opendict, key=lambda x: int(x.split('端口：')[
        1].split('状态：')[0].replace(' ', '')))
    blockdict1 = sorted(blockdict, key=lambda x: int(x.split('端口：')[
        1].split('状态：')[0].replace(' ', '')))
    jg1 = sorted(jg, key=lambda x: int(x.split('端口：')[
        1].split('状态：')[0].replace(' ', '')))
    with open(f'{ip}-open.txt', 'a', encoding='utf-8') as f:
        # 写入单行
        # f.writeline(opendict)
        f.write('\n'.join(opendict1))
    with open(f'{ip}.txt', 'a', encoding='utf-8') as f:
        f.write('\n'.join(jg1))
    print(f'ip：{ip}扫描完成！')


if __name__ == '__main__':
    os.chdir(os.getcwd())
    jg = []
    opendict = []
    blockdict = []
    jclb = []
    # 加锁，放在run里面
    # threadLock = threading.Lock()
    # threadLock.acquire()
    # threadLock.release()
    ip = input('请输入ip：')
    qsdk = input('请输入开始端口：\n')
    jsdk = input('请输入结束端口：\n')
    num = 10
    interval = (int(jsdk) - int(qsdk)) // num
    if qsdk == jsdk:
        f = Smdk(ip, str(qsdk),
                 str(jsdk))
        f.start()
    elif 0 < int(jsdk) - int(qsdk) < 10:
        f = Smdk(ip, str(qsdk),
                 str(jsdk))
        f.start()
    else:
        # ddsj = input('输入最后一个线程运行的等待时间(默认10)：')
        # if ddsj:
        #     pass
        # else:
        #     ddsj = 10
        with open(f'{ip}-open.txt', 'a', encoding='utf-8') as f:
            f.truncate(0)
        with open(f'{ip}.txt', 'a', encoding='utf-8') as f:
            f.truncate(0)
        for i in range(interval):
            if i == 0 and interval == 1:
                f = Smdk(ip, str((i * num)+int(qsdk)),
                         str(((i+1) * num)+int(qsdk)))
                f.start()
                f.join()
                mwzx()
            elif i == 0:
                f0 = Smdk(ip, str((i * num)+int(qsdk)),
                          str(((i+1) * num)+int(qsdk)))
                f0.start()
                jclb.append(f0)
            elif i == interval-1 and i != 0:
                # time.sleep(int(ddsj))
                for jc in jclb:
                    jc.join()
                f = Smdk(ip, str((i * num)+int(qsdk)+1),
                         str(((i+1) * num)+int(qsdk)))
                f.start()
                f.join()
                mwzx()
            else:
                jcmc = 'f'+str(i)
                jcmc = Smdk(ip, str((i * num)+int(qsdk)+1),
                            str(((i+1) * num)+int(qsdk)))
                jcmc.setDaemon(True)
                jcmc.start()
                jclb.append(jcmc)
