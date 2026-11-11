import bpy
print("##FILE", bpy.data.filepath)
print("##TEXTS", [(t.name, len(t.as_string())) for t in bpy.data.texts])
drv=[]
for coll in (bpy.data.objects,bpy.data.materials,bpy.data.node_groups,bpy.data.scenes,bpy.data.worlds,bpy.data.meshes,bpy.data.shape_keys,bpy.data.cameras,bpy.data.lights,bpy.data.armatures):
    for d in coll:
        ad=getattr(d,'animation_data',None)
        if ad:
            for f in ad.drivers:
                if f.driver.type=='SCRIPTED': drv.append((d.name,f.data_path,f.driver.expression[:80]))
        nt=getattr(d,'node_tree',None)
        if nt:
            for n in nt.nodes:
                if n.bl_idname=='ShaderNodeScript': drv.append((d.name,'OSL script node',n.name))
print("##SCRIPTED_DRIVERS", len(drv), drv[:10])
print("##ADDONS_IN_FILE n/a; libraries:", [l.filepath for l in bpy.data.libraries])
print("##OBJ", len(bpy.data.objects), "MESHES", len(bpy.data.meshes))
