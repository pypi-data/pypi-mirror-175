## How to install 
pip install vlt-comm

## How to use:

from FcBus.VltOp import *

from FcBus.dbglog import *

### Examples:
    ## import all functions from the module
    from FcBus.VltOp import *
    from FcBus.dbglog import *

    ## find and open port for vlt communication(auto set baudrate to 115200)
    findb()   #Note: Only support one driver connected at same time

    ## Write 0 to parameter 110
    p[110] = 0

    ## Read parameter 3821 with index = 8
    p[3821.08]

    ## Close serial port 
    pclose()

    ## Open serial port
    ope() or p.open()

    ## Let the driver go into testmonitor mode
    tm()

    ## Reset the driver
    reset()


## Get all supported functions:
dir()


## New commands 

### since 0.0.12
laoc(filepath)

llang(filepath)

### since 0.0.13
lmoc(filepath)

lpud(filepath)

u = ui(g1614) #paramter monitor