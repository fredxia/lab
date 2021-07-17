
NUM_DAYS=2 find /var/log/mylog*.txt -mtime +$NUM_DAYS  -exec rm -f {} +

