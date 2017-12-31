rm -rvf __pycache__
# scp -r [!.]* pi@192.168.1.28:/home/pi/weebo
rsync -av --exclude="/.*" ./ pi@192.168.1.28:/home/pi/weebo
