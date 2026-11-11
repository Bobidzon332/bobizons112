import bpy, os
miss=[i.filepath for i in bpy.data.images if i.source=='FILE' and not os.path.exists(bpy.path.abspath(i.filepath))]
print("##IMAGES", len(bpy.data.images), "MISSING", len(miss), sorted(set(miss))[:8])
