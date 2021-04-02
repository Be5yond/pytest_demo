import pathlib
import configparser
HOME = pathlib.Path(__file__).absolute().parent.parent
config = configparser.ConfigParser()
config.read(HOME/'config.ini')

