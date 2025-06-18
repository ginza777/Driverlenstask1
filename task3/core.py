from typing import List, Tuple
from shapely.geometry import Polygon
import logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='[%(asctime)s] ACTION: %(message)s'
)


def check_polygon_collision(polygon1: List[Tuple[float, float]], polygon2: List[Tuple[float, float]]) -> bool:
    poly1 = Polygon(polygon1)
    poly2 = Polygon(polygon2)
    logging.info(f"Checking collision between polygons: {polygon1} and {polygon2}")
    if not poly1.is_valid or not poly2.is_valid:
        logging.error("One or both polygons are invalid.")
        return False
    return poly1.intersects(poly2) or poly1.contains(poly2) or poly2.contains(poly1)


# Примеры использования
polygon1 = [(0, 0), (4, 0), (4, 4), (0, 4)]
polygon2 = [(2, 2), (6, 2), (6, 6), (2, 6)]
polygon3 = [(5, 5), (7, 5), (7, 7), (5, 7)]

print(check_polygon_collision(polygon1, polygon2))
print(check_polygon_collision(polygon1, polygon3))


# To'qnashuvchi poligonlar (qisman kesishish)
polygon4 = [(3, 3), (5, 3), (5, 5), (3, 5)]

# To'liq bir poligon ichida boshqa poligon (ichki qamrab olish)
polygon5 = [(1, 1), (3, 1), (3, 3), (1, 3)]

# To'qnashmaydigan, to'liq tashqarida poligonlar
polygon6 = [(10, 10), (12, 10), (12, 12), (10, 12)]

# Chekka teguvchi poligonlar (bir nuqta bo'yicha yoki chegara bo'yicha)
polygon7 = [(4, 0), (8, 0), (8, 4), (4, 4)]

print(check_polygon_collision(polygon1, polygon4))  # True, qisman kesishadi
print(check_polygon_collision(polygon1, polygon5))  # True, polygon1 ichida polygon5 bor
print(check_polygon_collision(polygon1, polygon6))  # False, butunlay tashqarida
print(check_polygon_collision(polygon1, polygon7))  # True, chegara bo'yicha tegishish