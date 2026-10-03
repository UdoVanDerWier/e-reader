import math

import pymupdf

SCALE=2
# eignelijk dus wel 7.25 inch display
# Display settings
TARGET_WIDTH = 480
TARGET_HEIGHT = 800

doc = pymupdf.open("./Donald_Duck-1952-01.epub")
matrix = pymupdf.Matrix(SCALE, SCALE)

def ImageQuantisizing(r, g, b, q_val) :
    return (r >> q_val) << q_val, (g >> q_val) << q_val, (b >> q_val) << q_val


for page in doc : 
    rect = page.rect
    zoom_x = TARGET_WIDTH / rect.width
    zoom_y = TARGET_HEIGHT / rect.height
    matrix = pymupdf.Matrix(zoom_x, zoom_y)

    pixmap = page.get_pixmap(matrix=matrix)

    for pixel_x in range(0, pixmap.width) : 
        error = 0
        for pixel_y in range(0, pixmap.height): 
            rgb = pixmap.pixel(pixel_x, pixel_y)[:3]
            r, g, b = ImageQuantisizing(rgb[0], rgb[1], rgb[2], 6)
            
            pixel = math.floor((r + g + b) / 3)
            pixmap.set_pixel(pixel_x, pixel_y, (pixel, pixel, pixel))

    pixmap.save(f"page-{page.number}-gray.png")