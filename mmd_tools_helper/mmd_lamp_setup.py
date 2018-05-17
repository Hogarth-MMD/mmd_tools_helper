import bpy

class MMDLampSetupPanel(bpy.types.Panel):
	"""One-click Lamp Setup for mmd_tools"""
	bl_idname = "OBJECT_PT_mmd_lamp_setup"
	bl_label = "MMD Lamp Setup"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"
	bl_category = "mmd_tools_helper"

	def draw(self, context):
		layout = self.layout
		row = layout.row()

		row.label(text="MMD Lamp", icon="LAMP")
		row = layout.row()
		row.operator("mmd_tools_helper.mmd_lamp_setup", text = "MMD Lamp")
		row = layout.row()
		row = layout.row()

def lamp_setup(o):
	o.rotation_mode = 'XYZ'
	o.rotation_euler[0] = 0.785398 #45 degrees in radians
	o.rotation_euler[1] = 0
	o.rotation_euler[2] = 0.785398 #45 degrees in radians
	o.location = (30, -30, 30)
	o.scale = (2,2,2)

	o.data.type = 'SUN'
	o.data.color = (0.6, 0.6, 0.6)
	o.data.shadow_ray_samples = 4
	o.data.shadow_soft_size = 2.0
	o.data.shadow_color = (0.4, 0.4, 0.4)

def main(context):
	bpy.context.scene.game_settings.material_mode = 'GLSL'
	bpy.context.space_data.viewport_shade = 'TEXTURED'
	bpy.context.scene.world.light_settings.use_environment_light = True

	#Set color management to None
	bpy.context.scene.display_settings.display_device = 'None'

	lamp_objects = [ob for ob in bpy.context.scene.objects if ob.type == 'LAMP']
	if len(lamp_objects) == 0:
		lamp_data = bpy.data.lamps.new("Lamp", "SUN")
		lamp_object = bpy.data.objects.new("Lamp", lamp_data)
		bpy.context.scene.objects.link(lamp_object)
		bpy.context.scene.update()

	if bpy.context.active_object is not None:
		active_object = bpy.context.active_object
	else:
		active_object = bpy.context.scene.objects[-1]


	if bpy.context.active_object is not None:
		if bpy.context.active_object.type == 'LAMP':
			o = bpy.context.active_object
			lamp_setup(o)
		else:
			lamp_objects = [ob for ob in bpy.context.scene.objects if ob.type == 'LAMP']
			o = lamp_objects[0]
			bpy.context.scene.objects.active = o
			lamp_setup(o)


	bpy.context.scene.objects.active = active_object

				# bpy.context.scene.world.ambient_color = (0.6, 0.6, 0.6)

				# o.data.type = 'SPOT'
				# o.data.shadow_method = 'BUFFER_SHADOW'
				# o.data.distance = 45
				# o.data.spot_size = 1.309 #radians = 75 degress
				# o.data.use_auto_clip_start = True
				# o.data.use_auto_clip_end = True
				# o.data.shadow_color = (0, 0, 0)

class MMDLampSetup(bpy.types.Operator):
	"""One-click Lamp Setup for mmd_tools"""
	bl_idname = "mmd_tools_helper.mmd_lamp_setup"
	bl_label = "MMD Lamp Setup"

	# @classmethod
	# def poll(cls, context):
		# return context.active_object is not None

	def execute(self, context):
		main(context)
		return {'FINISHED'}


def register():
	bpy.utils.register_class(MMDLampSetup)
	bpy.utils.register_class(MMDLampSetupPanel)


def unregister():
	bpy.utils.unregister_class(MMDLampSetup)
	bpy.utils.unregister_class(MMDLampSetupPanel)


if __name__ == "__main__":
	register()

