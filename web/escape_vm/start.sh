#! /bin/sh

if [ "$GZCTF_FLAG" ]
then
  INSERT_FLAG="$GZCTF_FLAG"
  export GZCTF_FLAG=no_flag
  GZCTF_FLAG=no_flag
fi

npm start