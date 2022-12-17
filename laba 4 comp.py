
from PIL import Image, ImageDraw
import random
from queue import Queue

def adjacent(p):
    x = p[0]
    y = p[1]

    return (
        (x+1, y),
        (x-1, y),
        (x, y+1),
        (x, y-1)
    )

def find1(el: tuple[int, int], s: set) -> set:

    q = Queue()
    visited = set()

    visited.add(el)
    q.put(el)
    s.remove(el)

    while not q.empty():
        pixel = q.get()

        for adj_pixel in adjacent(pixel):
            if adj_pixel in s and adj_pixel not in visited:
                s.remove(adj_pixel)
                visited.add(adj_pixel)
                q.put(adj_pixel)

    return visited

def avg(s: set) -> tuple:

    return (
        int(sum(map(lambda a: a[0], s)) / len(s)),
        int(sum(map(lambda a: a[1], s)) / len(s)),
    )


def find2(s: set) -> list:
    results = list()
    while s:
        random_element = list(s)[0]
        results.append(find1(random_element, s))
        
    return list(map(avg, results))

def distance(a, b):
    i = a[0] - b[0]
    i = i * i

    j = a[1] - b[1]
    j = j * j
    return i + j


def diagram(p: dict) -> Image:
    w, h = 960, 540
    img = Image.new('RGB', (w, h))

    for x in range(w):
        for y in range(h):

            point = min(p.keys(), key=lambda a: distance(a, (x, y)))

            img.putpixel((x, y), p[point])

    return img

def random_colors(p: set) -> dict:
    a = dict()
    for i in p:
        a[i] = (
            random.randrange(0, 256),
            random.randrange(0, 256),
            random.randrange(0, 256)
        )

    return a


f = open('DS3.txt', 'r')
dataset = [(int(x), int(y)) for x, y in map(str.split, f.readlines())]
f.close()

points = find2(set(dataset))
color_dict = random_colors(points)
img = diagram(color_dict)

for p in dataset:
    color = img.getpixel(p)
    new_color = tuple(map(lambda x: int(x * 0.9), color))
    img.putpixel(p, new_color)

image_draw = ImageDraw.Draw(img)

for p in points:
    i, j = p
    image_draw.ellipse((i - 2.5, j - 2.5, i + 2.5, j + 2.5), '#ffffff')


img.save('screenshot.png')


