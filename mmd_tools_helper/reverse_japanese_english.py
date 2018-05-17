import bpy

class ReverseJapaneseEnglishPanel(bpy.types.Panel):
	"""Sets up nodes in Blender node editor for rendering toon textures"""
	bl_idname = "OBJECT_PT_reverse_japanese_english"
	bl_label = "Reverse Japanese English names"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"
	bl_category = "mmd_tools_helper"

	def draw(self, context):
		layout = self.layout
		row = layout.row()

		row.label(text="Reverse Japanese English names", icon="TEXT")
		row = layout.row()
		row.operator("mmd_tools_helper.reverse_japanese_english", text = "Reverse Japanese English names")
		row = layout.row()

def main(context):
	for m in bpy.data.materials:
		name_j = m.mmd_material.name_j
		name_e = m.mmd_material.name_e
		if name_e != '':
			m.mmd_material.name_e = name_j
			m.mmd_material.name_j = name_e
			m.mmd_material.name = name_e

	for m in bpy.data.materials:
		m.name = m.mmd_material.name


	for o in bpy.context.scene.objects:
		if o.type == 'ARMATURE':
			o.data.show_names = True
			bpy.context.scene.objects.active = o
			bpy.ops.object.mode_set(mode='POSE')
			for b in bpy.context.active_object.pose.bones:
				name_j = b.mmd_bone.name_j
				name_e = b.mmd_bone.name_e
				if name_e != '':
					b.mmd_bone.name_j = name_e
					b.mmd_bone.name_e = name_j
					b.name = name_e

	bpy.ops.object.mode_set(mode='OBJECT')

	for o in bpy.context.scene.objects:
		if o.mmd_type == 'ROOT':
			for vm in o.mmd_root.vertex_morphs:
				name_j = vm.name
				name_e = vm.name_e
				if name_e != '':
					vm.name = name_e
					vm.name_e = name_j


class ReverseJapaneseEnglish(bpy.types.Operator):
	"""Reverses Japanese and English names of shape keys, materials, bones"""
	bl_idname = "mmd_tools_helper.reverse_japanese_english"
	bl_label = "Reverse Japanese English names of MMD model"

	def execute(self, context):
		main(context)
		return {'FINISHED'}

def register():
	bpy.utils.register_class(ReverseJapaneseEnglish)
	bpy.utils.register_class(ReverseJapaneseEnglishPanel)


def unregister():
	bpy.utils.unregister_class(ReverseJapaneseEnglishShader)
	bpy.utils.unregister_class(ReverseJapaneseEnglishShaderPanel)


if __name__ == "__main__":
	register()