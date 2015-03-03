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

time.sleep(2)
vc.dump()
btn_license = vc.findViewWithText(u'I Agree')
if btn_license:
    btn_license.touch()

while True:
    try:
        time.sleep(5)
        vc.dump()
        btn_start_on = vc.findViewByIdOrRaise("com.eembc.andebench:id/s1_runall")
        btn_start_on.touch()
        break
    except ViewNotFoundException:
        pass
    except RuntimeError:
        pass
    except ValueError:
        pass

while(True):
    try:
        time.sleep(30)
        vc.dump('-1')
        vc.findViewByIdOrRaise("com.eembc.andebench:id/view_web_button")

        vc.findViewWithTextOrRaise(u'3D').touch()
        vc.findViewWithTextOrRaise(u'Platform').touch()
        vc.findViewWithTextOrRaise(u'Storage').touch()
        vc.findViewWithTextOrRaise(u'Memory Latency').touch()
        vc.findViewWithTextOrRaise(u'Memory Bandwidth').touch()
        vc.findViewWithTextOrRaise(u'CoreMark-HPC (Peak)').touch()
        vc.findViewWithTextOrRaise(u'CoreMark-HPC (Base)').touch()
        break
    except ViewNotFoundException:
        pass
    except RuntimeError:
        pass
    except ValueError:
        pass
