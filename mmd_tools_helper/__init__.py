bl_info = {
	"name": "MMD tools helper",
	"author": "Hogarth-MMD",
	"version": (2, 4),
	"blender": (2, 80, 0),
	"location": "View3D > Tool Shelf > MMD Tools Helper",
	"description": "various mmd_tools helper scripts",
	"warning": "",
	"wiki_url": "",
	"category": "Object",
	}

__bl_classes = []
def register_wrap(cls):
    #print('%3d'%len(__bl_classes), cls)
    #assert(cls not in __bl_classes)
    if __make_annotations:
        bl_props = {k:v for k, v in cls.__dict__.items() if isinstance(v, __bpy_property)}
        if bl_props:
            if '__annotations__' not in cls.__dict__:
                setattr(cls, '__annotations__', {})
            annotations = cls.__dict__['__annotations__']
            for k, v in bl_props.items():
                #print('   -', k, v)
                #assert(v.__class__.__name__ == '_PropertyDeferred' or getattr(v[0], '__module__', None) == 'bpy.props' and isinstance(v[1], dict))
                annotations[k] = v
                delattr(cls, k)
    if hasattr(cls, 'bl_rna'):
        __bl_classes.append(cls)
    return cls

if "bpy" in locals():
    if bpy.app.version < (2, 71, 0):
        import imp as importlib
    else:
        import importlib
    importlib.reload(model)
    importlib.reload(mmd_view)
    importlib.reload(mmd_lamp_setup)
    importlib.reload(convert_to_blender_camera)
    importlib.reload(background_color_picker)
    importlib.reload(boneMaps_renamer)
    importlib.reload(replace_bones_renaming)
    importlib.reload(armature_diagnostic)
    importlib.reload(add_foot_leg_ik)
    importlib.reload(add_hand_arm_ik)
    importlib.reload(display_panel_groups)
    importlib.reload(toon_textures_to_node_editor_shader)
    importlib.reload(toon_modifier)
    importlib.reload(reverse_japanese_english)
    importlib.reload(miscellaneous_tools)
    importlib.reload(blender_bone_names_to_japanese_bone_names)
else:
    import bpy
    import logging

    __make_annotations = (bpy.app.version >= (2, 80, 0))
    __bpy_property = (bpy.props._PropertyDeferred if hasattr(bpy.props, '_PropertyDeferred') else tuple)
    from . import model
    from . import mmd_view
    from . import mmd_lamp_setup
    from . import convert_to_blender_camera
    from . import background_color_picker
    from . import boneMaps_renamer
    from . import replace_bones_renaming
    from . import armature_diagnostic
    from . import add_foot_leg_ik
    from . import add_hand_arm_ik
    from . import display_panel_groups
    from . import toon_textures_to_node_editor_shader
    from . import toon_modifier
    from . import reverse_japanese_english
    from . import miscellaneous_tools
    from . import blender_bone_names_to_japanese_bone_names

if bpy.app.version < (2, 80, 0):
    bl_info['blender'] = (2, 70, 0)

logging.basicConfig(format='%(message)s', level=logging.DEBUG)

@register_wrap
class MMDToolsHelperPanel(bpy.types.Panel):
	"""Creates the MMD Tools Helper Panel in a VIEW_3D TOOLS tab"""
	bl_label = "MMD Tools Helper"
	bl_idname = "OBJECT_PT_mmd_tools_helper"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "mmd_tools_helper"

	def draw(self, context):
		layout = self.layout
		row = layout.row()


def register():
    for cls in __bl_classes:
        bpy.utils.register_class(cls)
    print(__name__, 'registed %d classes'%len(__bl_classes))

def unregister():
    for cls in reversed(__bl_classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
