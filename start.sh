# docker run -p 9999:8888 -p 27017:27017 -p 2222:8080 \
#     --volume=/mnt/c/bots/data/:/home/app/data/ \
#     --volume=/mnt/c/bots/binance_bot/:/home/app/binance_bot/ \
#     bot bash

sudo docker run -ti  -p 9999:8888 -p 27017:27017 -p 2222:8080 \
    --volume=/home/jmarcolan/app/data/:/home/app/data/ \
    --volume=/media/sf_bots/binance_bot/:/home/app/binance_bot/ \
    bot bash