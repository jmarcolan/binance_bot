docker run -p 9999:8888 -p 27017:27017 -p 2222:8080 \
    --volume=/mnt/c/bots/data/:/home/app/data/ \
    --volume=/mnt/c/bots/app/:/home/app/ \
    bot