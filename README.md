# linux-undervolt
Undervolt CPU on Linux

## Disclaimer
I take no responsibility for any damage done to your system. This was only tested
on an Intel i7-6700HQ (My system is a Dell XPS 15 9550)

For a safer alternative, if you are dual booting Windows, use the [Intel® Extreme Tuning Utility](https://downloadcenter.intel.com/download/24075/Intel-Extreme-Tuning-Utility-Intel-XTU-) and reboot back into Linux.

## Dependencies
* [msr-tools](https://01.org/msr-tools)

## Instructions
Make sure you have the msr module loaded.
```shell
modprobe msr
```
### Usage
```
usage: undervolt.py [-h] [--cpu-core mV] [--intel-gpu mV] [--cpu-cache mV]
                    [--system-agent mV] [--analog-io mV] [-r] [-c]

Undervolt Intel i7 6700HQ (not tested on others)

optional arguments:
  -h, --help         show this help message and exit
  --cpu-core mV      undervolt the cpu core
  --intel-gpu mV     undervolt the intel gpu
  --cpu-cache mV     undervolt the cpu cache
  --system-agent mV  undervolt the system agent
  --analog-io mV     undervolt the analog I/O
  -r, --reset        reset voltages
  -c, --check        check undervoltage
```

## Credits
* @[mihic](https://www.github.com/mihic) for writing [this](https://github.com/mihic/linux-intel-undervolt) guide
* @[andikleen](https://github.com/andikleen) for his python msr [functions](https://github.com/andikleen/pmu-tools/blob/master/msr.py)
* [This](http://forum.notebookreview.com/threads/undervolting-e-g-skylake-in-linux.807953/) forum on notebookreview.com
