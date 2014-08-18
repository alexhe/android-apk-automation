# Author: Botao Sun <botao.sun@linaro.org>
# First touch on GLBenchmark

import time
import re
from com.dtmilano.android.viewclient import ViewClient

device, serialno = ViewClient.connectToDeviceOrExit()
vc = ViewClient(device, serialno)
time.sleep(2)

apps_tab = vc.findViewWithContentDescriptionOrRaise(re.compile('Apps'))
apps_tab.touch()
time.sleep(5)

vc.dump(window='-1')
target_app = vc.findViewWithText("GLBenchmark 2.5.1")
target_app.touch()
print "GLBenchmark 2.5.1 touched!"
time.sleep(15)

device.press('KEYCODE_BACK')
time.sleep(3)
