"""
Week 1 practice project template for Python Data Visualization
Load a county-level PNG map of the USA and draw it using matplotlib
"""

import matplotlib.pyplot as plt

# Houston location

USA_SVG_SIZE = [555, 352]

HOUSTON_POS = [302, 280]
def draw_USA_map(map_name):
    """
    Given the name of a PNG map of the USA (specified as a string),
    draw this map using matplotlib
    """
     
    # Load map image, note that using 'rb'option in open() is critical since png files are binary
    usa_map=open(map_name,"rb")

    #  Get dimensions of USA map image
    dimensions_map=plt.imread(usa_map)
    print(type(dimensions_map))
    ypixels, xpixels, bands = dimensions_map.shape
    print(bands)
    # Plot USA map
    usa_map_img=plt.imshow(dimensions_map)
    #plt.show(usa_map_img)
    # Plot green scatter point in center of map
    plt.scatter(x = xpixels / 2, y = ypixels / 2, s = 50, c = "Green")
    plt.scatter(x = HOUSTON_POS[0] * xpixels / USA_SVG_SIZE[0], y = HOUSTON_POS[1] * ypixels / USA_SVG_SIZE[1], s = 50, c = "Red") 

    # Plot red scatter point on Houston, Tx - include code that rescale coordinates for larger PNG files
    plt.show(usa_map_img)
    pass

#draw_USA_map("USA_Counties_555x352.png")
draw_USA_map("USA_Counties_1000x634.png")   
