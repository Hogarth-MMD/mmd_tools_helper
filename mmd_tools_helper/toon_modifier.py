import bpy
from . import model

 # blend_type
	# Type:	enum in ["MIX", "ADD", "MULTIPLY", "SUBTRACT", "SCREEN", "DIVIDE", "DIFFERENCE", "DARKEN", "LIGHTEN", "OVERLAY", "DODGE", "BURN", "HUE", "SATURATION", "VALUE", "COLOR", "SOFT_LIGHT", "LINEAR_LIGHT"], default ‘MIX’

class MMDToonModifierPanel(bpy.types.Panel):
	"""User can modify the rendering of toon texture color"""
	bl_idname = "OBJECT_PT_mmd_toon_modifier"
	bl_label = "MMD toon modifier"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"
	bl_category = "mmd_tools_helper"

	def draw(self, context):
		layout = self.layout
		row = layout.row()

		row.label(text="MMD Toon modifier", icon="MATERIAL")
		layout.prop(context.scene, "ToonModifierBlendType")
		row = layout.row()
		layout.prop(context.scene, "ToonModifierColor")
		row = layout.row()
		row.operator("mmd_tools_helper.toon_modifier", text = "Modify Toon")

def main(context):
	mesh_objects_list = model.find_MMD_MeshesList(bpy.context.active_object)
	# print("mesh_objects_list = ", mesh_objects_list)
	assert(mesh_objects_list is not None), "The active object is not an MMD model."
	for o in mesh_objects_list:
		bpy.context.scene.objects.active = o
		for m in bpy.context.active_object.data.materials:
			for n in m.node_tree.nodes:
				if n.label == "toon_modifier":
					n.inputs['Color2'].default_value[0] = bpy.context.scene.ToonModifierColor[0]
					n.inputs['Color2'].default_value[1] = bpy.context.scene.ToonModifierColor[1]
					n.inputs['Color2'].default_value[2] = bpy.context.scene.ToonModifierColor[2]
					n.blend_type = bpy.context.scene.ToonModifierBlendType



class MMDToonModifier(bpy.types.Operator):
	"""User can modify the rendering of toon texture color"""
	bl_idname = "mmd_tools_helper.toon_modifier"
	bl_label = "MMD toon modifier"

	bpy.types.Scene.ToonModifierColor = bpy.props.FloatVectorProperty(name="Toon Modifer Color", description="toon modifer color", default=(1.0, 1.0, 1.0), min=0.0, max=1.0, soft_min=0.0, soft_max=1.0, step=3, precision=2, options={'ANIMATABLE'}, subtype='COLOR', unit='NONE', size=3, update=None, get=None, set=None)

	bpy.types.Scene.ToonModifierBlendType = bpy.props.EnumProperty(items = [('MIX', 'MIX', 'MIX'), ('ADD', 'ADD', 'ADD'), ('MULTIPLY', 'MULTIPLY', 'MULTIPLY'), ('SUBTRACT', 'SUBTRACT', 'SUBTRACT'), ('SCREEN', 'SCREEN', 'SCREEN'), ('DIVIDE', 'DIVIDE', 'DIVIDE'), ('DIFFERENCE', 'DIFFERENCE', 'DIFFERENCE'), ('DARKEN', 'DARKEN', 'DARKEN'), ('LIGHTEN', 'LIGHTEN', 'LIGHTEN'), ('OVERLAY', 'OVERLAY', 'OVERLAY'), ('DODGE', 'DODGE', 'DODGE'), ('BURN', 'BURN', 'BURN'), ('HUE', 'HUE', 'HUE'), ('SATURATION', 'SATURATION', 'SATURATION'), ('VALUE', 'VALUE', 'VALUE'), ('COLOR', 'COLOR', 'COLOR'), ('SOFT_LIGHT', 'SOFT_LIGHT', 'SOFT_LIGHT'), ('LINEAR_LIGHT', 'LINEAR_LIGHT', 'LINEAR_LIGHT')], name = "Toon Modifier Blend Type", default = 'MULTIPLY')

	# @classmethod
	# def poll(cls, context):
		# return context.active_object is not None

	def execute(self, context):
		main(context)
		return {'FINISHED'}


def register():
	bpy.utils.register_class(MMDToonModifier)
	bpy.utils.register_class(MMDToonModifierPanel)


def unregister():
	bpy.utils.unregister_class(MMDToonModifier)
	bpy.utils.unregister_class(MMDToonModifierPanel)


if __name__ == "__main__":
	register()