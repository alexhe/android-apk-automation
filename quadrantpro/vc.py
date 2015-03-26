#!/usr/bin/env python
# Author:
# Xavier Hsu <xavier.hsu@linaro.org>
import re
import sys
import os
import time

from subprocess import call
from com.dtmilano.android.viewclient import ViewClient, ViewNotFoundException

kwargs1 = {'verbose': False, 'ignoresecuredevice': False}
device, serialno = ViewClient.connectToDeviceOrExit(**kwargs1)
kwargs2 = {'startviewserver': True, 'forceviewserveruse': False, 'autodump': False, 'ignoreuiautomatorkilled': True, 'compresseddump': False}

vc = ViewClient(device, serialno, **kwargs2)

vc.dump()
view_license_btn = vc.findViewWithText("View license")
if view_license_btn:
    ok_button = vc.findViewWithTextOrRaise("OK")
    ok_button.touch()

vc.dump()
run_full_item=vc.findViewWithTextOrRaise(u'Run full benchmark')
run_full_item.touch()

finished = False
while(not finished):
    try:
        time.sleep(5)
        vc.dump()
        vc.findViewByIdOrRaise("com.aurorasoftworks.quadrant.ui.professional:id/chart")
        finished = True
        print "Benchmark finished"
    except ViewNotFoundException:
        pass
    except RuntimeError:
        pass
    except ValueError:
        pass
