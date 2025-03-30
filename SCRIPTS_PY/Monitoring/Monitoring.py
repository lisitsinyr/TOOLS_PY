"""Monitoring.py"""
# -*- coding: UTF-8 -*-
__annotations__ = """
 =======================================================
 Copyright (c) 2025
 Author:
     Lisitsin Y.R.
 Project:
     SCRIPTS_PY
 Module:
     Monitoring.py
 =======================================================
"""

#------------------------------------------
# БИБЛИОТЕКИ python
#------------------------------------------
import os
import sys
import argparse
import logging
import shutil
import filecmp
import psutil
import time

#------------------------------------------
# БИБЛИОТЕКИ сторонние
#------------------------------------------
from tqdm import tqdm
import json

#------------------------------------------
# БИБЛИОТЕКА lyrpy
#------------------------------------------
import lyrpy.LUos as LUos
import lyrpy.LUDoc as LUDoc
import lyrpy.LULog as LULog
import lyrpy.LUConst as LUConst
import lyrpy.LUDoc as LUDoc
import lyrpy.LULog as LULog
import lyrpy.LUFile as LUFile
import lyrpy.LUParserARG as LUParserARG

#------------------------------------------
# func_pass ()
#------------------------------------------
def func_pass():
    """func_pass"""
#beginfunction
    pass
#endfunction

#-----------------------------------------------------------
# get_cpu_usage ()
#-----------------------------------------------------------
def get_cpu_usage():
    """get_cpu_usage"""
#beginfunction
    return psutil.cpu_percent(interval=1)
#endfunction

#-----------------------------------------------------------
# get_memory_usage ()
#-----------------------------------------------------------
def get_memory_usage():
    """get_memory_usage"""
#beginfunction
    memory = psutil.virtual_memory()
    return {
        'total': memory.total,
        'available': memory.available,
        'used': memory.used,
        'percent': memory.percent
    }
#endfunction

#------------------------------------------
# get_disk_usage ()
#------------------------------------------
def get_disk_usage():
    """get_disk_usage"""
#beginfunction
    disk = psutil.disk_usage('/')
    return {
        'total': disk.total,
        'used': disk.used,
        'free': disk.free,
        'percent': disk.percent
    }
#endfunction

#------------------------------------------
# get_network_usage ()
#------------------------------------------
def get_network_usage():
    """get_network_usage"""
#beginfunction
    net_io = psutil.net_io_counters()
    return {
        'bytes_sent': net_io.bytes_sent,
        'bytes_recv': net_io.bytes_recv,
        'packets_sent': net_io.packets_sent,
        'packets_recv': net_io.packets_recv
    }
#endfunction

#------------------------------------------
# monitor_server (interval=5)
#------------------------------------------
def monitor_server (interval=5):
    """monitor_server"""
#beginfunction
    while True:
        print("\n--- Server Monitoring ---")
        
        # CPU Usage
        cpu_usage = get_cpu_usage()
        print(f"CPU Usage: {cpu_usage}%")

        # Memory Usage
        memory_usage = get_memory_usage()
        print(f"Memory Usage: {memory_usage['percent']}% (Used: {memory_usage['used'] / (1024 ** 3):.2f} GB)")

        # Disk Usage
        disk_usage = get_disk_usage()
        print(f"Disk Usage: {disk_usage['percent']}% (Used: {disk_usage['used'] / (1024 ** 3):.2f} GB)")

        # Network Usage
        network_usage = get_network_usage()
        print(f"Network - Sent: {network_usage['bytes_sent'] / (1024 ** 2):.2f} MB, Received: {network_usage['bytes_recv'] / (1024 ** 2):.2f} MB")

        time.sleep(interval)
#endfunction

#------------------------------------------
def main ():
    """main"""
#beginfunction
    LUConst.SET_LIB(__file__)

    LULog.STARTLogging (LULog.TTypeSETUPLOG.tslINI, 'console', LUConst.GDirectoryLOG, LUConst.GFileNameLOG,
                        LUConst.GFileNameLOGjson)
    LULog.LoggerTOOLS.level = logging.INFO

    LPath = LUFile.ExtractFileDir(__file__)
    print(f'LPath: {LPath}')

    #--------------------------------------------------------------
    # 
    #--------------------------------------------------------------
    try:
        interval = int(input("Enter monitoring interval in seconds: "))
        monitor_server(interval)
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
    
    LULog.STOPLogging ()
#endfunction

#------------------------------------------
#
#------------------------------------------
#beginmodule
if __name__ == "__main__":
    main ()
# endif

# endmodule
