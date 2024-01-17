class Config:
    host = '127.0.0.1'
    port = 5555

    @staticmethod
    def getHost():
        return Config.host

    @staticmethod
    def getPort():
        return Config.port
