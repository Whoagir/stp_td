import pathlib
from grid import HexagonGridTypes


BASE_DIR = pathlib.Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / 'assets'


GAME_GRID_TYPE = HexagonGridTypes.pointy_top
