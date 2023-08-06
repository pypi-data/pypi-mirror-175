# Start/stop functions/methods with hotkeys!

```python
$pip install pykeycontrol
from pykeycontrol import StopStart
from time import sleep
def testest2():
    startstop = StopStart(hotkey_enable="ctrl+alt+p",
                          hotkey_disable="ctrl+alt+o",
                          hotkey_hc_exit="ctrl+alt+e", )
    startstop.reset_all_hotkeys().add_hotkeys()
    startstop.stop = False
    while startstop.stop is False:
        print('baba')
        sleep(1)
		
		
		
class NewClass:
    def __init__(self):
        self.startstop = StopStart(hotkey_enable="ctrl+alt+p",
                                   hotkey_disable="ctrl+alt+o",
                                   hotkey_hc_exit="ctrl+alt+e", )
        self.startstop.add_hotkeys()
        self.startstop.stop = False
    def testest(self):
        while self.startstop.stop is False:
            print('baba')
            sleep(1)
			
			
testest2()
baba
baba
baba
baba
baba
HARDCORE EXIT! FTW!
Process finished with exit code 1   #"ctrl+alt+e"

nac=NewClass()
nac.testest()
baba
baba
baba
baba
baba
baba
baba
baba
Disabled! #"ctrl+alt+o"

```