import threading
from sys import exit

try:
    import usb.core
    import usb.util
except ImportError:
    exit("This script requires the pyusb module\nInstall with: sudo pip install pyusb")


class StoppableThread(threading.Thread):
    """Basic stoppable thread wrapper
    Adds Event for stopping the execution loop and exiting cleanly."""
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.daemon = True

    def start(self):
        if not self.isAlive():
            self.stop_event.clear()
            threading.Thread.start(self)

    def stop(self):
        if self.isAlive():
            # set event to signal thread to terminate
            self.stop_event.set()
            # block calling thread until thread really has terminated
            self.join()


class AsyncWorker(StoppableThread):
    """Basic thread wrapper class for asyncronously running functions
    Basic thread wrapper class for running functions asyncronously. Return False from your function to abort looping."""
    def __init__(self, todo):
        StoppableThread.__init__(self)
        self.todo = todo

    def run(self):
        while not self.stop_event.is_set():
            if self.todo() is False:
                break


UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
BUTTON = 'enter'

handlers = {}
directions = {
    'up': 82,
    'down': 81,
    'left': 80,
    'right': 79,
    'enter': 40
}

dev = usb.core.find(idVendor=0x1997, idProduct=0x2433)

if dev is None:
    exit('USB device not found!')

endpoint = dev[0][(0, 0)][0]

if dev.is_kernel_driver_active(0) is True:
    dev.detach_kernel_driver(0)

usb.util.claim_interface(dev, 0)


def on(button, bouncetime=0):
    def register(handler):
        handlers[button] = handler

    return register


def repeat(button, handler, delay, speed):
    pass


def poll():
    control = None
    try:
        control = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
    except:
        pass
    if control:
        for direction in directions.keys():
            if directions[direction] in control:
                if direction in handlers.keys():
                    handlers[direction](directions[direction])


p = AsyncWorker(poll)
p.start()
