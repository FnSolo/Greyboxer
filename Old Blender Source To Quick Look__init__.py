# This version bugs, when deleting default cube... Only for core code quick read!
bl_info = {
    "description": "ESC: Cancel. Pages: Height change",
    "name": "Greyboxer",
    "author": "Unlicense",
    "version": (1, 1),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Greyboxer",
    "category": "Mesh",
}

import blf
import bpy
import gpu
import bmesh
from gpu_extras.batch import batch_for_shader
from bpy.types import Panel, Operator, PropertyGroup
from bpy.props import (FloatProperty, BoolProperty, FloatVectorProperty, 
                      PointerProperty, IntProperty, BoolVectorProperty)
from mathutils import Vector
from bpy_extras import view3d_utils
import math

class MeshExtruderProperties(PropertyGroup):
    # Rename to make it clearer
    extrude_depth: FloatProperty(
        name="Extrude Amount",
        description="Amount to extrude (when enabled)",
        default=1.0,
        # min=0.01, # we don't need to restrict the user(can bug w/ commented?)
        unit='LENGTH'
    )
    
    grid_size: FloatProperty(
        name="Grid Size",
        description="Size of grid snapping",
        default=0.25,
        min=0.01,
        unit='LENGTH'
    )
    
    snap_grid: BoolProperty(
        name="Snap to Grid",
        default=True
    )
    
    smooth_shading: BoolProperty(
        name="Smooth Shading",
        default=False
    )
    
    # Mirror settings
    use_mirror: BoolProperty(
        name="Add Mirror",
        default=False
    )
    mirror_x: BoolProperty(name="X", default=True)
    mirror_y: BoolProperty(name="Y", default=False)
    mirror_z: BoolProperty(name="Z", default=False)
    mirror_clip: BoolProperty(name="Clip", default=True)
    
    wall_mode: BoolProperty(
        name="Edge Mode",
        description="Create edges without closing shape",
        default=False
    )
    
    # Solidify settings
    use_solidify: BoolProperty(
        name="Add Solidify",
        default=False
    )
    wall_thickness: FloatProperty(
        name="Wall Thickness",
        description="Thickness of walls",
        default=0.1,
        min=0.001,
        max=10.0,
        unit='LENGTH'
    )
    solidify_offset: FloatProperty(
        name="Wall Offset",
        description="Offset of the wall thickness",
        default=0.0, # keep 0 for wall mode
        min=-1.0,
        max=1.0
    )
    use_even_thickness: BoolProperty(
        name="Even Thickness",
        description="Maintain even thickness across the wall",
        default=True
    )
    
    # Bevel settings
    use_bevel: BoolProperty(
        name="Add Bevel",
        default=False
    )
    bevel_width: FloatProperty(
        name="Bevel Width",
        description="Width of bevel",
        default=0.02,
        min=0.0001,
        max=1.0,
        unit='LENGTH'
    )
    bevel_segments: IntProperty(
        name="Segments",
        description="Number of bevel segments",
        default=2,
        min=1,
        max=10
    )
    
    segmented_mode: BoolProperty(
        name="Segmented Mode",
        description="Create separate segments for walls",
        default=False
    )
    
    draw_height: FloatProperty(
        name="Draw Height",
        description="Height level for drawing",
        default=0.0,
        unit='LENGTH'
    )
    
    height_step: FloatProperty(
        name="Height Step",
        description="Amount to change height by PgUp - Step up. PgDwn - Step down",
        default=1.0,
        min=0.01,
        unit='LENGTH'
    )
    
    # Add after existing properties
    use_extrude: BoolProperty(
        name="Extrude",
        description="Enable/disable extrusion",
        default=True
    )


class VIEW3D_PT_mesh_extruder(Panel):
    bl_label = "Greyboxer"
    bl_idname = "VIEW3D_PT_mesh_extruder"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Greyboxer'
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.mesh_extruder

        # Main properties
        col = layout.column(align=True)
        col.prop(props, "grid_size")
        col.prop(props, "snap_grid")
        col.prop(props, "smooth_shading")
        
        # Add height controls NEW
        col.separator()
        col.prop(props, "draw_height")
        col.prop(props, "height_step")
        
        # Extrusion controls NEW
        col.separator()
        row = col.row(align=True)
        row.prop(props, "use_extrude", toggle=True)
        sub = row.row()
        sub.active = props.use_extrude  # Gray out when disabled
        sub.prop(props, "extrude_depth")
        
        # Modifier settings
        box = layout.box()
        box.label(text="Modifiers:")
        
        # Wall Mode
        col = box.column(align=True)
        col.prop(props, "wall_mode")
        if props.wall_mode:
            col.prop(props, "segmented_mode")
        
        # Mirror settings
        col.prop(props, "use_mirror", text="Mirror")
        if props.use_mirror:
            box = col.box()
            row = box.row(align=True)
            row.prop(props, "mirror_x")
            row.prop(props, "mirror_y")
            row.prop(props, "mirror_z")
            box.prop(props, "mirror_clip")
        
        # Solidify settings
        col.prop(props, "use_solidify", text="Solidify")
        if props.use_solidify:
            box = col.box()
            box.prop(props, "wall_thickness")
            box.prop(props, "solidify_offset")
            box.prop(props, "use_even_thickness")
        
        # Bevel settings
        col.prop(props, "use_bevel", text="Bevel")
        if props.use_bevel:
            box = col.box()
            box.prop(props, "bevel_width")
            box.prop(props, "bevel_segments")
        
        # Operator button
        layout.operator("mesh.extruder_draw", text="Draw Shape")

def apply_modifiers(self, context, obj):
    props = context.scene.mesh_extruder
    
    if props.use_mirror:
        mirror_mod = obj.modifiers.new(name="Mirror", type='MIRROR')
        mirror_mod.use_axis[0] = props.mirror_x
        mirror_mod.use_axis[1] = props.mirror_y
        mirror_mod.use_axis[2] = props.mirror_z
        mirror_mod.use_clip = props.mirror_clip

    if props.use_solidify:
        solid_mod = obj.modifiers.new(name="Solidify", type='SOLIDIFY')
        solid_mod.thickness = props.wall_thickness
        solid_mod.offset = props.solidify_offset
        solid_mod.use_even_offset = props.use_even_thickness

    if props.use_bevel:
        bevel_mod = obj.modifiers.new(name="Bevel", type='BEVEL')
        bevel_mod.width = props.bevel_width
        bevel_mod.segments = props.bevel_segments

class MESH_OT_ExtruderDraw(Operator):
    bl_idname = "mesh.extruder_draw"
    bl_label = "Draw Shape"
    bl_options = {'REGISTER', 'UNDO'}
    
    # NEW unleaky?
    def __init__(self):
        self.points = []
        self.is_near_start = False
        self._handle = None
        self._handle_text = None
        self.close_threshold = 20
    
    def snap_to_grid(self, point, grid_size):
        return Vector((
            round(point.x / grid_size) * grid_size,
            round(point.y / grid_size) * grid_size,
            round(point.z / grid_size) * grid_size
        ))
    
    isWallMode: bool = False

    # [Previous draw_callback_px, draw_text, get_3d_point, and check_near_start methods remain the same]

    def create_mesh(self, context):
        if len(self.points) < 2:
            return

        props = context.scene.mesh_extruder
        
        if props.wall_mode:
            if props.segmented_mode:
                for i in range(len(self.points) - 1):
                    dir_vector = self.points[i+1] - self.points[i]
                    dir_vector.normalize()
                    
                    mesh = bpy.data.meshes.new(f"Wall_Segment_{i}")
                    obj = bpy.data.objects.new(f"Wall_Segment_{i}", mesh)
                    context.collection.objects.link(obj)
                    
                    bm = bmesh.new()
                    
                    thickness = props.wall_thickness
                    if i > 0:
                        start_point = self.points[i] - (dir_vector * thickness/2)
                    else:
                        start_point = self.points[i]
                        
                    if i < len(self.points) - 2:
                        end_point = self.points[i+1] + (dir_vector * thickness/2)
                    else:
                        end_point = self.points[i+1]
                    
                    v1 = bm.verts.new(start_point)
                    v2 = bm.verts.new(end_point)
                    
                    edge = bm.edges.new((v1, v2))
                    ret = bmesh.ops.extrude_edge_only(bm, edges=[edge])
                    verts = [v for v in ret["geom"] if isinstance(v, bmesh.types.BMVert)]
                    
                    bmesh.ops.translate(bm,
                        vec=(0, 0, props.extrude_depth),
                        verts=verts)
                    
                    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
                    
                    bm.to_mesh(mesh)
                    mesh.update()
                    
                    apply_modifiers(self, context, obj)
                    
                    if props.smooth_shading:
                        for f in mesh.polygons:
                            f.use_smooth = True
                            
                    bm.free()
            else:
                mesh = bpy.data.meshes.new("Edge_Shape")
                obj = bpy.data.objects.new("Edge_Shape", mesh)
                context.collection.objects.link(obj)
                
                bm = bmesh.new()
                
                verts = []
                prev_point = None
                for point in self.points:
                    if prev_point is None or (point - prev_point).length > 0.0001:
                        verts.append(bm.verts.new(point))
                        prev_point = point
                
                edges = []
                for i in range(len(verts)-1):
                    edges.append(bm.edges.new((verts[i], verts[i+1])))
                
                ret = bmesh.ops.extrude_edge_only(bm, edges=edges)
                extruded_verts = [v for v in ret["geom"] if isinstance(v, bmesh.types.BMVert)]
                
                extruded_verts.sort(key=lambda v: (v.co[0], v.co[1]))
                
                bmesh.ops.translate(bm,
                    vec=(0, 0, props.extrude_depth),
                    verts=extruded_verts)
                
                bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
                for face in bm.faces:
                    if face.normal.z < 0:
                        face.normal_flip()
                
                bm.to_mesh(mesh)
                mesh.update()
                
                apply_modifiers(self, context, obj)
                
                if props.smooth_shading:
                    for f in mesh.polygons:
                        f.use_smooth = True
                        
                bm.free()
        else:
            # Non-wall mode (closed shape)
            mesh = bpy.data.meshes.new("Shape")
            obj = bpy.data.objects.new("Shape", mesh)
            context.collection.objects.link(obj)
            
            bm = bmesh.new()
            
            # Create vertices
            verts = [bm.verts.new(point) for point in self.points]
            
            # Create faces
            bm.faces.new(verts)
            
            # Extrude (New)
            if props.use_extrude:
                ret = bmesh.ops.extrude_face_region(bm, geom=[f for f in bm.faces])
                verts = [v for v in ret["geom"] if isinstance(v, bmesh.types.BMVert)]
                
                bmesh.ops.translate(bm,
                    vec=(0, 0, props.extrude_depth),
                    verts=verts)
            
            bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
            
            bm.to_mesh(mesh)
            mesh.update()
            
            apply_modifiers(self, context, obj)
            
            if props.smooth_shading:
                for f in mesh.polygons:
                    f.use_smooth = True
                    
            bm.free()
            
        return {'FINISHED'}

    # draw help
    def draw_callback_px(self, context):
        global isWallMode
        isWallMode = context.scene.mesh_extruder.wall_mode
        
        # Add constant draw mode indicator NEW
        font_id = 0
        blf.size(font_id, 10)      
        # Draw mode indicator
        blf.position(font_id, 60, 140, 0)
        blf.draw(font_id, "(Can't use UI. \n Pg to height. \n ESC: Cancel drawed)")
        
        # Draw help text first
        if isWallMode:
            self.draw_text(context, "RMB: Finish.")
            
        if not self.points:
            return
            
        shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        region = context.region
        rv3d = context.region_data
        points_2d = []
        
        # Convert all points to 2D for drawing
        for point in self.points:
            point_2d = view3d_utils.location_3d_to_region_2d(region, rv3d, point)
            if point_2d:
                points_2d.append(point_2d)
        
        if not points_2d:
            return
        
        # Draw lines
        if len(points_2d) > 1:
            shader.bind()
            shader.uniform_float("color", (1, 1, 1, 1))
            batch = batch_for_shader(shader, 'LINE_STRIP', {"pos": points_2d})
            batch.draw(shader)
        
        # Draw points
        shader.bind()
        for i, point_2d in enumerate(points_2d):
            if i == 0 and self.is_near_start:
                shader.uniform_float("color", (0, 1, 0, 1))
            else:
                shader.uniform_float("color", (1, 0, 0, 1))
            batch = batch_for_shader(shader, 'POINTS', {"pos": [point_2d]})
            gpu.state.point_size_set(10 if i == 0 else 6)
            batch.draw(shader)
            
        # Draw help text
        if len(self.points) > 2 and not isWallMode:
            if self.is_near_start:
                self.draw_text(context, "Click to close shape")
            else:
                self.draw_text(context, "Right-click to finish")
             
        # Add height indicator text
        height_text = f"Height: {context.scene.mesh_extruder.draw_height:.2f}"
        font_id = 0
        blf.size(font_id, 20)
        blf.position(font_id, 60, 100, 0)
        blf.draw(font_id, height_text)
    
    def draw_text(self, context, text):
        font_id = 0
        blf.size(font_id, 20)
        blf.position(font_id, 60, 60, 0)
        blf.draw(font_id, text)
    
    # Upd. to sup height and make it correctly
    def get_3d_point(self, context, event):
        mouse_pos = event.mouse_region_x, event.mouse_region_y
        region = context.region
        rv3d = context.region_data
        view_vector = view3d_utils.region_2d_to_vector_3d(region, rv3d, mouse_pos)
        ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, mouse_pos)
        
        plane_normal = Vector((0, 0, 1))
        # Ensure exact height placement
        height = context.scene.mesh_extruder.draw_height
        plane_point = Vector((0, 0, height))
        
        denominator = view_vector.dot(plane_normal)
        if abs(denominator) > 0:
            t = (plane_point - ray_origin).dot(plane_normal) / denominator
            point = ray_origin + t * view_vector
            
            if context.scene.mesh_extruder.snap_grid:
                snapped = self.snap_to_grid(point, context.scene.mesh_extruder.grid_size)
                # Force exact height after snapping
                snapped.z = height
                return snapped
            
            # Force exact height for non-snapped points too
            point.z = height
            return point
        return None
    
    def check_near_start(self, context, event):
        if len(self.points) < 3:
            return False
            
        region = context.region
        rv3d = context.region_data
        
        start_2d = view3d_utils.location_3d_to_region_2d(region, rv3d, self.points[0])
        if not start_2d:
            return False
            
        mouse_pos = Vector((event.mouse_region_x, event.mouse_region_y))
        return (mouse_pos - Vector((start_2d.x, start_2d.y))).length < self.close_threshold
    
    def cleanup(self):
        if self._handle:
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            self._handle = None
    
    def modal(self, context, event):
        if context.area:
            context.area.tag_redraw()
        # new
        try:
            # Add height control with PageUp/PageDown
            if event.type == 'PAGE_UP' and event.value == 'PRESS':
                context.scene.mesh_extruder.draw_height += context.scene.mesh_extruder.height_step
                return {'RUNNING_MODAL'}
                
            elif event.type == 'PAGE_DOWN' and event.value == 'PRESS':
                context.scene.mesh_extruder.draw_height -= context.scene.mesh_extruder.height_step
                return {'RUNNING_MODAL'}
        # new
            self.is_near_start = False if context.scene.mesh_extruder.wall_mode else self.check_near_start(context, event)
            
            if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                point = self.get_3d_point(context, event)
                if point:
                    self.points.append(point)
                    if not context.scene.mesh_extruder.wall_mode and self.is_near_start and len(self.points) >= 3:
                        self.points.append(self.points[0])
                        self.create_mesh(context)
                        self.cleanup()
                        return {'FINISHED'}
                return {'RUNNING_MODAL'}
                    
            elif event.type in {'RIGHTMOUSE', 'ESC'}:
                self.cleanup()
                if event.type == 'RIGHTMOUSE' and len(self.points) >= 2:
                    self.create_mesh(context)
                return {'FINISHED'}
            
            return {'PASS_THROUGH'}
                
        except Exception as e:
            self.report({'ERROR'}, f"Error in modal: {str(e)}")
            self.cleanup()
            return {'CANCELLED'}

    def invoke(self, context, event):
        if context.area.type != 'VIEW_3D':
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}

        self.points.clear()
        args = (context,)
        self._handle = bpy.types.SpaceView3D.draw_handler_add(
            self.draw_callback_px, args, 'WINDOW', 'POST_PIXEL')
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
    
    
classes = (
    MeshExtruderProperties,
    MESH_OT_ExtruderDraw,
    VIEW3D_PT_mesh_extruder,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.mesh_extruder = PointerProperty(type=MeshExtruderProperties)
    
def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.mesh_extruder

if __name__ == "__main__":
    register()
