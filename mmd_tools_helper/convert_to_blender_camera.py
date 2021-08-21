import bpy

from . import register_wrap

@register_wrap
class MMDCameraToBlenderCameraPanel(bpy.types.Panel):
	"""Convert MMD cameras back to Blender cameras"""
	bl_idname = "OBJECT_PT_mmd_camera_to_blender_camera"
	bl_label = "Convert MMD Cameras to Blender cameras"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "mmd_tools_helper"

	def draw(self, context):
		layout = self.layout
		row = layout.row()

		row = layout.row()
		row.operator("mmd_tools_helper.mmd_camera_to_blender_camera", text = "Convert MMD cameras to Blender cameras")
		row = layout.row()

def main(context):
	for o in bpy.context.scene.objects:
		if o.type == 'CAMERA':
			camera = o
			camera.lock_location[0] = False
			camera.lock_location[1] = False
			camera.lock_location[2] = False
			camera.lock_rotation[0] = False
			camera.lock_rotation[1] = False
			camera.lock_rotation[2] = False
			camera.lock_scale[0] = False
			camera.lock_scale[1] = False
			camera.lock_scale[2] = False

			if o.animation_data is not None:
				for d in o.animation_data.drivers:
					d.mute = True

	if camera.parent is not None:
		if camera.parent.mmd_type == 'CAMERA':
			bpy.context.scene.objects.unlink(camera.parent)
			bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')

@register_wrap
class MMDCameraToBlenderCamera(bpy.types.Operator):
	"""Convert MMD cameras back to Blender cameras"""
	bl_idname = "mmd_tools_helper.mmd_camera_to_blender_camera"
	bl_label = "Convert MMD Cameras to Blender cameras"

	# @classmethod
	# def poll(cls, context):
		# return context.active_object is not None

	def execute(self, context):
		main(context)
		return {'FINISHED'}
