import redis

class RedisManager():
    """
    Wrapper for Redis client
    """

    def __init__(self, host='localhost', port=6379, db=0) -> None:
        self.__instance = redis.Redis(
                            host=host,
                            port=port,
                            db=db
                            )

    def get_instance(self):
        return self.__instance

    def test_connection(self) -> bool:
        return self.__instance.ping()
