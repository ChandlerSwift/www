#!/usr/bin/env python
import argparse
import xml.dom.minidom

# Apologies; I know a lot of this is pretty hacky. It's intended as a one-time
# illustration for a blog post, so I didn't take too much time commenting it.


def drawTicTacToeGrid(TopLeft, width, depth=1, id=None) -> str:
    return_string = "<g>" if id is None else f"""<g id="{id}">"""

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
parser.add_argument(
    "--animate_limit",
    "-l",
    help="only perform the first n animations, but highlight the remaining cells",
)
parser.add_argument(
    "--no-animate",
    "-n",
    action="store_true",
    help="just render the static (highlighted) grid",
)
args = parser.parse_args()
coords = args.coords
animate_limit = args.animate_limit
animate = not args.no_animate

# Begin SVG
svg = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns:svg="http://www.w3.org/2000/svg"
     xmlns="http://www.w3.org/2000/svg"
     width="200mm"
     height="200mm"
     viewBox="0 0 100 100"
     version="1.1">
     """


def get_animateTransform_values(coords):
    values = [(0, 0)]
    for i, c in enumerate(coords[:-1]):
        prev_x = values[-1][0] * 4 + (1 + 2 * c[0]) * -50
        prev_y = values[-1][1] * 4 + (1 + 2 * c[1]) * -50
        values.append((prev_x, prev_y))
    return (
        "".join([f"{x},{y}; {x},{y}; " for x, y in values])
        + f"{values[-1][0]},{values[-1][1]}"
    )


def get_animateTransform_keyTimes(coords):
    times = []
    for i in range(len(coords)):
        times += [i / len(coords), (i + 3 / 4) / len(coords)]
    times += [1]
    return "; ".join(map(str, times))


if animate_limit:
    anim_coords = coords[
        : int(animate_limit) + 1
    ]  # set this to a subset of coords to only do one animation
else:
    anim_coords = coords

svg += "<g>"
# animate boxes
if animate:
    svg += f"""
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
        values="{"".join([f"{4**i};{4**i}; " for i in range(len(anim_coords))])}{4**(len(anim_coords)-1)}"
        keyTimes="{get_animateTransform_keyTimes(anim_coords)}"
        repeatCount="indefinite"/>
        """
# draw boxes
colors = [
    "LightGoldenRodYellow",
    "LightPink",
    "LightGreen",
    "LightBlue",
    "LightSalmon",
    "LightSeaGreen",
]  # chosen arbitrarily
for i, coord in enumerate(coords[1:]):
    svg += f"""
    <rect
        x="{sum([(1 + 2 * coords[j][0]) * 50/4**(j+1) for j in range(i+2)] + [50/4**(i+3)])}"
        y="{sum([(1 + 2 * coords[j][1]) * 50/4**(j+1) for j in range(i+2)] + [50/4**(i+3)])}"
        width="{75/4**(i+2)}"
        height="{75/4**(i+2)}"
        fill="{colors[i]}" />
    """
svg += "</g>"


def get_transform_values(coords, transition_number):
    c = coords[transition_number-1]
    x = (1 + 2 * c[0]) * -50
    y = (1 + 2 * c[1]) * -50
    num_transitions = 2 * len(coords) + 1
    return "".join(["0,0; "] * (2 * transition_number) + [f"{x},{y}; "] * (num_transitions - (2 * transition_number)))


def get_scale_values(coords, transition_number):
    num_transitions = 2 * len(coords) + 1
    return "".join(["1;"] * (2 * transition_number) + [f"4;"] * (num_transitions - (2 * transition_number)))


# draw expanding grids with the boxes
if animate:
    for i, coord in enumerate(anim_coords[:-1]):
        svg += f"""<g>
        <animateTransform
            attributeName="transform"
            type="translate"
            dur="{2 * len(anim_coords)}s"
            values="{get_transform_values(anim_coords, i+1)}"
            keyTimes="{get_animateTransform_keyTimes(anim_coords)}"
            repeatCount="indefinite"/>
        <animateTransform
            attributeName="transform"
            type="scale"
            additive="sum"
            dur="{2 * len(anim_coords)}s"
            values="{get_scale_values(anim_coords, i+1)}"
            keyTimes="{get_animateTransform_keyTimes(anim_coords)}"
            repeatCount="indefinite"/>
            """
        x_offset = (1 + 2 * coord[0]) * 12.5
        y_offset = (1 + 2 * coord[1]) * 12.5
        svg += drawTicTacToeGrid((x_offset, y_offset), 25)
        svg += "</g>"

# draw main grid over the top
# this happens after the overlay because we want this to appear on top, and the
# SVG spec says z-index is based on order presented
svg += drawTicTacToeGrid((0, 0), 100, len(coords))

# close tags
svg += "</svg>"

# Clean up and print the svg
dom = xml.dom.minidom.parseString(svg)
print(dom.toxml())
# for pretty printing, do this instead:
# print(dom.toprettyxml())
