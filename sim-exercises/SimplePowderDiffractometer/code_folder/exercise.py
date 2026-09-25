import mcstasscript as ms
from mcstasscript.jb_interface import show
import code_folder.SimplePowderDiffractometer_generated as PowdDiffr

def make():
    # simple function to provide instrument if they want to play with it
    return PowdDiffr.make(input_path="code_folder")

def show_widget():
    # simple function to provide widget
    instr = PowdDiffr.make(input_path="code_folder")
    return show(instr)
