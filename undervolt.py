#!/usr/bin/python
# Got most of my info here: https://github.com/mihic/linux-intel-undervolt
# and here: http://forum.notebookreview.com/threads/undervolting-e-g-skylake-in-linux.807953/
# uses msr-tools which can be found here: https://01.org/msr-tools

import os
import sys
import argparse
import subprocess

def twos_comp(val, bits):
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
        return val

# convert negative decimal to two's complement hex
def convertmVtoHex(n):
    return format(0xFFE00000&( (round(n*1.024)&0xFFF) <<21), '08x')

def convertHextomV(n):
    return round(twos_comp(int(hex(n >>21), 16), 11) / 1.024)

def writeValues(value, index):
    if int(value) > 0:
        print("mV should be a negative number or zero!")
        sys.exit()

    msr_register = "0x150"
    constant = 80000
    single_const = 1
    read_write = 1
    offset = convertmVtoHex(int(value))
    val = "0x" + str(constant) + str(index) + str(single_const) + str(read_write) + offset
    # still need to figure out how to write to register without dependencies
    subprocess.call(["wrmsr", msr_register, val])

def checkValues():
    msr_register = "0x150"
    constant = 80000
    single_const = 1
    read_write = 0
    offset = convertmVtoHex(0)
    for x in range(0, 5):
        value = "0x" + str(constant) + str(x) + str(single_const) + str(read_write) + str(offset)
        # still need to figure out how to write to register without dependencies
        subprocess.call(["wrmsr", msr_register, value])
        print(str(x) + ":")
        # still need to figure out how to read from register without dependencies
        p = subprocess.Popen(["rdmsr", msr_register], stdout=subprocess.PIPE)
        out, err = p.communicate()
        out = out.decode('utf-8').rstrip()
        if err is not None:
            print(err)
        print(str(out) + " --> " + str(convertHextomV(int(out, 16))))

if __name__ == '__main__':
    if os.getuid() != 0:
        args = ['sudo', sys.executable] + sys.argv + [os.environ]
        os.execlpe('sudo', *args)
    parser = argparse.ArgumentParser(description='Undervolt Intel i7 6700HQ (not tested on others)')
    parser.add_argument('--cpu-core', metavar='mV', help='undervolt the cpu core', action='store')
    parser.add_argument('--intel-gpu', metavar='mV', help='undervolt the intel gpu', action='store')
    parser.add_argument('--cpu-cache', metavar='mV', help='undervolt the cpu cache', action='store')
    parser.add_argument('--system-agent', metavar='mV', help='undervolt the system agent', action='store')
    parser.add_argument('--analog-io', metavar='mV', help='undervolt the analog I/O', action='store')
    parser.add_argument('-r', '--reset', help='reset voltages', action='store_true')
    parser.add_argument('-c', '--check', help='check undervoltage', action='store_true')

    a = parser.parse_args()

    # probably a better way to do this
    indicies = {"0":a.cpu_core, "1":a.intel_gpu, "2":a.cpu_cache, "3":a.system_agent, "4":a.analog_io}
    for key, value in indicies.items():
        if value is not None:
            writeValues(value, key)
    if a.reset:
        for key, value in indicies.items():
            writeValues(0, key)
    if a.check:
        checkValues()
