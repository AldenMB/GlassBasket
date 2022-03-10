import cadquery as cq
from template import length, width, height, taper

glass_thickness = 2.25
base_thickness = 3.2
corner_radius = 20
fillet = glass_thickness

prism = cq.Workplane().rect(width, length).extrude(-height, taper=taper)

shell = (
    prism.faces(">Z")
    .shell(3 * glass_thickness, kind="intersection")
    .faces("<Z")
    .wires()
    .toPending()
    .extrude(-3 * (base_thickness - glass_thickness), taper=taper)
    .fillet(fillet)
)


def face2pane(face, thickness=glass_thickness):
    return (
        face.wires()
        .tag("face")
        .toPending()
        .workplane()
        .extrude(2 * thickness, combine=False)
        .wires(tag="face")
        .toPending()
        .workplane()
        .cutBlind(thickness)
    )


panes = {side: face2pane(prism.faces(side)) for side in ">X <X >Y <Y".split()}
panes["<Z"] = face2pane(prism.faces("<Z"), thickness=base_thickness)

corners = prism.vertices().sphere(corner_radius, combine=False).intersect(shell)

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
