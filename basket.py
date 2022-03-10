import cadquery as cq
import math

bottom_length = 180
bottom_width = 140
height = 50
taper = 30
margin = 2 * height * math.tan(math.radians(taper))

length = bottom_length + margin
width = bottom_width + margin
glass_thickness = 4
corner_radius = 20
fillet = 2

prism = cq.Workplane().rect(width, length).extrude(-height, taper=taper)

shell = prism.faces(">Z").shell(3 * glass_thickness)


def face2pane(face):
    return (
        face.wires()
        .tag("face")
        .toPending()
        .workplane()
        .extrude(2 * glass_thickness, combine=False)
        .wires(tag="face")
        .toPending()
        .workplane()
        .cutBlind(glass_thickness)
    )


panes = {side: face2pane(prism.faces(side)) for side in ">X <X >Y <Y <Z".split()}

corners = (
    prism.vertices().sphere(corner_radius).intersect(shell).faces(">Z").fillet(fillet)
)

for name, pane in panes.items():
    corners = corners.cut(pane)

# save corners as stl
one_corner = (
    cq.Workplane()
    .box(width, length, 2 * height, centered=False)
    .translate([0, 0, -height * 1.5])
    .intersect(corners)
    .faces(">Z")
    .workplane(-height / 2)
)
upper_corner = one_corner.split(keepTop=True)
lower_corner = one_corner.split(keepBottom=True)
cq.exporters.export(upper_corner.mirror(), "upper_corner.stl")
cq.exporters.export(lower_corner, "lower_corner.stl")


# show a preview in CQgui
if __name__ == "temp":
    show_object(corners, name="corners")
    for name, pane in panes.items():
        show_object(
            pane, options={"alpha": 0.5, "color": "light blue"}, name=f"pane {name}"
        )
