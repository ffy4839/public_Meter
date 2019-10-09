import serial
from binascii import *
from crcmod import *
import time
import struct
import random
import threading


def time_now(struct = '%Y-%m-%d %H:%M:%S'):
    return time.strftime(struct, time.localtime(time.time()))
