ssh HGCAL_dev@HGCALZCU102BE
# password: daq5HGCAL!
#################################

# If you log in for the first time you need to run:
# Sets the clock for the MGT (multi gigabit transiver from the fpga)
python3 sw/my_little_320.py
# Loads the firmware
sudo fw-loader Slow_Control # /opt/cms-hgcal-firmware/hgc-test-system/Slow_Control

# Martim's forlder
cd ipbus-software
python3 testSlowControl.py
# If not 40 MHz then repeat procedure upt to here, if still doesn't work hard reset the board.

# In the SlowControl.py the first 5 transactions (out of 9) configure the lpgbt: ec port and sets the lpgbt in ready state.

### Check rsync (shell command through ssh)
