from pynput.keyboard import Listener
from pymem.process import *
from pymem import *

fov = None

class Client:

    def __init__(self):
      
            try:
                mem = Pymem("Minecraft")
            except pymem.exception.ProcessNotFound:
                return

            module = module_from_name(mem.process_handle, "Minecraft.Windows.exe").lpBaseOfDll
            mods = {"Zoom": 0x048DFFD8, "OffSetsZoom": [0x6F8, 0x4D0, 0x10, 0x178, 0x18]}

            def GetPointer(base, offsets):
                addr = mem.read_longlong(base)
                for offset in offsets:
                    if offset != offsets[-1]:
                        try:
                            addr = mem.read_longlong(addr + offset)
                        except:
                            exit()
                return addr + offsets[-1]

            global fov
            
            fov = mem.read_float(GetPointer(module + mods["Zoom"], mods["OffSetsZoom"]))

            def on_press(key):
                key = str(key).lower().replace("'", "")
                if key == "c":
                    mem.write_float(GetPointer(module + mods["Zoom"], mods["OffSetsZoom"]), 30.0)

            def on_release(key):
                key = str(key).lower().replace("'", "")
                if key == "c":
                    mem.write_float(GetPointer(module + mods["Zoom"], mods["OffSetsZoom"]), fov)

            with Listener(on_press=on_press, on_release=on_release) as listener:
                listener.join()

client = Client()
