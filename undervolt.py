#!/usr/bin/python
# Got most of my info here: https://github.com/mihic/linux-intel-undervolt
# and here:
# http://forum.notebookreview.com/threads/undervolting-e-g-skylake-in-linux.807953/
# uses msr-tools which can be found here: https://01.org/msr-tools

import argparse
import glob
import os
import struct
import sys


def writemsr(msr, val):
    n = glob.glob('/dev/cpu/[0-9]*/msr')
    for c in n:
        f = os.open(c, os.O_WRONLY)
        os.lseek(f, msr, os.SEEK_SET)
        os.write(f, struct.pack('Q', val))
        os.close(f)
    if not n:
        raise OSError("msr module not loaded (run modprobe msr)")


def readmsr(msr, cpu=0):
    f = os.open('/dev/cpu/%d/msr' % (cpu,), os.O_RDONLY)
    os.lseek(f, msr, os.SEEK_SET)
    val = struct.unpack('Q', os.read(f, 8))[0]
    os.close(f)
    return val

# convert negative decimal to two's complement hex


def convertmVtoHex(n):
    return format(0xFFE00000 & ((round(n * 1.024) & 0xFFF) << 21), '08x')

# convert two's complement hex to negative decimal


def convertHextomV(n):
    if n == 0:
        return 0
    # only works for negative numbers lol hopefully that's good enough
    return ~ round((((n >> 21) ^ 0xFFF) - 2048) / 1.024)


def writeValues(value, index):
    if int(value) > 0:
        print("mV should be a negative number or zero!")
        sys.exit()

    msr_register = 0x150
    constant = 80000
    single_const = 1
    read_write = 1
    offset = convertmVtoHex(int(value))

    val = "0x" + str(constant) + str(index) + \
        str(single_const) + str(read_write) + offset
    writemsr(msr_register, int(val, 16))


def checkValues():
    msr_register = 0x150
    constant = 80000
    single_const = 1
    read_write = 0
    offset = convertmVtoHex(0)
    index_names = ["cpu_core", "intel_gpu",
                   "cpu_cache", "system_agent", "analog_io"]
    for x in range(0, 5):
        value = "0x" + str(constant) + str(x) + \
            str(single_const) + str(read_write) + str(offset)
        writemsr(msr_register, int(value, 16))
        print(str(x) + ", " + index_names[x] + ":")
        out = readmsr(msr_register)
        print(str(hex(out)) + " --> " + str(convertHextomV(out)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Undervolt Intel i7 6700HQ (not tested on others)')
    parser.add_argument(
        '--cpu-core',
        metavar='mV',
        help='undervolt the cpu core',
        action='store'
    )
    parser.add_argument(
        '--intel-gpu',
        metavar='mV',
        help='undervolt the intel gpu',
        action='store'
    )
    parser.add_argument(
        '--cpu-cache',
        metavar='mV',
        help='undervolt the cpu cache',
        action='store'
    )
    parser.add_argument(
        '--system-agent',
        metavar='mV',
        help='undervolt the system agent',
        action='store'
    )
    parser.add_argument(
        '--analog-io',
        metavar='mV',
        help='undervolt the analog I/O',
        action='store'
    )
    parser.add_argument(
        '-l',
        '--list',
        metavar='\b',
        nargs=5,
        type=int,
        help='apply undervolt as list in the above order',
        action='store'
    )
    parser.add_argument(
        '-r',
        '--reset',
        help='reset voltages',
        action='store_true'
    )
    parser.add_argument(
        '-c',
        '--check',
        help='check undervoltage',
        action='store_true'
    )

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    a = parser.parse_args()

    if os.getuid() != 0:
        args = ['sudo', sys.executable] + sys.argv + [os.environ]
        os.execlpe('sudo', *args)

    # probably a better way to do this
    indicies = {"0": a.cpu_core, "1": a.intel_gpu,
                "2": a.cpu_cache, "3": a.system_agent, "4": a.analog_io}

    if a.check:
        checkValues()
        sys.exit()

    if a.reset:
        for key, value in indicies.items():
            writeValues(0, key)
        sys.exit()

    for key, value in indicies.items():
        if value is not None:
            writeValues(value, key)
        elif a.list is not None:
            writeValues(a.list[int(key)], key)
