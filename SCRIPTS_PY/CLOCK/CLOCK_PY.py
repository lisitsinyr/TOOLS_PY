"""CLOCK_PY.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2022-2025
 Author:
     Lisitsin Y.R.
 Project:
     SCRIPTS_PY
 Module:
     CLOCK_PY.py

 =======================================================
"""

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
from tkinter import Label, Tk
import time

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------


#------------------------------------------
# 
#------------------------------------------

#------------------------------------------
def main ():
    """main"""
#beginfunction
    app_window = Tk ()
    app_window.title ("Digital Clock")
    app_window.geometry ("420x150")
    app_window.resizable (1, 1)

    text_font = ("Boulder", 68, 'bold')
    background = "#f2e750"
    foreground = "#363529"
    border_width = 25
    label = Label (app_window, font=text_font, bg=background,
                   fg=foreground, bd=border_width)
    label.grid (row=0, column=1)


    def digital_clock ():
        """digital_clock"""
    # beginfunction
        time_live = time.strftime ("%H:%M:%S")
        label.config (text=time_live)
        label.after (200, digital_clock)
    # endfunction

    digital_clock()
    app_window.mainloop()
#endfunction

#------------------------------------------
#
#------------------------------------------
#beginmodule
if __name__ == "__main__":
    main()
#endif

#endmodule
