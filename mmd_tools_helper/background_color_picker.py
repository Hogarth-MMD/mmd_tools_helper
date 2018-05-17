import bpy
import sys

class MMDBackgroundColorPicker_Panel(bpy.types.Panel):
	"""Selects world background color and a contrasting text color"""
	bl_idname = "OBJECT_PT_mmd_background_color_picker"
	bl_label = "MMD background color picker"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"
	bl_category = "mmd_tools_helper"

	def draw(self, context):
		layout = self.layout
		row = layout.row()

		row = layout.row()
		layout.prop(context.scene, "BackgroundColor")
		row.operator("mmd_tools_helper.background_color_picker", text = "MMD background color picker")
		row = layout.row()


def main(context):
	screens = ['Animation', 'Scripting', 'UV Editing', 'Default']

	for screen in screens:
		for area in bpy.data.screens[screen].areas:
			if area.type == 'VIEW_3D':
				area.spaces[0].show_world = True

	bpy.context.scene.world.horizon_color = bpy.context.scene.BackgroundColor

	bpy.context.user_preferences.themes[0].view_3d.space.text_hi = (round(1-bpy.context.scene.BackgroundColor[0]), round(1-bpy.context.scene.BackgroundColor[1]),round(1-bpy.context.scene.BackgroundColor[2]))

class MMDBackgroundColorPicker(bpy.types.Operator):
	"""Selects world background color and a contrasting text color"""
	bl_idname = "mmd_tools_helper.background_color_picker"
	bl_label = "MMD background color picker"

	bpy.types.Scene.BackgroundColor =   bpy.props.FloatVectorProperty(name="Background Color", description="Set world background color", default=(1.0, 1.0, 1.0), min=0.0, max=1.0, soft_min=0.0, soft_max=1.0, step=3, precision=2, options={'ANIMATABLE'}, subtype='COLOR', unit='NONE', size=3, update=None, get=None, set=None)


	def execute(self, context):
		main(context)
		return {'FINISHED'}


def register():
	bpy.utils.register_class(MMDBackgroundColorPicker)
	bpy.utils.register_class(MMDBackgroundColorPicker_Panel)


def unregister():
	bpy.utils.unregister_class(MMDBackgroundColorPicker)
	bpy.utils.register_class(MMDBackgroundColorPicker_Panel)


if __name__ == "__main__":
	register()
