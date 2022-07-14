#!/bin/bash
NAME=$(( RANDOM % 1000 ))
POST_STATUS=`curl -i -X POST -d "name=${NAME}&email=email@test.com&content=Testing API" http://127.0.0.1:5000/api/timeline_post -o /dev/null -w '%{http_code}\n' -s`
if [ $POST_STATUS == 200 ]
then 
    DELETE_STATUS=`curl -i -X DELETE -d "name=${NAME}" http://127.0.0.1:5000/api/timeline_post -o /dev/null -w '%{http_code}\n' -s`
    if [ $DELETE_STATUS == 200 ]
    then 
        echo "PASS"
    else
        echo "FAIL"
    fi
else
    echo "FAIL"
fi