import sys

external_module_path = r'C:\Users\over\Desktop\external_dir'
sys.path.append(external_module_path)
try:
    from aa__ import *
except ModuleNotFoundError:
    print(
        'External module path: "' + external_module_path + '" has no current module. Please check module name according Docs.')
    input('\nPress "enter" to exit.\n')
    exit()
def A():
    wevas="sgsadaf"
    print(locals())
sdfe='vberaewrdc'
enumerate(sdfe)

globals()['p'](locals()['sdfe'])
globals()['A']()
