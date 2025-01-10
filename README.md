# Mesh-Extruder-Blender-Unity-
A grid based line drawer on ground plane in Blender and a raw one for Unity, currently.
In Blender you get a quickly extruded N-Gon (will add a toggle auto a triangulate and tris to quad later).

Is it better than to do defaultly it from scratch with hotkeys? Let me know.


Blender screenshots (the toilet was an accident, don't blame me):

With show normals:
![image](https://github.com/user-attachments/assets/7d8e3fbd-27de-4878-933d-d6177df96494)

![image](https://github.com/user-attachments/assets/47a36db9-1227-4371-94f6-fdc9d402768a)

![image](https://github.com/user-attachments/assets/5a676bec-93c8-436a-8dfe-dbd212ecdcdd)

![image](https://github.com/user-attachments/assets/2152ae94-229c-4dfb-a707-31dae9172805)


N-Gon topology in the end (it is non-smooth shaded another toilet):

![image](https://github.com/user-attachments/assets/216179f3-cd2b-47ea-97d6-9fcb07305f62)

After manual steps:

Triangulate:
![image](https://github.com/user-attachments/assets/4fa38311-ebb0-4f13-809b-920a50026946)

Tris to quads 40 40:
![image](https://github.com/user-attachments/assets/837db4d1-a194-4931-a0a8-8f41f894db89)

Tris to quads 180 180:
![image](https://github.com/user-attachments/assets/a8d007e0-ac85-4276-806b-8ac11be5e253)





Using Blender 4.0.0+.
Blender version features:
1. Grid based dot placing on ground plane that automatically turn to edges
2. Merged in the end with LMB near last point or just by pressing RMB if there is at least 2 dots already
3. It automatically recalculates normals outside so your shader is not a mess.
4. Placing dots while not looking topdown or downtop is not recommended.
5. Etc?

Blender Issues:
1. You can't go less than 10 mm in a grid in Blender one, modify script self or give to AI for other improvements (Claude 3.5 is the best one?).
2. You can't use UI if not closed the shape or cancelled it by 'Escape'.
3. You can't undo lines like in Unity
4. You can't close shape, right after undo it, and then redo it. It is lost forever.

Potential Unity Issues:
1. It tries to recalculate, but the normals are still flipped in some places (?)
2. Geometry is worse than Blender one, if it was triangulated (?)
3. (Not checked) Can make redundant vertice in the same spot on closing as it was in early Blender version

The May Be Roadmap:
1. Make it a full fledge make a low-poly asset for games thing
2. Color in one click, texture draw whole separated meshes.
3. Separate meshes more easily than default solution
4. Make a solid mesh back easily
5. Proper Auto-UV making unwrapping in the process
6. All features are toggleable up to the state of classic simplest version










Extra:

You are dead after fixing AI bugs and fixing Python identations, because your VSC flickers, as is it does the Upscayl when you upscaled your image. (Updated Windows 10, fixed?)

P.S.

Should i separate Unity version so it can be installed via github link thing? Probably there is no sense in doing so with just 1 script.

Now contains 3 Branches (can a branch be installed by link?):

1. Whole thing
2. Only Blender
3. Only Unity
