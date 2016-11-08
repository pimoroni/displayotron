import fcntl
import socket
import struct
import subprocess
import time
from sys import exit

try:
    import psutil
except ImportError:
    exit("This library requires the psutil module\nInstall with: sudo pip install psutil")

from dot3k.menu import MenuOption


def run_cmd(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = p.communicate()[0]
    return output


class IPAddress(MenuOption):
    """
    A plugin which gets the IP address for wlan0
    and eth0 and displays them on the screen.
    """
    def __init__(self):
        self.mode = 0
        self.wlan0 = self.get_addr('wlan0')
        self.eth0 = self.get_addr('eth0')
        self.is_setup = False
        MenuOption.__init__(self)

    def get_addr(self, ifname):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            return socket.inet_ntoa(fcntl.ioctl(
                s.fileno(),
                0x8915,  # SIOCGIFADDR
                struct.pack('256s', ifname[:15].encode('utf-8'))
            )[20:24])
        except IOError:
            return 'Not Found!'

    def redraw(self, menu):
        if not self.is_setup:
            menu.lcd.create_char(0, [0, 4, 14, 0, 0, 14, 4, 0])  # Up down arrow
            self.is_setup = True

        menu.write_row(0, 'IP Address')
        if self.mode == 0:
            menu.write_row(1, chr(0) + ' Wired:')
            menu.write_row(2, self.eth0)
        else:
            menu.write_row(1, chr(0) + ' Wireless:')
            menu.write_row(2, self.wlan0)

    def down(self):
        self.mode = 1

    def up(self):
        self.mode = 0

    def left(self):
        return False

    def cleanup(self):
        self.is_setup = False


class GraphCPU(MenuOption):
    """
    A simple "plug-in" example, this gets the CPU load
    and draws it to the LCD when active
    """

    def __init__(self, backlight=None):
        self.backlight = backlight
        self.cpu_samples = [0, 0, 0, 0, 0]
        self.cpu_avg = 0
        self.last = self.millis()
        MenuOption.__init__(self)

    def redraw(self, menu):
        now = self.millis()
        if now - self.last < 1000:
            return false

        self.cpu_samples.append(psutil.cpu_percent())
        self.cpu_samples.pop(0)
        self.cpu_avg = sum(self.cpu_samples) / len(self.cpu_samples)

        self.cpu_avg = round(self.cpu_avg * 100.0) / 100.0

        menu.write_row(0, 'CPU Load')
        menu.write_row(1, str(self.cpu_avg) + '%')
        menu.write_row(2, '#' * int(16 * (self.cpu_avg / 100.0)))

        if self.backlight is not None:
            self.backlight.set_graph(self.cpu_avg / 100.0)

    def left(self):
        if self.backlight is not None:
            self.backlight.set_graph(0)
        return False


class GraphTemp(MenuOption):
    """
    A simple "plug-in" example, this gets the Temperature
    and draws it to the LCD when active
    """

    def __init__(self):
        self.last = self.millis()
        MenuOption.__init__(self)

    def get_cpu_temp(self):
        tempFile = open("/sys/class/thermal/thermal_zone0/temp")
        cpu_temp = tempFile.read()
        tempFile.close()
        return float(cpu_temp) / 1000

    def get_gpu_temp(self):
        proc = subprocess.Popen(['/opt/vc/bin/vcgencmd', 'measure_temp'], stdout=subprocess.PIPE)
        out, err = proc.communicate()
        out = out.decode('utf-8')
        gpu_temp = out.replace('temp=', '').replace('\'C', '')
        return float(gpu_temp)

    def redraw(self, menu):
        now = self.millis()
        if now - self.last < 1000:
            return False

        menu.write_row(0, 'Temperature')
        menu.write_row(1, 'CPU:' + str(self.get_cpu_temp()))
        menu.write_row(2, 'GPU:' + str(self.get_gpu_temp()))


class GraphNetTrans(MenuOption):
    """
    Gets the total transferred amount of the raspberry and displays to the LCD, ONLY on eth0.
    """

    def __init__(self):
        self.last = self.millis()
        MenuOption.__init__(self)

    def get_down(self):
        show_dl_raw = ""
        show_dl_hr = "ifconfig eth0 | grep bytes | cut -d')' -f1 | cut -d'(' -f2"
        hr_dl = run_cmd(show_dl_hr)
        return hr_dl

    def get_up(self):
        show_ul_raw = ""
        show_ul_hr = "ifconfig eth0 | grep bytes | cut -d')' -f2 | cut -d'(' -f2"
        hr_ul = run_cmd(show_ul_hr)
        return hr_ul

    def redraw(self, menu):
        now = self.millis()
        if now - self.last < 1000:
            return false

        menu.write_row(0, 'ETH0 Transfers')
        menu.write_row(1, str('Dn:' + self.get_down())[:-1])
        menu.write_row(2, str('Up:' + self.get_up())[:-1])


class GraphNetSpeed(MenuOption):
    """
    Gets the total network transferred amount of the raspberry and displays to the LCD, ONLY on eth0.
    """

    def __init__(self):
        self.last = self.millis()
        self.last_update = 0
        self.raw_dlold = 0
        self.raw_ulold = 0
        self.dlspeed = 0
        self.ulspeed = 0
        self.iface = 'eth0'
        MenuOption.__init__(self)

    def get_current_down(self, iface='eth0'):
        show_dl_raw = "ifconfig " + iface + " | grep bytes | cut -d':' -f2 | cut -d' ' -f1"
        raw_dl = run_cmd(show_dl_raw)
        return raw_dl[:-1]

    def get_current_up(self, iface='eth0'):
        show_ul_raw = "ifconfig " + iface + " | grep bytes | cut -d':' -f3 | cut -d' ' -f1"
        raw_ul = run_cmd(show_ul_raw)
        return raw_ul[:-1]

    def up(self):
        self.iface = 'eth0'

    def down(self):
        self.iface = 'wlan0'

    def redraw(self, menu):
        if self.millis() - self.last_update > 1000:

            tdelta = self.millis() - self.last_update
            self.last_update = self.millis()

            raw_dlnew = self.get_current_down(self.iface)
            raw_ulnew = self.get_current_up(self.iface)

            self.dlspeed = 0
            self.ulspeed = 0

            try:
                ddelta = int(raw_dlnew) - int(self.raw_dlold)
                udelta = int(raw_ulnew) - int(self.raw_ulold)

                self.dlspeed = round(float(ddelta) / float(tdelta), 1)
                self.ulspeed = round(float(udelta) / float(tdelta), 1)
            except ValueError:
                pass

            self.raw_dlold = raw_dlnew
            self.raw_ulold = raw_ulnew

        menu.write_row(0, self.iface + ' Speed')
        menu.write_row(1, str('Dn:' + str(self.dlspeed) + 'kB/s'))
        menu.write_row(2, str('Up:' + str(self.ulspeed) + 'kB/s'))


class GraphSysShutdown(MenuOption):
    """Shuts down the Raspberry Pi"""

    def __init__(self):
        self.last = self.millis()
        MenuOption.__init__(self)

    def redraw(self, menu):
        shutdown = "sudo shutdown -h now"

        now = self.millis()
        if now - self.last < 1000 * 5:
            return False

        a = run_cmd(shutdown)

        menu.write_row(0, 'RPI Shutdown')
        menu.write_row(1, '')
        menu.write_row(2, time.strftime('  %a %H:%M:%S  '))


class GraphSysReboot(MenuOption):
    """Reboots the Raspberry Pi"""

    def __init__(self):
        self.last = self.millis()
        MenuOption.__init__(self)

    def redraw(self, menu):
        reboot = "sudo reboot"

        now = self.millis()
        if now - self.last < 1000 * 5:
            return False

        a = run_cmd(reboot)

        menu.write_row(0, 'RPI Reboot')
        menu.write_row(1, '')
        menu.write_row(2, time.strftime('  %a %H:%M:%S  '))
