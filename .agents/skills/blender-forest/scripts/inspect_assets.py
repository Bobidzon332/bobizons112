import bpy, collections
print("##OBJ", len(bpy.data.objects), "COLL", len(bpy.data.collections), "MAT", len(bpy.data.materials), "IMG", len(bpy.data.images))
packed=sum(1 for i in bpy.data.images if i.packed_file); print("##IMG packed", packed, "of", len(bpy.data.images))
missing=[i.filepath for i in bpy.data.images if not i.packed_file and i.source=='FILE'][:5]; print("##IMG external sample", missing)
c=collections.Counter()
for o in bpy.data.objects:
    n=o.name.rsplit('.',1)[0]
    import re; n=re.sub(r'[_ ]?\d+$','',n); c[(n,o.type)]+=1
for k,v in sorted(c.items()): print("##NAME",k,v)
print("##ASSETS", len([o for o in bpy.data.objects if o.asset_data]), len([o for o in bpy.data.collections if o.asset_data]))
