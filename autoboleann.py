bl_info = {
    "name": "bool Object",
    "author": "rglumampao",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Meshboolean > ",
    "description": "boolean mesh",
    "category": "Add Mesh",
}
import bpy

class AutoBooleanPanel(bpy.types.Panel):
    bl_label = "Auto Boolean"
    bl_idname = "OBJECT_PT_auto_boolean"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Boolean'

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.prop_search(context.scene, "obj1", bpy.data, "objects", text="boolObject")
        col.prop_search(context.scene, "obj2", bpy.data, "objects", text="cutter/join")
        col.prop(context.scene, "operation", expand=True)

        col.operator("object.auto_boolean", text="Auto Boolean")

class OBJECT_OT_auto_boolean(bpy.types.Operator):
    bl_idname = "object.auto_boolean"
    bl_label = "Auto Boolean"

    def execute(self, context):
        obj1 = context.scene.obj1
        obj2 = context.scene.obj2
        operation = context.scene.operation

        # Set the cutter object to display as wireframe for difference operation
        if operation == 'DIFFERENCE':
            obj2.display_type = 'WIRE'

        # Perform the boolean operation
        bpy.context.view_layer.objects.active = obj1
        bpy.ops.object.modifier_add(type='BOOLEAN')
        bpy.context.object.modifiers["Boolean"].operation = operation
        bpy.context.object.modifiers["Boolean"].object = obj2
        bpy.ops.object.modifier_apply(modifier="Boolean")

        return {'FINISHED'}

def register():
    bpy.utils.register_class(AutoBooleanPanel)
    bpy.utils.register_class(OBJECT_OT_auto_boolean)
    bpy.types.Scene.obj1 = bpy.props.PointerProperty(type=bpy.types.Object)
    bpy.types.Scene.obj2 = bpy.props.PointerProperty(type=bpy.types.Object)
    bpy.types.Scene.operation = bpy.props.EnumProperty(
        items=[('INTERSECT', 'Intersect', 'Intersect'),
               ('UNION', 'Union', 'Union'),
               ('DIFFERENCE', 'Difference', 'Difference')],
        name="Operation")

def unregister():
    bpy.utils.unregister_class(AutoBooleanPanel)
    bpy.utils.unregister_class(OBJECT_OT_auto_boolean)
    del bpy.types.Scene.obj1
    del bpy.types.Scene.obj2
    del bpy.types.Scene.operation

if __name__ == "__main__":
    register()
