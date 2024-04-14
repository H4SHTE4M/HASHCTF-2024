#! /bin/sh

if [ "$GZCTF_FLAG" ]
then
  export GZCTF_FLAG=no_flag
  GZCTF_FLAG=no_flag
fi

cd /app && flask run -h 0.0.0.0 -p 5000