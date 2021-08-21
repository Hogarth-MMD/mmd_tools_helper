

import bpy

from . import register_wrap
from . import model
from . import import_csv

@register_wrap
class BonesRenamerPanel_MTH(bpy.types.Panel):
	"""Creates the Bones Renamer Panel in a VIEW_3D TOOLS tab"""
	bl_label = "Bones Renamer"
	bl_idname = "OBJECT_PT_bones_renamer_MTH"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "mmd_tools_helper"

	def draw(self, context):
		layout = self.layout
		row = layout.row()

		row.label(text="Mass Rename Bones", icon="ARMATURE_DATA")
		row = layout.row()
		row = layout.row()
		layout.prop(context.scene, "Origin_Armature_Type")
		row = layout.row()
		layout.prop(context.scene, "Destination_Armature_Type")
		row = layout.row()
		row.operator("object.bones_renamer", text = "Mass Rename Bones")
		row = layout.row()



#use international fonts and display the names of the bones
def use_international_fonts_display_names_bones():
	bpy.context.user_preferences.system.use_international_fonts = True
	bpy.context.object.data.show_names = True


def unhide_all_armatures():
	for o in bpy.context.scene.objects:
		if o.type == 'ARMATURE':
			o.hide = False

def print_missing_bone_names():
	missing_bone_names = []
	BONE_NAMES_DICTIONARY = import_csv.use_csv_bones_dictionary()
	FINGER_BONE_NAMES_DICTIONARY = import_csv.use_csv_bones_fingers_dictionary()
	SelectedBoneMap = bpy.context.scene.Destination_Armature_Type
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
	print("\nBones renaming destination bone map was:")
	print(SelectedBoneMap)
	print("These bone names of" , SelectedBoneMap, "are missing from the active armature:" )
	print(missing_bone_names)



def rename_bones(boneMap1, boneMap2, BONE_NAMES_DICTIONARY): 
	boneMaps = BONE_NAMES_DICTIONARY[0]
	boneMap1_index = boneMaps.index(boneMap1)
	boneMap2_index = boneMaps.index(boneMap2)
	bpy.ops.object.mode_set(mode='OBJECT')

	for k in BONE_NAMES_DICTIONARY[1:]:
		if k[boneMap1_index] in bpy.context.active_object.data.bones.keys():
			if k[boneMap2_index] != '':
				bpy.context.active_object.data.bones[k[boneMap1_index]].name = k[boneMap2_index]
				if boneMap2 == 'mmd_japanese' or boneMap2 == 'mmd_japaneseLR':
					bpy.ops.object.mode_set(mode='POSE')
					if hasattr(bpy.context.active_object.pose.bones[k[boneMap2_index]] , "mmd_bone"):
						bpy.context.active_object.pose.bones[k[boneMap2_index]].mmd_bone.name_e = k[0]
					bpy.ops.object.mode_set(mode='OBJECT')



def rename_finger_bones(boneMap1, boneMap2, FINGER_BONE_NAMES_DICTIONARY):
	boneMaps = FINGER_BONE_NAMES_DICTIONARY[0]
	boneMap1_index = boneMaps.index(boneMap1)
	boneMap2_index = boneMaps.index(boneMap2)
	bpy.ops.object.mode_set(mode='OBJECT')

	for k in FINGER_BONE_NAMES_DICTIONARY[1:]:
		if k[boneMap1_index] in bpy.context.active_object.data.bones.keys():
			if k[boneMap2_index] != '':
				bpy.context.active_object.data.bones[k[boneMap1_index]].name = k[boneMap2_index]
				if boneMap2 == 'mmd_japanese' or boneMap2 == 'mmd_japaneseLR':
					bpy.ops.object.mode_set(mode='POSE')
					if hasattr(bpy.context.active_object.pose.bones[k[boneMap2_index]] , "mmd_bone"):
						bpy.context.active_object.pose.bones[k[boneMap2_index]].mmd_bone.name_e = k[0]
					bpy.ops.object.mode_set(mode='OBJECT')

	bpy.context.scene.Origin_Armature_Type = boneMap2
	print_missing_bone_names()


def main(context):
	bpy.context.scene.objects.active = model.findArmature(bpy.context.active_object)

	use_international_fonts_display_names_bones()
	unhide_all_armatures()
	BONE_NAMES_DICTIONARY = import_csv.use_csv_bones_dictionary()
	FINGER_BONE_NAMES_DICTIONARY = import_csv.use_csv_bones_fingers_dictionary()
	rename_bones(bpy.context.scene.Origin_Armature_Type, bpy.context.scene.Destination_Armature_Type, BONE_NAMES_DICTIONARY)
	rename_finger_bones(bpy.context.scene.Origin_Armature_Type, bpy.context.scene.Destination_Armature_Type, FINGER_BONE_NAMES_DICTIONARY)
	bpy.ops.object.mode_set(mode='POSE')
	bpy.ops.pose.select_all(action='SELECT')


@register_wrap
class BonesRenamer(bpy.types.Operator):
	"""Mass bones renamer for armature conversion"""
	bl_idname = "object.bones_renamer"
	bl_label = "Bones Renamer"

	bpy.types.Scene.Origin_Armature_Type = bpy.props.EnumProperty(items = [('mmd_english', 'MMD English bone names', 'MikuMikuDance English bone names'), ('mmd_japanese', 'MMD Japanese bone names', 'MikuMikuDamce Japanese bone names'), ('mmd_japaneseLR', 'MMD Japanese bones names .L.R suffixes', 'MikuMikuDamce Japanese bones names with .L.R suffixes'), ('xna_lara', 'XNALara bone names', 'XNALara bone names'), ('daz_poser', 'DAZ/Poser bone names', 'DAZ/Poser/Second Life bone names'), ('blender_rigify', 'Blender rigify bone names', 'Blender rigify bone names before generating the complete rig'), ('sims_2', 'Sims 2 bone names', 'Sims 2 bone names'), ('motion_builder', 'Motion Builder bone names', 'Motion Builder bone names'), ('3ds_max', '3ds Max bone names', '3ds Max bone names'), ('bepu', 'Bepu full body IK bone names', 'Bepu full body IK bone names'), ('project_mirai', 'Project Mirai bone names', 'Project Mirai bone names'), ('manuel_bastioni_lab', 'Manuel Bastioni Lab bone names', 'Manuel Bastioni Lab bone names'), ('makehuman_mhx', 'Makehuman MHX bone names', 'Makehuman MHX bone names'), ('sims_3', 'Sims 3 bone names', 'Sims 3 bone names'), ('doa5lr', 'DOA5LR bone names', 'Dead on Arrival 5 Last Round bone names'), ('Bip_001', 'Bip001 bone names', 'Bip001 bone names'), ('biped_3ds_max', 'Biped 3DS Max bone names', 'Biped 3DS Max bone names'), ('biped_sfm', 'Biped Source Film Maker bone names', 'Biped Source Film Maker bone names'), ('valvebiped', 'ValveBiped bone names', 'ValveBiped bone names'), ('iClone7', 'iClone7 bone names', 'iClone7 bone names')], name = "Rename  bones  from :", default = 'mmd_japanese')


	bpy.types.Scene.Destination_Armature_Type = bpy.props.EnumProperty(items = [('mmd_english', 'MMD English bone names', 'MikuMikuDance English bone names'), ('mmd_japanese', 'MMD Japanese bone names', 'MikuMikuDamce Japanese bone names'), ('mmd_japaneseLR', 'MMD Japanese bones names .L.R suffixes', 'MikuMikuDamce Japanese bones names with .L.R suffixes'), ('xna_lara', 'XNALara bone names', 'XNALara bone names'), ('daz_poser', 'DAZ/Poser bone names', 'DAZ/Poser/Second Life bone names'), ('blender_rigify', 'Blender rigify bone names', 'Blender rigify bone names before generating the complete rig'), ('sims_2', 'Sims 2 bone names', 'Sims 2 bone names'), ('motion_builder', 'Motion Builder bone names', 'Motion Builder bone names'), ('3ds_max', '3ds Max bone names', '3ds Max bone names'), ('bepu', 'Bepu full body IK bone names', 'Bepu full body IK bone names'), ('project_mirai', 'Project Mirai bone names', 'Project Mirai bone names'), ('manuel_bastioni_lab', 'Manuel Bastioni Lab bone names', 'Manuel Bastioni Lab bone names'), ('makehuman_mhx', 'Makehuman MHX bone names', 'Makehuman MHX bone names'), ('sims_3', 'Sims 3 bone names', 'Sims 3 bone names'), ('doa5lr', 'DOA5LR bone names', 'Dead on Arrival 5 Last Round bone names'), ('Bip_001', "Bip001 bone names", 'Bip001 bone names'), ('biped_3ds_max', 'Biped 3DS Max bone names', 'Biped 3DS Max bone names'), ('biped_sfm', 'Biped Source Film Maker bone names', 'Biped Source Film Maker bone names'), ('valvebiped', 'ValveBiped bone names', 'ValveBiped bone names'), ('iClone7', 'iClone7 bone names', 'iClone7 bone names')], name = "Rename  bones  to :", default = 'mmd_english')

	#@classmethod
	#def poll(cls, context):
		#return context.active_object.type == 'ARMATURE'
		#return context.active_object is not None

	def execute(self, context):
		main(context)
		return {'FINISHED'}
