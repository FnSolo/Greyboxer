# 2D to 3D Shape Drawer
Grid based 2D Outline Drawer *on ground plane in Blender* and a *raw one in 2D Window* for Unity.
-

In Blender you get a quickly extruded N-Gon (will add a toggleable triangulate + tris to quads, mirror later).

Is it better than to do defaultly it from scratch with hotkeys? Let me know.


Blender install instructions:
-
1. Download the zip *(On the right press '+' to see other releases and press it then press "source.zip" to download the project, unzip project folder = same list as on GitHub)*
2. Open Blender - Edit - Preferences - Addons - Click the \/ (its upper right) - Install from disk - Select Blender Mesh Extruder.zip - Install from disk button
3. Press N or arrow to open default Sidebar (on right) - click Tool - it is below "Workspace" if no other addons.

Blender main how to use:
-
1. Press Z or -Z on your axis or hotkey Numpad 7
2. Press Draw Shape
3. Start placing dots that will connect sequentially.
4. When done close shape on first point or with RMB
5. Be careful with default Blender undo system, as if you mixed action in it, it can't redo.

Extra steps:

7. Reference? This 1st is step then, download sideview image.

8. Drag it from your folder to Blender, while looking topdown 2D (Z on axis pressed)

Typical use case (I want an outblock / ugly cow for my 3D Printer to 3D print):
-
![image](https://github.com/user-attachments/assets/dc59544b-4f10-4eaa-89ad-7b237aa0a9f2)



Unity how to use:
-
1. Download the zip *(On the right press '+' to see other releases and press it then press "source.zip" to download the project, unzip project folder = same list as on GitHub)*
2. Put the script anywhere in assets folder 
3. In Unity look upper - Tools - Simple Mesh Extruder
4. No grid, draw by hand, decrease your mouse DPI to 200 to achieve "mirrored" effect if needed.
5. RMB undo last line (it can't redo it back)
6. Close the and generate the shape by pressing first point or generate button

Typical use case:
-
Spam bunch of rigidbodies of simple shapes to test out ideas. (the end, use Blender one if want walls in one mesh)

Blender screenshots:
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

Unity:
-

![image](https://github.com/user-attachments/assets/dd4ba2c3-4421-4d66-a031-aa04d5dc2d61)

More recent screenshot of same version showing where to find it:
-
![image](https://github.com/user-attachments/assets/d825bb8d-eb41-48eb-908a-199a8ef31fa7)

The "normal" problem:
-
![image](https://github.com/user-attachments/assets/53a15831-030a-4046-a581-f17b9f23eb88)






Blender features (For Blender 4.0.0+):
-
1. Grid based dot placing on ground plane that automatically turn to edges
2. Merged in the end with LMB near last point or just by pressing RMB if there is at least 3 dots already
3. It automatically recalculates normals outside so your shader is not a mess.
4. Placing dots while not looking topdown or downtop is not recommended.
5. Etc?

Blender Issues:
-
1. You can't go less than 10 mm in grid snap (You can just disable grid if outlining reference), modify script self or give to AI for other improvements (Claude 3.5 is the best one?).
2. Extrusion can't be below 10 mm as is the grid.
3. You can't use UI if not closed the shape or cancelled it by 'Escape'.
4. You can't undo lines like in Unity (and redo too)
5. Do not go far from scene center, origin is at 0 0 0, if not want to RMB - Set Origin - Origin to Geometry, manually

Unity features:
-
1. Comparing to Blender it can undo lines with RMB
2. Can only make outline without grid snap and close the shape with extrusion
3. Can add a Rigidbody after creation

Unity Issues:
-
1. Yes, normals are madly flipped, especially in sharp meshes.
2. Geometry is worse than Blender one, if it was triangulated (?)
3. (Not checked) Can make redundant vertice in the same spot on closing as it was in early Blender version
4. Origin point is not correct, rotation will be bad without parenting to empty root gO.
5. Don't replace temporary " " mesh with the saved, you have to do it manually on need

The May Be Roadmap:
-
1. Make a toggleable mirror modifier while making shape or show a preview outline before generating it with mirror modifier
2. Make it a full fledge make a low-poly asset for games thing
3. Color in one click, texture draw whole separated meshes.
4. Separate meshes more easily than default solution
5. Make a solid mesh back easily
6. Proper Auto-UV making unwrapping in the process
7. Add toggleable origin to geometry on finish (in case it is not made in center)
8. All features are toggleable up to the state of classic simplest version

The Great final version goal sketches:
-
![The Potential End version](https://github.com/user-attachments/assets/46ec464d-8563-4942-8e3b-b02097b55ac9)
![image](https://github.com/user-attachments/assets/d5399f66-aaf8-4639-9bf3-f6d7946c9901)


Thoughts (This Last section is useless):
-
Probably the Unity one will be deprecated, as Unity doesn't have enough saturated libraries to manipulate meshes.
Or it will await when Blender one will be finished, to ask AI chat to remake (with many prompts) it for Unity, like it was with Blender one










Extra:

You are dead after fixing AI bugs and fixing Python identations, because your VSC flickers, as is it does the Upscayl when you upscaled your image. (Updated Windows 10, it fixed)

P.S.

Should i separate Unity version so it can be installed via github link thing? Probably there is no sense in doing so with just 1 script.

Contains 3 Branches (can a branch be installed by link?):
-
1. Whole thing
2. Only Blender
3. Only Unity
