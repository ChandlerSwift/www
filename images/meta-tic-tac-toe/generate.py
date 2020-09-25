#!/usr/bin/env python
import argparse
import xml.dom.minidom

# Apologies; I know a lot of this is pretty hacky. It's intended as a one-time
# illustration for a blog post, so I didn't take too much time commenting it.

def drawTicTacToeGrid(TopLeft, width, depth=1, id=None, extra_tags=None) -> str:
    return_string = "<g>" if id is None else f"""<g id="{id}">"""
    if extra_tags:
        return_string += extra_tags

    # left
    return_string += f"""<line
      x1="{TopLeft[0] + 3/8 * width}"
      y1="{TopLeft[1] + 1/8 * width}"
      x2="{TopLeft[0] + 3/8 * width}"
      y2="{TopLeft[1] + 7/8 * width}"
      stroke="black" stroke-width="{max(width/100, 0.1)}px" />"""

    # right
    return_string += f"""<line
      x1="{TopLeft[0] + 5/8 * width}"
      y1="{TopLeft[1] + 1/8 * width}"
      x2="{TopLeft[0] + 5/8 * width}"
      y2="{TopLeft[1] + 7/8 * width}"
      stroke="black" stroke-width="{max(width/100, 0.1)}px" />"""

    # top
    return_string += f"""<line
      x1="{TopLeft[0] + 1/8 * width}"
      y1="{TopLeft[1] + 3/8 * width}"
      x2="{TopLeft[0] + 7/8 * width}"
      y2="{TopLeft[1] + 3/8 * width}"
      stroke="black" stroke-width="{max(width/100, 0.1)}px" />"""

    # bottom
    return_string += f"""<line
      x1="{TopLeft[0] + 1/8 * width}"
      y1="{TopLeft[1] + 5/8 * width}"
      x2="{TopLeft[0] + 7/8 * width}"
      y2="{TopLeft[1] + 5/8 * width}"
      stroke="black" stroke-width="{max(width/100, 0.1)}px" />"""

    return_string += "</g>"

    if depth > 1:
        for y in range(3):
            for x in range(3):
                return_string += drawTicTacToeGrid(
                    (
                        TopLeft[0] + (1 + 2 * x) * width / 8,
                        TopLeft[1] + (1 + 2 * y) * width / 8,
                    ),
                    width / 4,
                    depth - 1,
                )
    return return_string

# https://stackoverflow.com/a/9979169/3814663
def coords(s):
    try:
        x, y = map(int, s.split(","))
    except:
        raise argparse.ArgumentTypeError("Coordinates must be x,y")
    if x not in range(3) or y not in range(3):
        raise argparse.ArgumentError("Invalid coord, must be 0, 1, or 2")
    return x, y

# parse args
parser = argparse.ArgumentParser()
parser.add_argument(
    "coords",
    metavar="C",
    help="coordinates w,x y,z ..., starting at the topmost grid",
    type=coords,
    nargs="+",
)
parser.add_argument('--animate_limit', '-l', help='only perform the first n animations, but highlight the remaining cells')
args = parser.parse_args()
coords = args.coords
animate_limit = int(args.animate_limit)

# Begin SVG
svg = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns:svg="http://www.w3.org/2000/svg"
     xmlns="http://www.w3.org/2000/svg"
     width="200mm"
     height="200mm"
     viewBox="0 0 100 100"
     version="1.1">"""

def get_animateTransform_values(coords):
    values = [(0, 0)]
    for i, c in enumerate(coords[:-1]):
        prev_x = values[-1][0] * 4 + (1 + 2 * c[0]) * -50/4**i
        prev_y = values[-1][1] * 4 + (1 + 2 * c[1]) * -50/4**i
        values.append((prev_x, prev_y))
    return "".join([f"{x},{y}; {x},{y}; " for x, y in values]) + "0,0"

def get_animateTransform_keyTimes(coords):
    times = []
    for i in range(len(coords)):
        times += [i/len(coords), (i+3/4)/len(coords)]
    times += [1] # end
    return "; ".join(map(str,times))

if animate_limit:
    anim_coords = coords[:animate_limit+1] # set this to a subset of coords to only do one animation
else:
    anim_coords = coords

# draw and animate boxes
animation = f"""
<animateTransform
    attributeName="transform"
    type="translate"
    dur="{2 * len(anim_coords)}s"
    values="{get_animateTransform_values(anim_coords)}"
    keyTimes="{get_animateTransform_keyTimes(anim_coords)}"
    repeatCount="indefinite"/>
<animateTransform
    attributeName="transform"
    type="scale"
    additive="sum"
    dur="{2 * len(anim_coords)}s"
    values="{"".join([f"{4**i};{4**i}; " for i in range(len(anim_coords))])}1"
    keyTimes="{get_animateTransform_keyTimes(anim_coords)}"
    repeatCount="indefinite"/>
<rect
    x="{(1 + 2 * coords[0][0]) * 50/4**1 + (1 + 2 * coords[1][0]) * 50/4**2 + 1 * 50/4**3}"
    y="{(1 + 2 * coords[0][1]) * 50/4**1 + (1 + 2 * coords[1][1]) * 50/4**2 + 1 * 50/4**3}"
    width="4.6875"
    height="4.6875"
    fill="yellow"
    opacity="0.5" />
<rect
    x="{(1 + 2 * coords[0][0]) * 50/4**1 + (1 + 2 * coords[1][0]) * 50/4**2 + (1 + 2 * coords[2][0]) * 50/4**3 + 1 * 50/4**4}"
    y="{(1 + 2 * coords[0][1]) * 50/4**1 + (1 + 2 * coords[1][1]) * 50/4**2 + (1 + 2 * coords[2][1]) * 50/4**3 + 1 * 50/4**4}"
    width="1.171875"
    height="1.171875"
    fill="red"
    opacity="0.5" />
    """

x_offset = (1 + 2 * coords[0][0]) * 12.5
y_offset = (1 + 2 * coords[0][1]) * 12.5

svg += drawTicTacToeGrid(
    (x_offset, y_offset), 25, id="overlay-grid", extra_tags=animation
)

# draw main grid
# this happens after the overlay because we want this to appear on top, and the
# SVG spec says z-index is based on order presented
# change 3 to 4 for extra nerd cred
svg += drawTicTacToeGrid((0, 0), 100, len(coords))

# close tags
svg += "</svg>"

# Clean up and print the svg
dom = xml.dom.minidom.parseString(svg)
print(dom.toxml())
# for pretty printing, do this instead:
# print(dom.toprettyxml())
