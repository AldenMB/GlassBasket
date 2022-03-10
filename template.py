import math

bottom_length = 180
bottom_width = 140
height = 50
taper = 30
margin = 2 * height * math.tan(math.radians(taper))

length = bottom_length + margin
width = bottom_width + margin

panel_height = height / math.cos(math.radians(taper))

print_margin = 5

svg = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   width="8.5in"
   height="11in"
   viewBox="0 0 215.9 279.4"
   version="1.1"
   id="svg5"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:svg="http://www.w3.org/2000/svg">
   <rect
      style="fill:none;stroke:#000000;stroke-width:0.1"
      id="base"
      width="{bottom_width}"
      height="{bottom_length}"
      x="{215.9-print_margin-bottom_width}"
      y="{print_margin}" />
   <path
      style="fill:none;stroke:#000000;stroke-width:0.1px;stroke-opacity:1"
      d="M {print_margin},{print_margin} l {panel_height},{margin/2} v {bottom_length} l {-panel_height},{margin/2} Z"
      id="side" />
   <path
      style="fill:none;stroke:#000000;stroke-width:0.1px;stroke-opacity:1"
      d="M {215.9-print_margin},{279.4-print_margin} l {-margin/2},{-panel_height} h {-bottom_width} l {-margin/2},{panel_height} Z"
      id="end" />
</svg>
"""

with open("template.svg", "w") as f:
    f.write(svg)
