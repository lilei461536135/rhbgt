#! /usr/bin/python
# -*- coding: utf-8 -*-
import subprocess
import os
import time

def printf(str):
    #print str
    pass
    
    
# check specpower status, return process id or -1
def check_app_status():
    cmd = "ps -ef | grep -i java | grep -v grep"
    printf("Executing %s" % cmd)
    pid = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = pid.communicate()
    printf("Returned output: %s" % out.decode())
    printf("Returned error: %s" % err.decode())
    printf("searching SpecPowerSsj from output")
    if out.decode().find('SpecPowerSsj') >= 0:
        printf("SpecPowerSsj has been found")
        for line in out.decode().split(os.linesep):
            if line.find('SpecPowerSsj') >= 0:
                process_id = line.strip().split()[2]
                printf("process id is %s" % process_id)
                return process_id
    else:
        printf("SpecPowerSsj has not been found")
        return -1
        
     
def set_as_manual():
    # set fan control mode as manual
    printf("set fan control mode as manual")
    cmd = "ipmitool raw 0x3a 0xa5 0x01"
    try:
        pid = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        pid.wait()
    except Exception as e:
        printf("set fan control mode as manual failed")
        printf(e)
        return False 
        
        
def set_as_auto():
    # set fan control mode as auto
    printf("set fan control mode as auto")
    cmd = "ipmitool raw 0x3a 0xa5 0x00"
    try:
        pid = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        pid.wait()
    except Exception as e:
        printf("set fan control mode as auto failed")
        printf(e)
        return False
        
        
def set_fan_speed(value):
    try:
        # set fan speed
        printf("set fan speed to %s" % value)
        cmd = "ipmitool raw 0x3a 0xa0 0 %s" % value
        pid = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = pid.communicate()
        printf("Returned output: %s" % out.decode())
        printf("Returned error: %s" % err.decode())
        cmd = "ipmitool raw 0x3a 0xa0 1 %s" % value
        pid = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = pid.communicate()
        printf("Returned output: %s" % out.decode())
        printf("Returned error: %s" % err.decode())
        cmd = "ipmitool raw 0x3a 0xa0 2 %s" % value
        pid = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = pid.communicate()
        printf("Returned output: %s" % out.decode())
        printf("Returned error: %s" % err.decode())
        cmd = "ipmitool raw 0x3a 0xa0 3 %s" % value
        pid = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = pid.communicate()
        printf("Returned output: %s" % out.decode())
        printf("Returned error: %s" % err.decode())
    except Exception as e:
        printf("set fan speed failed")
        printf(e)
        sys.exit(-1)
        
if __name__ == "__main__":
    beg_trace_flag = 0
    start_time = 0
    app_status_old = 's'  # init status: stopped
    while True:
        pid0 = check_app_status()
        if pid0 != -1:  # app is running
            app_status_new = 'r'
        else:  # app is stopped
            app_status_new = 's'
        if app_status_old == 's' and app_status_new == 's':
            app_status = 's'
        elif app_status_old == 's' and app_status_new == 'r':
            app_status = 's2r'
        elif app_status_old == 'r' and app_status_new == 'r':
            app_status = 'r'
        elif app_status_old == 'r' and app_status_new == 's':
            app_status = 'r2s'
        app_status_old = app_status_new  # update app_status_old value
        
        # deal with all situations 
        if app_status == 's2r':
            beg_trace_flag = 1
            start_time = time.time()
        elif app_status == 's':
            beg_trace_flag = 0
            start_time = 0
        elif app_status == 'r2s':
            set_as_auto()
        elif app_status == 'r' and beg_trace_flag == 1:
            duration = time.time() - start_time
            if int(duration) >= 1240:
                set_as_manual()
                set_fan_speed('20')
                beg_trace_flag = 0
        else:
            pass
        time.sleep(5)
