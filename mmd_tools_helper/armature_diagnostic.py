import bpy

from . import register_wrap
from . import import_csv
from . import model

@register_wrap
class ArmatureDiagnosticPanel(bpy.types.Panel):
	"""Armature Diagnostic panel"""
	bl_label = "Armature Diagnostic Panel"
	bl_idname = "OBJECT_PT_armature_diagnostic"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "mmd_tools_helper"

	def draw(self, context):
		layout = self.layout
		row = layout.row()
		layout.prop(context.scene, "selected_armature_to_diagnose")
		row = layout.row()
		row.label(text="Armature Diagnostic", icon='ARMATURE_DATA')
		row = layout.row()
		row.operator("mmd_tools_helper.armature_diagnostic", text = "Diagnose Armature")
		row = layout.row()
		row = layout.row()


def main(context):
	missing_bone_names = []
	BONE_NAMES_DICTIONARY = import_csv.use_csv_bones_dictionary()
	FINGER_BONE_NAMES_DICTIONARY = import_csv.use_csv_bones_fingers_dictionary()
	SelectedBoneMap = bpy.context.scene.selected_armature_to_diagnose
	BoneMapIndex = BONE_NAMES_DICTIONARY[0].index(SelectedBoneMap)
	FingerBoneMapIndex = FINGER_BONE_NAMES_DICTIONARY[0].index(SelectedBoneMap)
	bpy.context.scene.objects.active = model.findArmature(bpy.context.active_object)
	for b in BONE_NAMES_DICTIONARY:
		if BONE_NAMES_DICTIONARY.index(b) != 0:
			if b[BoneMapIndex] != '':
				if b[BoneMapIndex] not in ["upper body 2", "上半身2"]:
					if b[BoneMapIndex] not in bpy.context.active_object.data.bones.keys():
						missing_bone_names.append(b[BoneMapIndex])
	for b in FINGER_BONE_NAMES_DICTIONARY:
		if FINGER_BONE_NAMES_DICTIONARY.index(b) != 0:
			if b[FingerBoneMapIndex] != '':
				if b[FingerBoneMapIndex] not in ["thumb0_L", "thumb0_R", "左親指0", "親指0.L", "右親指0", "親指0.R"]:
					if b[FingerBoneMapIndex] not in bpy.context.active_object.data.bones.keys():
						missing_bone_names.append(b[FingerBoneMapIndex])
	print("\nSelected diagnostic bone map is:")
	print(SelectedBoneMap)
	print("These bone names of", SelectedBoneMap, "are missing from the active armature:" )
	print(missing_bone_names)
	if SelectedBoneMap == 'mmd_english':
		print("Please note that these 3 bones are MMD semi-standard bones and are not essential in an MMD armature:")
		print("upper body 2, thumb0_L, thumb0_R")

@register_wrap
class ArmatureDiagnostic(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "mmd_tools_helper.armature_diagnostic"
	bl_label = "Armature Diagnostic"

	bpy.types.Scene.selected_armature_to_diagnose = bpy.props.EnumProperty(items = [('mmd_english', 'MMD English bone names', 'MikuMikuDance English bone names'), ('mmd_japanese', 'MMD Japanese bone names', 'MikuMikuDamce Japanese bone names'), ('mmd_japaneseLR', 'MMD Japanese bones names .L.R suffixes', 'MikuMikuDamce Japanese bones names with .L.R suffixes'), ('xna_lara', 'XNALara bone names', 'XNALara bone names'), ('daz_poser', 'DAZ/Poser bone names', 'DAZ/Poser bone names'), ('blender_rigify', 'Blender rigify bone names', 'Blender rigify bone names before generating the complete rig'), ('sims_2', 'Sims 2 bone names', 'Sims 2 bone names'), ('motion_builder', 'Motion Builder bone names', 'Motion Builder bone names'), ('3ds_max', '3ds Max bone names', '3ds Max bone names'), ('bepu', 'Bepu full body IK bone names', 'Bepu full body IK bone names'), ('project_mirai', 'Project Mirai bone names', 'Project Mirai bone names'), ('manuel_bastioni_lab', 'Manuel Bastioni Lab bone names', 'Manuel Bastioni Lab bone names'), ('makehuman_mhx', 'Makehuman MHX bone names', 'Makehuman MHX bone names'), ('sims_3', 'Sims 3 bone names', 'Sims 3 bone names'), ('doa5lr', 'DOA5LR bone names', 'Dead on Arrival 5 Last Round bone names'), ('Bip_001', 'Bip001 bone names', 'Bip001 bone names'), ('biped_3ds_max', 'Biped 3DS Max bone names', 'Biped 3DS Max bone names'), ('biped_sfm', 'Biped Source Film Maker bone names', 'Biped Source Film Maker bone names'), ('valvebiped', 'ValveBiped bone names', 'ValveBiped bone names'), ('iClone7', 'iClone7 bone names', 'iClone7 bone names') ], name = "Armature Type :", default = 'mmd_english')

	@classmethod
	def poll(cls, context):
		return context.active_object is not None

	def execute(self, context):
		bpy.context.scene.objects.active = model.findArmature(bpy.context.active_object)
		print()
		print()
		print(bpy.context.active_object.name, "all bone names")
		print([b for b in bpy.context.active_object.data.bones.keys() if 'dummy' not in b and 'shadow' not in b])
		print()
		main(context)
		return {'FINISHED'}
