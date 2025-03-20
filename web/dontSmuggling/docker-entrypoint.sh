#!/bin/sh

# Get the user
user=$(ls /home)

# Check the environment variables for the flag and assign to INSERT_FLAG
# 需要注意，以下语句会将FLAG相关传递变量进行覆盖，如果需要，请注意修改相关操作
if [ "$DASFLAG" ]; then
    INSERT_FLAG="$DASFLAG"
    export DASFLAG=no_FLAG
elif [ "$FLAG" ]; then
    INSERT_FLAG="$FLAG"
    export FLAG=no_FLAG
elif [ "$GZCTF_FLAG" ]; then
    INSERT_FLAG="$GZCTF_FLAG"
    export GZCTF_FLAG=no_FLAG
else
    INSERT_FLAG="flag{TEST_Dynamic_FLAG}"
fi

# 将FLAG写入文件
echo $INSERT_FLAG | tee /app/f1ag

chmod 744 /app/f1ag

sleep 5

mitmdump --mode reverse:http://${SERVER_HOSTNAME}:${SERVER_PORT} -p 8002 -s filter.py --set block_global=false --no-http2 &


exec gunicorn --threads 8 --bind 0.0.0.0:2333 flask_autoindex.run:app

echo "Running..."

