from Xlib import display
from Xlib.Xatom import STRING

# Function to set WM_CLASS for the window
def set_wm_class(win_id, instance_name, class_name):
    # Set the WM_CLASS property for a window.
    disp = display.Display()
    window = disp.create_resource_object('window', win_id)
    wm_class_atom = disp.intern_atom('WM_CLASS')
    value = f'{instance_name}\0{class_name}\0'.encode('utf-8')
    window.change_property(wm_class_atom, STRING, 8, value)
    disp.flush()