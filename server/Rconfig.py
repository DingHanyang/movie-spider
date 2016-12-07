import configparser

class Cf():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("../config.ini")


# if __name__ == '__main__':
#     cf=Cf()
#     print(cf.config.get("db","port"))
