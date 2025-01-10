# Mesh-Extruder-Blender-Unity-
A grid based outline drawer *on ground plane in Blender* and a *raw one in 2D Window* for Unity.
-

In Blender you get a quickly extruded N-Gon (will add a toggle auto a triangulate and tris to quad later).

Is it better than to do defaultly it from scratch with hotkeys? Let me know.


Blender install instructions:
-
1. Download the zip
2. Open Blender - Edit - Preferences - Addons - Click the \/ (its upper right) - Install from disk - Select Blender Mesh Extruder.zip - Install from disk button
3. Press N or arrow to open default Sidebar (on right) - click Tool - it is below "Workspace" if no other addons.

Blender main how to use:
-
1. Press Z or -Z on your axis or hotkey Numpad 7
2. Press Draw Shape
3. Start placing dots that will connect sequentially.
4. When done close shape on first point or with RMB
5. Be careful with default Blender undo system, as if you mixed action in it, it can't redo.


Unity how to use:
-
1. Put the script anywhere in assets folder
2. Look upper - Tools - Simple Mesh Extruder
3. No grid, draw by hand, decrease your mouse DPI to 200 to achieve "mirrored" effect if needed.
4. RMB undo last line (it can't redo it back)
5. Close the and generate the shape by pressing first point or generate button

Blender screenshots (the toilet was an accident, don't blame me):
-

With show normals:
-
![image](https://github.com/user-attachments/assets/7d8e3fbd-27de-4878-933d-d6177df96494)

![image](https://github.com/user-attachments/assets/47a36db9-1227-4371-94f6-fdc9d402768a)

![image](https://github.com/user-attachments/assets/5a676bec-93c8-436a-8dfe-dbd212ecdcdd)

![image](https://github.com/user-attachments/assets/2152ae94-229c-4dfb-a707-31dae9172805)


N-Gon topology in the end (it is non-smooth shaded another toilet):
-
![image](https://github.com/user-attachments/assets/216179f3-cd2b-47ea-97d6-9fcb07305f62)

After manual steps:
-

Triangulate:
-
![image](https://github.com/user-attachments/assets/4fa38311-ebb0-4f13-809b-920a50026946)

Tris to quads 40 40:
-
![image](https://github.com/user-attachments/assets/837db4d1-a194-4931-a0a8-8f41f894db89)

Tris to quads 180 180:
-
![image](https://github.com/user-attachments/assets/a8d007e0-ac85-4276-806b-8ac11be5e253)

-
-

Unity version screenshot that pretty much covers its current state:
-

![image](https://github.com/user-attachments/assets/dd4ba2c3-4421-4d66-a031-aa04d5dc2d61)

More recent screenshot of same version:
-
![image](https://github.com/user-attachments/assets/d825bb8d-eb41-48eb-908a-199a8ef31fa7)

The "normal" problem:
-
![image](https://github.com/user-attachments/assets/53a15831-030a-4046-a581-f17b9f23eb88)





Using Blender 4.0.0+

Blender version features:
-
1. Grid based dot placing on ground plane that automatically turn to edges
2. Merged in the end with LMB near last point or just by pressing RMB if there is at least 2 dots already
3. It automatically recalculates normals outside so your shader is not a mess.
4. Placing dots while not looking topdown or downtop is not recommended.
5. Etc?

Blender Issues:
-
1. You can't go less than 10 mm in grid snap (You can just disable grid if outlining reference), modify script self or give to AI for other improvements (Claude 3.5 is the best one?).
2. Extrusion can't be below 10 mm as is the grid.
3. You can't use UI if not closed the shape or cancelled it by 'Escape'.
4. You can't undo lines like in Unity (and redo too)

-
-

Potential Unity Issues:
-
1. Yes, normals are madly flipped, especially in sharp meshes.
2. Geometry is worse than Blender one, if it was triangulated (?)
3. (Not checked) Can make redundant vertice in the same spot on closing as it was in early Blender version
4. Will conflict with same name script, cause doesn't have a namespace.

-
-

The May Be Roadmap:
-
1. Make a toggleable mirror modifier while making shape or show a preview outline before generating it with mirror modifier
2. Make it a full fledge make a low-poly asset for games thing
3. Color in one click, texture draw whole separated meshes.
4. Separate meshes more easily than default solution
5. Make a solid mesh back easily
6. Proper Auto-UV making unwrapping in the process
7. All features are toggleable up to the state of classic simplest version

-
-
-

Thoughts (This Last section is useless):
-
Probably the Unity one will be deprecated, as Unity doesn't have enough saturated libraries to manipulate meshes.
Or it will await when Blender one will be finished, to ask AI chat to remake (with many prompts) it for Unity, like it was with Blender one










Extra:

You are dead after fixing AI bugs and fixing Python identations, because your VSC flickers, as is it does the Upscayl when you upscaled your image. (Updated Windows 10, it fixed)

P.S.

Should i separate Unity version so it can be installed via github link thing? Probably there is no sense in doing so with just 1 script.
-
Now contains 3 Branches (can a branch be installed by link?):
-
1. Whole thing
2. Only Blender
3. Only Unity
