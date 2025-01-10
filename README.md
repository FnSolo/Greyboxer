# Mesh-Extruder-Blender-Unity-
A grid based line drawer on ground plane in Blender and a raw one for Unity, currently.
In Blender you get a quickly extruded N-Gon (will add a toggle auto a triangulate and tris to quad later).

Is it better than to do defaultly it from scratch with hotkeys? Let me know.

Using Blender 4.0.0+.
Blender version features:
1. Grid based dot placing on ground plane that automatically turn to edges
2. Merged in the end with LMB near last point or just by pressing RMB if there is at least 2 dots already
3. It automatically recalculates normals outside so your shader is not a mess.
4. Placing dots while not looking topdown or downtop is not recommended.
5. Etc?

Issues:
1. You can't go less than 10 mm in a grid in Blender one, modify script self or give to AI for other improvements (Claude 3.5 is the best one?).

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
