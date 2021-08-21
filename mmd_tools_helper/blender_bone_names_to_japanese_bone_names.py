import bpy

from . import register_wrap
from . import model

@register_wrap
class BlenderToJapaneseBoneNamesPanel(bpy.types.Panel):
	"""Creates a Panel"""
	bl_idname = "OBJECT_PT_blender_to_japanese_bone_names"
	bl_label = "Copy Blender bone names to Japanese bone names"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "mmd_tools_helper"

	def draw(self, context):
		layout = self.layout
		row = layout.row()

		row.label(text="Copy Blender bone names to Japanese bone names", icon="TEXT")
		row = layout.row()
		row.operator("mmd_tools_helper.blender_to_japanese_bone_names", text = "Copy Blender bone names to Japanese bone names")
		row = layout.row()

def main(context):
	armature = model.findArmature(bpy.context.active_object)
	for b in armature.data.bones:
		if hasattr(armature.pose.bones[b.name], "mmd_bone"):
			armature.pose.bones[b.name].mmd_bone.name_j = b.name


@register_wrap
class BlenderToJapaneseBoneNames(bpy.types.Operator):
	"""Copy Blender bone names to Japanese bone names"""
	bl_idname = "mmd_tools_helper.blender_to_japanese_bone_names"
	bl_label = "Copy Blender bone names to Japanese bone names"

	def execute(self, context):
		main(context)
		return {'FINISHED'}
