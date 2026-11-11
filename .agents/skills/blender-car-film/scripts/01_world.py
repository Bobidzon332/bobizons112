import bpy, os, math
A = os.path.expanduser("~/blender-car-film/assets/ph")
# fresh scene
for o in list(bpy.data.objects): bpy.data.objects.remove(o)
for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.images, bpy.data.worlds, bpy.data.lights, bpy.data.cameras):
    for x in list(coll): coll.remove(x)
for c in list(bpy.data.collections): bpy.data.collections.remove(c)
sc = bpy.context.scene
sc.render.fps = 24; sc.frame_start = 1; sc.frame_end = 480
sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Medium High Contrast"
sc.render.engine = "BLENDER_EEVEE"
sc.eevee.use_shadows = True
sc.render.use_motion_blur = True

def col(name):
    c = bpy.data.collections.get(name) or bpy.data.collections.new(name)
    if c.name not in sc.collection.children: sc.collection.children.link(c)
    return c

def pbr(name, tex, scale=1.0, tint=None, rough_mul=1.0, disp=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    d = os.path.join(A, "tex", tex); fs = os.listdir(d)
    f = lambda k: os.path.join(d, next(x for x in fs if k in x))
    tc = nt.nodes.new("ShaderNodeTexCoord"); mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (scale, scale, scale)
    nt.links.new(tc.outputs["UV"], mp.inputs["Vector"])
    def img(k, nc=False):
        n = nt.nodes.new("ShaderNodeTexImage"); n.image = bpy.data.images.load(f(k))
        if nc: n.image.colorspace_settings.name = "Non-Color"
        nt.links.new(mp.outputs["Vector"], n.inputs["Vector"]); return n
    di = img("diff")
    if tint:
        mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = "RGBA"; mx.blend_type = "MULTIPLY"
        mx.inputs["Factor"].default_value = 1; mx.inputs[7].default_value = (*tint, 1)
        nt.links.new(di.outputs["Color"], mx.inputs[6]); nt.links.new(mx.outputs[2], b.inputs["Base Color"])
    else: nt.links.new(di.outputs["Color"], b.inputs["Base Color"])
    r = img("rough", True)
    mr = nt.nodes.new("ShaderNodeMath"); mr.operation = "MULTIPLY"; mr.inputs[1].default_value = rough_mul
    nt.links.new(r.outputs["Color"], mr.inputs[0]); nt.links.new(mr.outputs[0], b.inputs["Roughness"])
    nm = nt.nodes.new("ShaderNodeNormalMap"); nt.links.new(img("nor_gl", True).outputs["Color"], nm.inputs["Color"])
    nt.links.new(nm.outputs["Normal"], b.inputs["Normal"])
    if disp and any("disp" in x for x in fs):
        dn = nt.nodes.new("ShaderNodeDisplacement"); dn.inputs["Scale"].default_value = disp
        nt.links.new(img("disp", True).outputs["Color"], dn.inputs["Height"])
        nt.links.new(dn.outputs[0], nt.nodes["Material Output"].inputs["Displacement"])
        m.displacement_method = "BOTH"
    return m

# world: moonlit HDRI, very dim, cold
w = bpy.data.worlds.new("Night"); sc.world = w; w.use_nodes = True
nt = w.node_tree; bg = nt.nodes["Background"]
env = nt.nodes.new("ShaderNodeTexEnvironment")
env.image = bpy.data.images.load(os.path.join(A, "hdri", os.listdir(os.path.join(A, "hdri"))[0]))
nt.links.new(env.outputs["Color"], bg.inputs["Color"]); bg.inputs["Strength"].default_value = 0.12

# ground: road strip along +Y (y -40..190), snow either side
g = col("Ground")
def plane(name, sx, sy, loc, mat):
    bpy.ops.mesh.primitive_plane_add(size=1, location=loc)
    o = bpy.context.object; o.name = name; o.scale = (sx, sy, 1)
    bpy.ops.object.transform_apply(scale=True)
    bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.subdivide(number_cuts=40)
    bpy.ops.uv.cube_project(cube_size=1.0); bpy.ops.object.mode_set(mode="OBJECT")
    o.data.materials.append(mat)
    for c in o.users_collection: c.objects.unlink(o)
    g.objects.link(o); return o
road = plane("Road", 7.0, 240, (0, 75, 0), pbr("RoadSnow", "asphalt_snow", 0.25, rough_mul=0.8, disp=0.03))
for s in (-1, 1):
    plane(f"Snow_{'L' if s<0 else 'R'}", 80, 240, (s * 43.5, 75, 0.04), pbr(f"Snow{s}", "snow_02", 0.2, tint=(0.92, 0.95, 1.0), disp=0.15))
# low snow bank at road edges
for s in (-1, 1):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=240, location=(s * 3.7, 75, -0.25), rotation=(math.pi/2, 0, 0))
    o = bpy.context.object; o.name = f"SnowBank{s}"; o.scale = (1.4, 1, 1)
    o.data.materials.append(bpy.data.materials["Snow1"])
    for c in o.users_collection: c.objects.unlink(o)
    g.objects.link(o)
print("world ok")
