# Scales the Blender grid, thereby making it unnecessary to scale MMD models.

import bpy
import math

from . import register_wrap

@register_wrap
class MMDViewPanel(bpy.types.Panel):
	"""Camera and Grid to be same as MikuMikuDance"""
	bl_idname = "OBJECT_PT_mmd_view"
	bl_label = "MMD View"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "mmd_tools_helper"

	def draw(self, context):
		layout = self.layout
		row = layout.row()

		row.label(text="MMD View", icon="CAMERA_DATA")
		row = layout.row()
		row.operator("mmd_tools_helper.mmd_view", text = "MMD View")
		row = layout.row()

def main(context):
	# bpy.context.scene.render.fps = 30

	bpy.context.user_preferences.system.use_international_fonts = True

	camera_objects = [ob for ob in bpy.context.scene.objects if ob.type == 'CAMERA']
	if len(camera_objects) == 0:
		camera_data = bpy.data.cameras.new("Camera")
		camera_object = bpy.data.objects.new("Camera", camera_data)
		bpy.context.scene.objects.link(camera_object)
		bpy.context.scene.update()
		bpy.context.scene.camera = camera_object

	if bpy.context.active_object is not None:
		active_object = bpy.context.active_object
	else:
		active_object = bpy.context.scene.objects[-1]



	o = bpy.context.scene.camera
	camera = o
	bpy.context.scene.objects.active = camera
	bpy.ops.mmd_tools.convert_to_mmd_camera(scale=1, bake_animation=False, camera_source='CURRENT', min_distance=0.1)
	# moves the camera to the world origin(0,0,0), x rotation 90 degrees, y rotation 0 degrees, z rotation 0 degrees
	# creates an empty object at the world origin(0,0,0), x,y,z rotations = (0,0,0) , empty object is made parent of the camera

	camera.parent.location[0] = 0
	camera.parent.location[1] = 0
	camera.parent.location[2] = 10 #MMD y (height) 10, Blender z (height) 10
	camera.parent.rotation_euler[0] = 0
	camera.parent.rotation_euler[1] = 0
	camera.parent.rotation_euler[2] = 0
	camera.location[0] = 0
	camera.location[1] = -45 # = MMD camera distance
	camera.location[2] = 0
	camera.rotation_euler[0] = math.pi/2
	camera.rotation_euler[1] = 0
	camera.rotation_euler[2] = 0
	camera.parent.mmd_camera.angle = 0.523599 #(camera lens viewing angle, 0.523599 radians = 30 degrees)
	# bpy.context.space_data.lock_camera = True


	screens = ['Animation', 'Scripting', 'UV Editing', 'Default']

	for screen in screens:
		for area in bpy.data.screens[screen].areas:
			if area.type == 'VIEW_3D':
				area.spaces[0].grid_lines = 20
				area.spaces[0].grid_scale = 5
				area.spaces[0].region_3d.view_perspective = 'CAMERA'
				# Possible options are [‘PERSP’, ‘ORTHO’, ‘CAMERA’]
				area.spaces[0].show_world = True
				#bpy.data.screens['Default'].areas[4].spaces[0].show_world = True
	bpy.context.scene.world.horizon_color = (1, 1, 1)
	bpy.context.user_preferences.themes[0].view_3d.space.text_hi = (0,0,0)

	# for o in bpy.context.scene.objects:
		# if o.type == "ARMATURE":
			# o.data.show_names = True

	bpy.context.scene.objects.active = active_object



@register_wrap
class MMDView(bpy.types.Operator):
	"""Camera and Grid to be same as MikuMikuDance"""
	bl_idname = "mmd_tools_helper.mmd_view"
	bl_label = "MMD View"

	# @classmethod
	# def poll(cls, context):
		# return context.active_object is not None

	def execute(self, context):
		main(context)
		return {'FINISHED'}
