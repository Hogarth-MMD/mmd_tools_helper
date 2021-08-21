
import bpy

from . import register_wrap
from . import model

@register_wrap
class ReplaceBonesRenamingPanel(bpy.types.Panel):
	"""Replace Bones Renaming panel"""
	bl_label = "Replace bones renaming panel"
	bl_idname = "OBJECT_PT_replace_bones_renaming"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "mmd_tools_helper"

	def draw(self, context):
		layout = self.layout
		row = layout.row()
		row.label(text="Find this string in bone names:")
		row = layout.row()
		row.prop(context.scene,"find_bone_string")
		row = layout.row()
		row.label(text="Replace it with this string:")
		row = layout.row()
		row.prop(context.scene,"replace_bone_string")
		row = layout.row()
		row.prop(context.scene, "bones_all_or_selected")
		row = layout.row()
		row.label(text="Selected bones only")
		row = layout.row()
		row.operator("mmd_tools_helper.replace_bones_renaming", text = "Find and replace a string in bone names")
		row = layout.row()

def main(context):
	bpy.context.scene.objects.active = model.findArmature(bpy.context.active_object)
	if bpy.context.scene.bones_all_or_selected == True:
		for b in bpy.context.active_object.data.bones:
			if b.select == True:
				if 'dummy' not in b.name and 'shadow' not in b.name:
					b.name = b.name.replace(bpy.context.scene.find_bone_string, bpy.context.scene.replace_bone_string)
	if bpy.context.scene.bones_all_or_selected == False:
		for b in bpy.context.active_object.data.bones:
			if 'dummy' not in b.name and 'shadow' not in b.name:
				b.name = b.name.replace(bpy.context.scene.find_bone_string, bpy.context.scene.replace_bone_string)


@register_wrap
class ReplaceBonesRenaming(bpy.types.Operator):
	"""Find and replace mass renaming of bones"""
	bl_idname = "mmd_tools_helper.replace_bones_renaming"
	bl_label = "Replace bones renaming"

	bpy.types.Scene.find_bone_string = bpy.props.StringProperty(name="", description="", default="", maxlen=0, options={'ANIMATABLE'}, subtype='NONE', update=None, get=None, set=None)
	
	bpy.types.Scene.replace_bone_string = bpy.props.StringProperty(name="", description="", default="", maxlen=0, options={'ANIMATABLE'}, subtype='NONE', update=None, get=None, set=None)

	bpy.types.Scene.bones_all_or_selected = bpy.props.BoolProperty(name="Selected bones only", description="", default=False, options={'ANIMATABLE'}, subtype='NONE', update=None, get=None, set=None)

	@classmethod
	def poll(cls, context):
		return context.active_object is not None

	def execute(self, context):
		main(context)
		return {'FINISHED'}
