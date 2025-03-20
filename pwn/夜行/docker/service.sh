#!/bin/sh
# Add your startup script

# DO NOT DELETE
echo $GZCTF_FLAG >/flag

/etc/init.d/xinetd start
sleep infinity
