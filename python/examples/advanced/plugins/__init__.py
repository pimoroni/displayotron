import sys

if sys.version_info[0] >= 3:
    from .radio import Radio
    from .volume import Volume
    from .graph import GraphCPU, GraphTemp
    from .debris import Debris
    from .utils import Backlight, Contrast
    from .clock import Clock
    from .stocks import Stocks
    from .transmission import Transmission
else:
    from radio import Radio
    from volume import Volume
    from graph import GraphCPU, GraphTemp
    from debris import Debris
    from utils import Backlight, Contrast
    from clock import Clock
    from stocks import Stocks
    from transmission import Transmission
