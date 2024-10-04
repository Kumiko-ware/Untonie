bt-adapter --set Powered 0; bt-adapter --set Powered 1
bt-adapter -d | grep Name
bt-device -c "R-S202D Yamaha"
bluetoothctl connect `bt-device -i "R-S202D Yamaha"|head -1|tr "[]" "  "`
