import bpy
from . import model


# Each image is a list of numbers(floats): R,G,B,A,R,G,B,A etc.
# So the length of the list of pixels is 4 X number of pixels
# pixels are in left-to-right rows from bottom left to top right of image

class MMDToonTexturesToNodeEditorShaderPanel(bpy.types.Panel):
	"""Sets up nodes in Blender node editor for rendering toon textures"""
	bl_idname = "OBJECT_PT_mmd_toon_render_node_editor"
	bl_label = "MMD toon textures render using node editor "
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"
	bl_category = "mmd_tools_helper"

	def draw(self, context):
		layout = self.layout
		row = layout.row()

		row.label(text="MMD Render toon textures", icon="MATERIAL")
		row = layout.row()
		row.operator("mmd_tools_helper.mmd_toon_render_node_editor", text = "MMD Create Toon Material Nodes")
		row = layout.row()

def toon_image_to_color_ramp(toon_texture_color_ramp, toon_image):
	pixels_width = toon_image.size[0]
	pixels_height = toon_image.size[1]
	toon_image_pixels = []
	toon_image_gradient = []

	for f in range(0, len(toon_image.pixels), 4):
		pixel_rgba = toon_image.pixels[f:f+4]
		toon_image_pixels.append(pixel_rgba)

	for p in range(0, len(toon_image_pixels), int(len(toon_image_pixels)/32)):
		toon_image_gradient.append(toon_image_pixels[p])

	toon_texture_color_ramp.color_ramp.elements[0].color = toon_image_gradient[0]
	toon_texture_color_ramp.color_ramp.elements[-1].color = toon_image_gradient[-1]

	for i in range(1, len(toon_image_gradient)-2, 1):
		toon_texture_color_ramp.color_ramp.elements.new(i/(len(toon_image_gradient)-1))
		toon_texture_color_ramp.color_ramp.elements[i].color = toon_image_gradient[i]
		if i > len(toon_image_gradient)/2:
			toon_texture_color_ramp.color_ramp.elements[i].color[3] = 0.0 #alpha of non-shadow colors set to 0.0

	return

# def toon_image_bottom_half_to_color_ramp(toon_texture_color_ramp, toon_image):
	# pixels_width = toon_image.size[0]
	# pixels_height = toon_image.size[1]
	# toon_image_pixels = []
	# toon_image_gradient = []

	# for f in range(0, len(toon_image.pixels), 4):
		# pixel_rgba = toon_image.pixels[f:f+4]
		# toon_image_pixels.append(pixel_rgba)

	# for p in range(0, len(toon_image_pixels), int(len(toon_image_pixels)/32)):
		# toon_image_gradient.append(toon_image_pixels[p])

	# toon_texture_color_ramp.color_ramp.elements[0].color = toon_image_gradient[0]
	# toon_texture_color_ramp.color_ramp.elements[-1].color = toon_image_gradient[-1]

	# print('length of toon_image_gradient = ', len(toon_image_gradient))
	# for i in range(1, int(len(toon_image_gradient)/2)-1, 1):
		# toon_texture_color_ramp.color_ramp.elements.new((i*2/(len(toon_image_gradient)-1)))
		# toon_texture_color_ramp.color_ramp.elements[i].color = toon_image_gradient[i]

	# return

def clear_material_nodes(context):
	for m in bpy.context.active_object.data.materials:
		if m.node_tree is not None:
			for n in range(len(m.node_tree.nodes)-1, 1, -1):
				m.node_tree.nodes.remove(m.node_tree.nodes[n])

# def create_default_material_nodes(context):
	# bpy.context.area.type = 'NODE_EDITOR'
	# for m in bpy.context.active_object.data.materials:
		# if m.node_tree is not None:
			# default_output_node = m.node_tree.nodes.new('ShaderNodeOutput')
			# default_output_node.location = (300, 300)
			# default_output_node.update()
			# default_material_node = m.node_tree.nodes.new('ShaderNodeMaterial')
			# default_material_node.location = (10, 300)
			# default_material_node.material = m
			# default_material_node.update()
			# m.node_tree.interface_update(bpy.context)
			# m.node_tree.nodes.update()
			# m.node_tree.links.new(default_output_node.inputs['Color'], default_material_node.outputs['Color'])
			# m.use_nodes = False
			# m.use_nodes = True
	# bpy.context.area.type = 'VIEW_3D'



def main(context):
	o = bpy.context.active_object
	if o.type == 'MESH':

		if len(bpy.data.lamps) == 0:
			bpy.data.lamps.new("Lamp", "SUN")

		for object in bpy.context.scene.objects:
			if object.data == bpy.data.lamps[0]:
				LAMP = object

		if o.data.materials is not None:
			for m in o.data.materials:
				m.use_nodes = True
				# m.node_tree.nodes.new('OUTPUT')
				# m.node_tree.nodes.new('MATERIAL')
				output_node = m.node_tree.nodes[0]
				output_node.location = (1450, 800)
				material_node = m.node_tree.nodes[1]
				material_node.material = m
				material_node.location = (-800, 800)

				lamp_node = m.node_tree.nodes.new('ShaderNodeLampData')
				lamp_node.lamp_object = LAMP
				lamp_node.location = (-530, -50)

				rgb_to_bw = m.node_tree.nodes.new('ShaderNodeRGBToBW')
				rgb_to_bw.location = (-90, -50) #(120, 470) (-530, -50)

				vector_math_node = m.node_tree.nodes.new('ShaderNodeVectorMath')
				vector_math_node.operation = 'DOT_PRODUCT'
				vector_math_node.location = (-520, 470)

				math_node_1 = m.node_tree.nodes.new('ShaderNodeMath')
				math_node_1.operation = 'ADD'
				math_node_1.inputs[1].default_value = 1.0
				math_node_1.location = (-325, 470)

				math_node_2 = m.node_tree.nodes.new('ShaderNodeMath')
				math_node_2.operation = 'MULTIPLY'
				math_node_2.inputs[1].default_value = 0.5 #1.0
				# math_node_2.use_clamp = True
				math_node_2.location = (-90, 470)

				math_node_3 = m.node_tree.nodes.new('ShaderNodeMath')
				math_node_3.operation = 'MULTIPLY'
				math_node_3.location = (120, 470)

				toon_texture_color_ramp = m.node_tree.nodes.new('ShaderNodeValToRGB')
				toon_texture_color_ramp.location = (340, 470)

				mix_rgb_node_ramp_overlay = m.node_tree.nodes.new('ShaderNodeMixRGB')
				mix_rgb_node_ramp_overlay.blend_type = 'MULTIPLY' #was 'OVERLAY'
				mix_rgb_node_ramp_overlay.inputs[0].default_value = 1.0
				mix_rgb_node_ramp_overlay.inputs['Color2'].default_value = (1.0, 1.0, 1.0, 1.0)
				mix_rgb_node_ramp_overlay.location = (690, 470)
				mix_rgb_node_ramp_overlay.label = "toon_modifier"

				mix_rgb_node = m.node_tree.nodes.new('ShaderNodeMixRGB')
				mix_rgb_node.blend_type = 'MULTIPLY'
				mix_rgb_node.inputs[0].default_value = 1.0
				# mix_rgb_node.use_clamp = True
				mix_rgb_node.location = (1000, 470)
				mix_rgb_node.inputs['Color2'].default_value = (m.diffuse_color[0], m.diffuse_color[1], m.diffuse_color[2], 1.0)

				mix_rgb_node_add_sphere = m.node_tree.nodes.new('ShaderNodeMixRGB')
				mix_rgb_node_add_sphere.blend_type = 'ADD'
				mix_rgb_node_add_sphere.inputs[0].default_value = 1.0
				mix_rgb_node_add_sphere.location = (1240, 470)

				diffuse_texture_geomety_uv_node = m.node_tree.nodes.new('ShaderNodeGeometry')
				diffuse_texture_geomety_uv_node.location = (620, 250)

				diffuse_texture_node = m.node_tree.nodes.new('ShaderNodeTexture')
				diffuse_texture_node.location = (820, 250)

				sphere_texture_geometry_normal_node = m.node_tree.nodes.new('ShaderNodeGeometry')
				sphere_texture_geometry_normal_node.location = (620, -50)

				sphere_texture_node = m.node_tree.nodes.new('ShaderNodeTexture')
				sphere_texture_node.location = (820, -50)


				print(len(m.node_tree.links))
				m.node_tree.links.new(output_node.inputs['Alpha'], material_node.outputs['Alpha'])
				print(len(m.node_tree.links))
				m.node_tree.links.new(vector_math_node.inputs[0], material_node.outputs['Normal']) #vector_math_node.inputs['Vector']
				print(len(m.node_tree.links))
				m.node_tree.links.new(vector_math_node.inputs[1], lamp_node.outputs['Light Vector']) #vector_math_node.inputs['Vector']
				print(len(m.node_tree.links))
				m.node_tree.links.new(rgb_to_bw.inputs['Color'], lamp_node.outputs['Shadow']) #math_node_3.inputs['Value']
				print(len(m.node_tree.links))
				m.node_tree.links.new(math_node_3.inputs[1], rgb_to_bw.outputs['Val'])

				print(len(m.node_tree.links))
				m.node_tree.links.new(math_node_1.inputs[0], vector_math_node.outputs['Value']) #math_node_1.inputs['Value']
				print(len(m.node_tree.links))
				m.node_tree.links.new(math_node_2.inputs['Value'], math_node_1.outputs['Value'])
				print(len(m.node_tree.links))
				m.node_tree.links.new(math_node_3.inputs[0], math_node_2.outputs['Value']) #math_node_3.inputs['Value']
				print(len(m.node_tree.links))
				m.node_tree.links.new(toon_texture_color_ramp.inputs['Fac'], math_node_3.outputs['Value'])
				print(len(m.node_tree.links))
				m.node_tree.links.new(mix_rgb_node_ramp_overlay.inputs['Color1'], toon_texture_color_ramp.outputs['Color'])
				print(len(m.node_tree.links))
				m.node_tree.links.new(mix_rgb_node_ramp_overlay.inputs['Fac'], toon_texture_color_ramp.outputs['Alpha'])
				print(len(m.node_tree.links))
				m.node_tree.links.new(mix_rgb_node.inputs['Color1'], mix_rgb_node_ramp_overlay.outputs['Color'])

				print(len(m.node_tree.links))
				m.node_tree.links.new(mix_rgb_node_add_sphere.inputs['Color1'], mix_rgb_node.outputs['Color'])
				print(len(m.node_tree.links))
				m.node_tree.links.new(output_node.inputs['Color'], mix_rgb_node_add_sphere.outputs['Color'])
				print(len(m.node_tree.links))
				m.node_tree.links.new(diffuse_texture_node.inputs['Vector'], diffuse_texture_geomety_uv_node.outputs['UV'])
				print(len(m.node_tree.links))
				m.node_tree.links.new(mix_rgb_node.inputs['Color2'], diffuse_texture_node.outputs['Color'])
				print(len(m.node_tree.links))
				m.node_tree.links.new(sphere_texture_node.inputs['Vector'], sphere_texture_geometry_normal_node.outputs['Normal'])
				print(len(m.node_tree.links))
				m.node_tree.links.new(mix_rgb_node_add_sphere.inputs['Color2'],sphere_texture_node.outputs['Color'])





				if m.texture_slots is not None:
					for t in range(len(m.texture_slots)):
						if m.texture_slots[t] is not None:
							texture_name = m.texture_slots[t].texture.name
							if t == 0:
								diffuse_texture_node.texture = bpy.data.textures[texture_name]
								diffuse_exists = True
								# bpy.data.textures[texture_name]["mmd_texture_type"] = "DIFFUSE"
							if t == 1:
								if m.texture_slots[t].texture.type == 'IMAGE':
									if m.texture_slots[t].texture.image is not None:
										#toon_image_bottom_half_to_color_ramp(toon_texture_color_ramp, m.texture_slots[t].texture.image)
										toon_image_to_color_ramp(toon_texture_color_ramp, m.texture_slots[t].texture.image)
									# bpy.data.textures[texture_name]["mmd_texture_type"] = "TOON"
									# bpy.context.active_object.data.materials[0].texture_slots[1].texture.image.name
							if t == 2:
								mix_rgb_node_add_sphere.blend_type = m.texture_slots[t].blend_type
								sphere_texture_node.texture = bpy.data.textures[texture_name]
								sphere_exists = True
								# bpy.data.textures[texture_name]["mmd_texture_type"] = "SPHERE"

				if diffuse_texture_node.texture == None:
					# m.node_tree.links.new(mix_rgb_node.inputs['Color2'], material_node.outputs['Color'])
					# m.use_shadeless = True
					m.node_tree.links.remove(mix_rgb_node.inputs['Color2'].links[0])
					print("This mesh object has no diffuse texture.")




class MMDToonTexturesToNodeEditorShader(bpy.types.Operator):
	"""Sets up nodes in Blender node editor for rendering toon textures"""
	bl_idname = "mmd_tools_helper.mmd_toon_render_node_editor"
	bl_label = "MMD toon textures render using node editor "


	# @classmethod
	# def poll(cls, context):
		# return context.active_object is not None

	def execute(self, context):

		mesh_objects_list = model.find_MMD_MeshesList(bpy.context.active_object)
		assert(mesh_objects_list is not None), "The active object is not an MMD model."
		for o in mesh_objects_list:
			bpy.context.scene.objects.active = o
			clear_material_nodes(context)
			# create_default_material_nodes(context)
			main(context)
		return {'FINISHED'}


def register():
	bpy.utils.register_class(MMDToonTexturesToNodeEditorShader)
	bpy.utils.register_class(MMDToonTexturesToNodeEditorShaderPanel)


def unregister():
	bpy.utils.unregister_class(MMDToonTexturesToNodeEditorShader)
	bpy.utils.unregister_class(MMDToonTexturesToNodeEditorShaderPanel)


if __name__ == "__main__":
	register()


