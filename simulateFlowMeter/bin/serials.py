from flowMeter.bin.func import *


class serial_flowMeter(serial.Serial):
    def __init__(self, port, baudrate=9600):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.err = []
        self.opened()

    def send(self, data):
        if not isinstance(data, str):
            self.err.append('{} | "send" type(str) Err {}'.format(time_now(),str(data)))
            print(self.err[-1])
            return False

        if len(data) % 2 != 0:
            self.err.append('{} | "send" length(data) Err {}'.format(time_now(), str(data)))
            print(self.err[-1])
            return False

        if not self.is_open:
            self.opened()


        try:
            data = unhexlify(data.encode())
            self.write(data)
            self.flush()
            return True
        except Exception as e:
            self.err.append('{} | {} Err {}'.format(time_now(), str(e), str(data)))
            return False

    def recv(self,waiting_time = 30):
        '''默认等待读取时间为6秒'''
        if not self.is_open:
            self.opened()
        try:
            for i in range(30):
                in_waitings = self.in_waiting
                if in_waitings:
                    return True
                time.sleep(1)
        except Exception as e:
            self.err.append('{} | {} Err'.format(time_now(), str(e)))

    def recv_parse(self, data):
        parse_data = ''
        parse = True
        if parse:
            try:
                parse_data = hexlify(parse_data).decode().upper()
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

