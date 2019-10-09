from flowMeter.bin.func import *


class flow_meter():
    def __init__(self, flow=0, cumulate=0, pressure=101.325, temperature=20.00):
        self.set_flow(flow)
        self.set_cumulate(cumulate)
        self.set_pressure(pressure)
        self.set_temperature(temperature)


    def init_parameter(self):
        self.flow_work = 0
        self.flow_standard = 0

        self.cumulate_work = 0
        self.cumulate_standard = 0

        self.pressure = 0
        self.temperature = 0

    def get(self, lock):
        with lock:
            res = {
                'flow_work' : round(self.flow_work,5),
                'flow_standard': round(self.flow_standard,5),

                'cumulate_work': round(self.cumulate_work,5),
                'cumulate_standard': round(self.cumulate_standard,5),

                'pressure': round(self.pressure,5),
                'temperature': round(self.temperature,5),
                    }
            return res

    def run(self,n=5):
        while True:
            t1 = time.time()
            self.run_pressure()
            self.run_temprature()
            self.run_modulus()
            self.run_flow()
            time.sleep(1/10**n)
            self.run_cumulate(time.time()-t1)

    def run_flow(self):
        self.flow_work = self.flow_base + self.random_parameter(bits=6)
        self.flow_standard = self.flow_work * self.modulus

    def run_cumulate(self, t):
        t = float(t/3600)
        self.cumulate_work += self.flow_work * t
        self.cumulate_standard += self.flow_standard * t
        # print(self.cumulate_standard-self.cumulate_work)

    def run_pressure(self):
        self.pressure  = self.pressure_base + self.random_parameter(bits=6)

    def run_temprature(self):
        self.temperature  = self.temperature_base + self.random_parameter(bits=6)

    def run_modulus(self):
        # 补偿系数
        stemp = 29315 / (27315 + self.temperature * 100)
        spres = self.pressure * 1000 / 101325
        self.modulus = stemp * spres

    def random_parameter(self, range=1, bits=1, zf=0):
        #流量波动 range：范围0-range, bits：小数位数
        pn = 1
        if not zf:
            if random.randint(1,10) <= 5:
                pn = -1
        elif zf < 0:
            pn = -1
        tn = 10 ** bits
        tr = range * tn
        res = pn * round(float(random.randint(1,tr)/tn), bits)
        return res

    def set_cumulate(self, cumulate):
        self.cumulate_work = cumulate
        self.cumulate_standard = cumulate

    def set_flow(self, flow):
        self.flow_base = flow

    def set_pressure(self, pressure):
        # 压力设置，压力范围30-120
        if pressure > 120:
            pressure = 120
        elif pressure < 30:
            pressure = 30
        self.pressure_base = pressure
        return True

    def set_temperature(self, temperature):
        # 温度设置，温度范围-40 — 80
        if temperature > 80:
            temperature = 80
        elif temperature < -40:
            temperature = -40
        self.temperature_base = temperature
        return True


if __name__ =='__main__':
    locks = threading.Lock()
    a = flow_meter(flow=500, cumulate=10, )
    p = threading.Thread(target=a.run,args=())
    p.start()
    while True:
        res = a.get(locks)
        print(res)
        time.sleep(1)
        print('\n')


