
from binascii import *
from crcmod import *
import time
import struct
import binascii
import random
import threading
import serial


def now_time(st = '%Y%m%d%H%M%S'):
    return time.strftime(st, time.localtime(time.time()))

def save(data):
    with open(PATH, 'a') as f:
        f.write(data)
        f.write('\n')

def save_print(data):
    with open(PATH, 'a') as f:
        f.write(data)
        f.write('\n')
        print(data)

def flowt2hex(a):
    res = binascii.hexlify(struct.pack("<f", a)).decode().upper()
    res = daxiaoduan(res,2)
    res = daxiaoduan(res)
    return res

def daxiaoduan(data, n = 4):
    res = ''
    for i in range(0, len(data), n):
        res = data[i:i+n] + res
    return res

# CRC16-MODBUS
def crc16Add(read):
    crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
    data = read.replace(" ", "")
    readcrcout = hex(crc16(unhexlify(data))).upper()
    res = readcrcout[2:].rjust(4,'0')
    return res


class serialss(serial.Serial):
    def __init__(self, port, baudrate=9600):
        super(serialss, self).__init__()
        self.port = port
        self.baudrate = baudrate
        self.err = []
        self.opened()

    def send(self, data):
        data = self.protocol(data)
        if not isinstance(data, str):
            self.err.append('{} | "send" type(str) Err {}'.format(now_time(),str(data)))
            print(self.err[-1])
            return False

        if len(data) % 2 != 0:
            self.err.append('{} | "send" length(data) Err {}'.format(now_time(), str(data)))
            print(self.err[-1])
            return False

        if not self.is_open:
            self.opened()
        try:
            data = binascii.unhexlify(data.encode())
            self.write(data)
            self.flush()
            return True
        except Exception as e:
            self.err.append('{} | {} Err {}'.format(now_time(), str(e), str(data)))
            return False

    def readdddd(self):
        if self.in_waiting:
            recv = self.read_all()
            try:
                print(binascii.hexlify(recv).decode())
            except:
                print(recv)
            self.flushInput()
            return recv


    def recv(self,waiting_time = 30):
        '''默认等待读取时间为6秒'''
        if not self.is_open:
            self.err.append('{} | "send" open status Err'.format(now_time()))
            return False
        try:
            for i in range(30):
                in_waitings = self.in_waiting
                if in_waitings:
                    return True
                time.sleep(1)
        except Exception as e:
            self.err.append('{} | {} Err'.format(now_time(), str(e)))

    def recv_parse(self, data):
        parse_data = ''
        parse = True
        if parse:
            try:
                parse_data = binascii.hexlify(parse_data).decode().upper()
                parse = False
            except:
                parse = True
        if parse:
            try:
                parse_data = data.decode('ascii')
                parse = False
            except:
                parse = True
        if parse:
            try:
                parse_data = data.decode('GBK').replace('\n','').replace('\r','')
                parse = False
            except:
                parse = True

        if not parse:
            return parse_data

    def opened(self):
        if not self.is_open:
            self.open()

    def closed(self):
        if self.is_open:
            self.close()




    def protocol(self,data):
        p1 = '010340'
        cumelate_gk = flowt2hex(data['cumulate_gk'])
        cumelate_bk = flowt2hex(data['cumulate_bk'])
        p2 = '00000000' * 8
        pressure = flowt2hex(101.685)
        temperature = flowt2hex(20.00)
        p3 = '00000000' * 1 + '65 16 43 AD'.replace(' ','')

        flow_gk = '00000000'
        flow_bk = '00000000'
        res = (p1+cumelate_gk+cumelate_bk+p2+pressure+temperature+ p3+flow_gk+flow_bk).replace(' ','').upper()
        pcrc = daxiaoduan(crc16Add(res),2)
        res = res + pcrc
        print(res)
        pd = [
            'cumelate_gk : | {} | {}'.format(cumelate_gk,data['cumulate_gk']),
            'cumelate_bk : | {} | {}'.format(cumelate_bk, data['cumulate_bk']),

               ]
        for i in pd:
            print(i)
        return res



class zhonghe():
    def __init__(self, port):
        self.ser = serialss(port)


        self.cumulate_gk = 1925725.4928764955   #正向工况累计流量(m3)
        self.cumulate_bk = 1949755.545337843   #正向标况累计流量(m3)
        # self.cumulate_gk_reverse = 0  # 反向工况累计流量(m3)
        # self.cumulate_bk_reverse = 0   #反向标况累计流量(m3)



        # self.pressure = 101.685   #压力(kPa)
        # self.temperature = 20   #温度(℃)
        # self.average_flow = 0   #平均流速(m/s)
        # self.average_sound_speed = 0   #平均声速(m/s)
        self.flow_gk = 0  # 工况瞬时流量(m3/h)
        self.flow_bk = 0  # 标况瞬时流量(m3/h)


    def run(self):
        locks = threading.Lock()
        p = threading.Thread(target=self.zhwsRUN, args=(locks,))
        p.start()
        gk = 0
        while True:
            recv_data = self.ser.readdddd()
            if recv_data:
                with locks:
                    if not gk:
                        gk = self.cumulate_gk
                    bk = self.cumulate_bk
                    data = {
                            'cumulate_gk': gk,
                            'cumulate_bk': bk,
                    }
                    print(self.ser.send(data))
                    print('send OK \n')
                    self.ser.flush()
                    gk = bk
                recv_data = False
            time.sleep(1)


    def read_cumulate(self):
        ser2 = serialss(port2)


    def read_pro(self):
        p1 = '68 FF FF FF FF FF FF 68 01 0A 00'
        p2 =  now_time(st = '%y%m%d%H%M%S')
        p3 =  '02 02 AA 00'
        pc = self.checkSum((p1+p2+p3))
        return (p1+p2+p3+pc+'16').replace(' ','')

    def checkSum(self, data):
        data = data.replace(' ', '').replace('\n', '').replace('\t', '')
        SUM = 0
        for i in range(0, len(data), 2):
            SUM += int(data[i:i + 2], 16)
        res = hex(SUM)[2:].rjust(2, '0')[-2:]
        return res.upper()

    def zhwsRUN(self, locks):
        c = [float(i / 100) for i in range(50, 599)]
        while True:
            t1 = time.time()
            with locks:
                self.flow_bk = 2400 + self.randomdata(c)
                self.flow_gk = 2400+ self.randomdata(c)
            time.sleep(1)

            t2 = time.time() - t1
            with locks:
                self.cumulate_bk = self.cumulate_bk + t2 * self.flow_bk
                self.cumulate_gk = self.cumulate_gk + t2 * self.flow_gk


    def randomdata(self, c):
        n = -1
        if random.randint(0,100) < 50: n = 1
        res = n * random.choice(c)
        return res

if __name__ == '__main__':
    # print(crc16Add("01 03 61 00 00 02"))
    a = zhonghe('com5')
    a.run()
