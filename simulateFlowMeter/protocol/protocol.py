from flowMeter.bin.func import *



class protocol():
    def __init__(self):
        pass

    def run(self, data):
        pass


    def float2hex(self, data):
        res = hexlify(struct.pack("<f", data)).decode().upper()
        res = self.endian(res, 2)
        res = self.endian(res)
        return res

    def endian(self, data, n=4):
        res = ''
        for i in range(0, len(data), n):
            res = data[i:i + n] + res
        return res

    # CRC16-MODBUS
    def crc16Add(self, read):
        crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
        data = read.replace(" ", "")
        readcrcout = hex(crc16(unhexlify(data))).upper()
        res = readcrcout[2:].rjust(4, '0')
        return res


class sendData():
    def __init__(self):
        pass

    def zhongHeWeiSi(self, data):
        #中核维斯流量计
        # 工标况累积量，工标况流量，温度压力
        pass

