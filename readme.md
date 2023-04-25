## First to create a account and get coins info
python create_account.py 

## Create bot and keep alive
python create_bot.py 

##


.open /home/app/data/bot.db
select * from Bot_tran;
delete from Bot_tran where ts_id = 3;
 update Bot_tran set sell_status = "WAIT" where ts_id == 3;

https://ilegra.com/blog/organizando-o-palco-instalando-e-configurando-o-airflow-localmente/

delete from Bot_info where bot_id = 2;
oi mundo e agora

pip install -e .
pip install -e app/binance_bot/

python3 -m pip install --upgrade build

python3 -m build

python /home/app/binance_bot/test/test_1.py



docker run -p 9999:8888 -p 27017:27017 -p 2222:8080 --volume=/mnt/c/bots/data/:/home/app/data/ --volume=/mnt/c/bots/binance_bot/:/home/app/binance_bot/ bot bash