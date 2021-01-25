bl_info = {
	"name": "MMD tools helper",
	"author": "Hogarth-MMD",
	"version": (2, 4),
	"blender": (2, 79, 0),
	"location": "View3D > Tool Shelf > MMD Tools Helper",
	"description": "various mmd_tools helper scripts",
	"warning": "",
	"wiki_url": "",
	"category": "Object",
	}

import bpy

class MMDToolsHelperPanel(bpy.types.Panel):
	"""Creates the MMD Tools Helper Panel in a VIEW_3D TOOLS tab"""
	bl_label = "MMD Tools Helper"
	bl_idname = "OBJECT_PT_mmd_tools_helper"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"
	bl_category = "mmd_tools_helper"

	def draw(self, context):
		layout = self.layout
		row = layout.row()

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


import imp
imp.reload(model)
imp.reload(mmd_view)
imp.reload(mmd_lamp_setup)
imp.reload(convert_to_blender_camera)
imp.reload(background_color_picker)
imp.reload(boneMaps_renamer)
imp.reload(replace_bones_renaming)
imp.reload(armature_diagnostic)
imp.reload(add_foot_leg_ik)
imp.reload(add_hand_arm_ik)
imp.reload(display_panel_groups)
imp.reload(toon_textures_to_node_editor_shader)
imp.reload(toon_modifier)
imp.reload(reverse_japanese_english)
imp.reload(miscellaneous_tools)
imp.reload(blender_bone_names_to_japanese_bone_names)



def register():
	bpy.utils.register_module(__name__)


def unregister():
	bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
	register()
