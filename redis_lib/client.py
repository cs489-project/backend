from redis import Redis

# TODO: weird error, can't be imported if it's inside a folder
redis_client: Redis = Redis(host='redis', port=6379, db=0)
