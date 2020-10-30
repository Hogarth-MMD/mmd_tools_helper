import bpy
import math
from . import model

# def armature_diagnostic():
	# ENGLISH_LEG_BONES = ["knee_L", "knee_R", "ankle_L", "ankle_R", "toe_L", "toe_R"]
	# JAPANESE_LEG_BONES = ["左ひざ", "右ひざ", "左足首", "右足首", "左つま先", "右つま先"]
	# IK_BONE_NAMES = ["leg IK_L", "leg IK_R", "toe IK_L", "toe IK_R", "左足ＩＫ", "右足ＩＫ", "左つま先ＩＫ", "右つま先ＩＫ"]
	# ENGLISH_OK = True
	# JAPANESE_OK = True

	# print('\n\n\n', 'These English bones are needed to add IK:', '\n')
	# print(ENGLISH_LEG_BONES, '\n')
	# for b in ENGLISH_LEG_BONES:
		# if b not in bpy.context.active_object.data.bones.keys():
			# ENGLISH_OK = False
			# print('This bone is not in this armature:', '\n', b)
	# if ENGLISH_OK == True:
		# print('OK! All English-named bones are present which are needed to add leg IK')

	# print('\n', 'OR These Japanese bones are needed to add IK:', '\n')
	# print(JAPANESE_LEG_BONES, '\n')
	# for b in JAPANESE_LEG_BONES:
		# if b not in bpy.context.active_object.data.bones.keys():
			# JAPANESE_OK = False
			# print('This bone is not in this armature:', '\n', b)
	# if JAPANESE_OK == True:
		# print('OK! All Japanese-named bones are present which are needed to add leg IK', '\n')

	# print('\n', 'IK bone names', '\n')
	# for b in IK_BONE_NAMES:
		# if b in bpy.context.active_object.data.bones.keys():
			# print('This armature appears to already have IK bones. This bone seems to be an IK bone:', '\n', b)

class Add_MMD_foot_leg_IK_Panel(bpy.types.Panel):
	"""Add foot and leg IK bones and constraints to MMD model"""
	bl_idname = "OBJECT_PT_mmd_add_foot_leg_ik"
	bl_label = "Add foot leg IK to MMD model"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"
	bl_category = "mmd_tools_helper"

	def draw(self, context):
		layout = self.layout
		row = layout.row()

		row.label(text="Add leg and foot IK to MMD model", icon="ARMATURE_DATA")
		row = layout.row()
		row.operator("object.add_foot_leg_ik", text = "Add leg and foot IK to MMD model")
		row = layout.row()
		row = layout.row()

def clear_IK(context):
	IK_target_bones = []
	IK_target_tip_bones = []
	bpy.context.scene.objects.active = model.findArmature(bpy.context.active_object)
	bpy.ops.object.mode_set(mode='POSE')
	english = ["knee_L", "knee_R", "ankle_L", "ankle_R", "toe_L", "toe_R"]
	japanese = ["左ひざ", "右ひざ", "左足首", "右足首", "左つま先", "右つま先"]
	japanese_L_R = ["ひざ.L", "ひざ.R", "足首.L", "足首.R", "つま先.L", "つま先.R"]
	leg_foot_bones = english + japanese + japanese_L_R
	for b in bpy.context.active_object.pose.bones.keys():
		if b in leg_foot_bones:
			for c in bpy.context.active_object.pose.bones[b].constraints:
				if c.type == "IK":
					print("c.target = ", c.target)
					if c.target == bpy.context.scene.objects.active:
						if c.subtarget is not None:
							print("c.subtarget = ", c.subtarget)
							if c.subtarget not in IK_target_bones:
								IK_target_bones.append(c.subtarget)
	for b in IK_target_bones:
		for c in bpy.context.active_object.pose.bones[b].children:
			if c.name not in IK_target_tip_bones:
				IK_target_tip_bones.append(c.name)
	bones_to_be_deleted = set(IK_target_bones + IK_target_tip_bones)
	print("bones to be deleted = ", bones_to_be_deleted)
	bpy.ops.object.mode_set(mode='EDIT')
	for b in bones_to_be_deleted:
		bpy.context.active_object.data.edit_bones.remove(bpy.context.active_object.data.edit_bones[b])
	bpy.ops.object.mode_set(mode='POSE')
	for b in bpy.context.active_object.pose.bones.keys():
		if b in leg_foot_bones:
			for c in bpy.context.active_object.pose.bones[b].constraints:
				bpy.context.active_object.pose.bones[b].constraints.remove(c)
				# if c.type == "IK":
					# bpy.context.active_object.pose.bones[b].constraints.remove(c)
				# if c.type == "LIMIT_ROTATION":
					# bpy.context.active_object.pose.bones[b].constraints.remove(c)

	bpy.ops.object.mode_set(mode='OBJECT')


def main(context):
	bpy.context.scene.objects.active = model.findArmature(bpy.context.active_object)

	#test japanese or english ("leg_R", "右足"), ("leg_L", "左足"),
	english = ["knee_L", "knee_R", "ankle_L", "ankle_R", "toe_L", "toe_R"]
	japanese = ["左ひざ", "右ひざ", "左足首", "右足首", "左つま先", "右つま先"] 
	japanese_L_R = ["ひざ.L", "ひざ.R", "足首.L", "足首.R", "つま先.L", "つま先.R"]

	keys = bpy.context.active_object.data.bones.keys()

	english_bones = all([e in keys for e in english])
	japanese_bones = all([j in keys for j in japanese])
	japanese_bones_L_R = all([j in keys for j in japanese_L_R])

	print('english_bones =', english_bones)
	print('japanese_bones =', japanese_bones)
	print('japanese_bones_L_R =', japanese_bones_L_R)
	print('\n\n')

	assert(english_bones == True or japanese_bones == True or japanese_bones_L_R == True), "This is not an MMD armature. MMD bone names of knee, ankle and toe bones are required for this script to run."

	IK_BONE_NAMES = ["leg IK_L", "leg IK_R", "toe IK_L", "toe IK_R", "左足ＩＫ", "右足ＩＫ", "左つま先ＩＫ", "右つま先ＩＫ", "足ＩＫ.L", "足ＩＫ.R", "つま先ＩＫ.L", "つま先ＩＫ.R"]
	ik_bones = any([ik in keys for ik in IK_BONE_NAMES])

	assert(ik_bones == False), "This armature already has MMD IK bone names."


	if english_bones == True:
		LEG_IK_LEFT_BONE = "leg IK_L"
		LEG_IK_RIGHT_BONE = "leg IK_R"
		TOE_IK_LEFT_BONE = "toe IK_L"
		TOE_IK_RIGHT_BONE = "toe IK_R"
		LEG_IK_LEFT_BONE_TIP = "leg IK_L_t"
		LEG_IK_RIGHT_BONE_TIP = "leg IK_R_t"
		TOE_IK_LEFT_BONE_TIP = "toe IK_L_t"
		TOE_IK_RIGHT_BONE_TIP = "toe IK_R_t"
		ROOT = "root"


	if japanese_bones == True or japanese_bones_L_R == True:
		LEG_IK_LEFT_BONE = "左足ＩＫ"
		LEG_IK_RIGHT_BONE = "右足ＩＫ"
		TOE_IK_LEFT_BONE = "左つま先ＩＫ"
		TOE_IK_RIGHT_BONE = "右つま先ＩＫ"
		LEG_IK_LEFT_BONE_TIP = "左足ＩＫ先"
		LEG_IK_RIGHT_BONE_TIP = "右足ＩＫ先"
		TOE_IK_LEFT_BONE_TIP = "左つま先ＩＫ先"
		TOE_IK_RIGHT_BONE_TIP = "右つま先ＩＫ先"
		ROOT = "全ての親"

		#Lists of possible names of knee, ankle and toe bones
	KNEE_LEFT_BONES = ["knee_L", "左ひざ", "ひざ.L" ]
	KNEE_RIGHT_BONES = ["knee_R", "右ひざ", "ひざ.R"]
	ANKLE_LEFT_BONES = ["ankle_L", "左足首", "足首.L"]
	ANKLE_RIGHT_BONES = ["ankle_R", "右足首", "足首.R"]
	TOE_LEFT_BONES = ["toe_L", "左つま先", "つま先.L"]
	TOE_RIGHT_BONES = ["toe_R", "右つま先", "つま先.R"]

	print('\n')
	#Searches through the bones of the active armature and finds the knee, ankle and toe bones.
	for b in bpy.context.active_object.data.bones:
		if b.name in KNEE_LEFT_BONES:
			KNEE_LEFT = b.name
			print('KNEE_LEFT = ', KNEE_LEFT)
		if b.name in KNEE_RIGHT_BONES:
			KNEE_RIGHT = b.name
			print('KNEE_RIGHT = ', KNEE_RIGHT)
		if b.name in ANKLE_LEFT_BONES:
			ANKLE_LEFT = b.name
			print('ANKLE_LEFT = ', ANKLE_LEFT)
		if b.name in ANKLE_RIGHT_BONES:
			ANKLE_RIGHT = b.name
			print('ANKLE_RIGHT = ', ANKLE_RIGHT)
		if b.name in TOE_LEFT_BONES:
			TOE_LEFT = b.name
			print('TOE_LEFT = ', TOE_LEFT)
		if b.name in TOE_RIGHT_BONES:
			TOE_RIGHT = b.name
			print('TOE_RIGHT = ', TOE_RIGHT)

	bpy.ops.object.mode_set(mode='POSE')
	bpy.context.active_object.pose.bones[KNEE_LEFT].use_ik_limit_x = True
	bpy.context.active_object.pose.bones[KNEE_RIGHT].use_ik_limit_x = True

	#measurements of the length of the foot bone which will used to calculate the lengths of the IK bones.
	LENGTH_OF_FOOT_BONE = bpy.context.active_object.data.bones[ANKLE_LEFT].length
	HALF_LENGTH_OF_FOOT_BONE = bpy.context.active_object.data.bones[ANKLE_LEFT].length * 0.5
	TWENTIETH_LENGTH_OF_FOOT_BONE = bpy.context.active_object.data.bones[ANKLE_LEFT].length * 0.05

	bpy.ops.object.mode_set(mode='EDIT')

	#The IK bones are created
	bone = bpy.context.active_object.data.edit_bones.new(LEG_IK_LEFT_BONE)
	bone.head = bpy.context.active_object.data.edit_bones[ANKLE_LEFT].head
	bone.tail = bpy.context.active_object.data.edit_bones[ANKLE_LEFT].head
	bone.tail.y = bpy.context.active_object.data.edit_bones[ANKLE_LEFT].head.y + LENGTH_OF_FOOT_BONE
	if ROOT in bpy.context.active_object.data.edit_bones.keys():
		print(ROOT, ROOT in bpy.context.active_object.data.edit_bones.keys())
		bone.parent = bpy.context.active_object.data.edit_bones[ROOT]
		print(bone, bone.parent)


	bone = bpy.context.active_object.data.edit_bones.new(LEG_IK_RIGHT_BONE)
	bone.head = bpy.context.active_object.data.edit_bones[ANKLE_RIGHT].head
	bone.tail = bpy.context.active_object.data.edit_bones[ANKLE_RIGHT].head
	bone.tail.y = bpy.context.active_object.data.edit_bones[ANKLE_RIGHT].head.y + LENGTH_OF_FOOT_BONE
	if ROOT in bpy.context.active_object.data.edit_bones.keys():
		print(ROOT, ROOT in bpy.context.active_object.data.edit_bones.keys())
		bone.parent = bpy.context.active_object.data.edit_bones[ROOT]
		print(bone, bone.parent)


	bone = bpy.context.active_object.data.edit_bones.new(TOE_IK_LEFT_BONE)
	bone.head = bpy.context.active_object.data.edit_bones[TOE_LEFT].head
	bone.tail = bpy.context.active_object.data.edit_bones[TOE_LEFT].head
	bone.tail.z = bpy.context.active_object.data.edit_bones[TOE_LEFT].head.z - HALF_LENGTH_OF_FOOT_BONE
	print('bone = ', bone)
	bone.parent = bpy.context.active_object.data.edit_bones[LEG_IK_LEFT_BONE]
	bone.use_connect = False

	bone = bpy.context.active_object.data.edit_bones.new(TOE_IK_RIGHT_BONE)
	bone.head = bpy.context.active_object.data.edit_bones[TOE_RIGHT].head
	bone.tail = bpy.context.active_object.data.edit_bones[TOE_RIGHT].head
	bone.tail.z = bpy.context.active_object.data.edit_bones[TOE_RIGHT].head.z - HALF_LENGTH_OF_FOOT_BONE
	bone.parent = bpy.context.active_object.data.edit_bones[LEG_IK_RIGHT_BONE]
	bone.use_connect = False

	bone = bpy.context.active_object.data.edit_bones.new(LEG_IK_LEFT_BONE_TIP)
	bone.head = bpy.context.active_object.data.edit_bones[LEG_IK_LEFT_BONE].head
	bone.tail = bpy.context.active_object.data.edit_bones[LEG_IK_LEFT_BONE].head
	bone.tail.y = bone.tail.y + TWENTIETH_LENGTH_OF_FOOT_BONE
	bone.parent = bpy.context.active_object.data.edit_bones[LEG_IK_LEFT_BONE]
	bone.use_connect = False
	bpy.ops.object.mode_set(mode='POSE')
	#if "leg IK_L_t" in bpy.context.active_object.pose.bones.keys():
	bpy.context.active_object.pose.bones[LEG_IK_LEFT_BONE_TIP].bone.hide = True
	if hasattr(bpy.context.active_object.pose.bones[LEG_IK_LEFT_BONE_TIP], "mmd_bone"):
		bpy.context.active_object.pose.bones[LEG_IK_LEFT_BONE_TIP].mmd_bone.is_visible = False
		bpy.context.active_object.pose.bones[LEG_IK_LEFT_BONE_TIP].mmd_bone.is_controllable = False
		bpy.context.active_object.pose.bones[LEG_IK_LEFT_BONE_TIP].mmd_bone.is_tip = True
	bpy.ops.object.mode_set(mode='EDIT')

	bone = bpy.context.active_object.data.edit_bones.new(LEG_IK_RIGHT_BONE_TIP)
	bone.head = bpy.context.active_object.data.edit_bones[LEG_IK_RIGHT_BONE].head
	bone.tail = bpy.context.active_object.data.edit_bones[LEG_IK_RIGHT_BONE].head
	bone.tail.y = bone.tail.y + TWENTIETH_LENGTH_OF_FOOT_BONE
	bone.parent = bpy.context.active_object.data.edit_bones[LEG_IK_RIGHT_BONE]
	bone.use_connect = False
	bpy.ops.object.mode_set(mode='POSE')
	#if "leg IK_R_t" in bpy.context.active_object.pose.bones.keys():
	bpy.context.active_object.pose.bones[LEG_IK_RIGHT_BONE_TIP].bone.hide = True
	if hasattr(bpy.context.active_object.pose.bones[LEG_IK_RIGHT_BONE_TIP], "mmd_bone"):
		bpy.context.active_object.pose.bones[LEG_IK_RIGHT_BONE_TIP].mmd_bone.is_visible = False
		bpy.context.active_object.pose.bones[LEG_IK_RIGHT_BONE_TIP].mmd_bone.is_controllable = False
		bpy.context.active_object.pose.bones[LEG_IK_RIGHT_BONE_TIP].mmd_bone.is_tip = True
	bpy.ops.object.mode_set(mode='EDIT')

	bone = bpy.context.active_object.data.edit_bones.new(TOE_IK_LEFT_BONE_TIP)
	bone.head = bpy.context.active_object.data.edit_bones[TOE_IK_LEFT_BONE].head
	bone.tail = bpy.context.active_object.data.edit_bones[TOE_IK_LEFT_BONE].head
	bone.tail.z = bone.tail.z - TWENTIETH_LENGTH_OF_FOOT_BONE
	bone.parent = bpy.context.active_object.data.edit_bones[TOE_IK_LEFT_BONE]
	bone.use_connect = False
	bpy.ops.object.mode_set(mode='POSE')
	#if "toe IK_L_t" in bpy.context.active_object.pose.bones.keys():
	bpy.context.active_object.pose.bones[TOE_IK_LEFT_BONE_TIP].bone.hide = True
	if hasattr(bpy.context.active_object.pose.bones[TOE_IK_LEFT_BONE_TIP], "mmd_bone"):
		bpy.context.active_object.pose.bones[TOE_IK_LEFT_BONE_TIP].mmd_bone.is_visible = False
		bpy.context.active_object.pose.bones[TOE_IK_LEFT_BONE_TIP].mmd_bone.is_controllable = False
		bpy.context.active_object.pose.bones[TOE_IK_LEFT_BONE_TIP].mmd_bone.is_tip = True
	bpy.ops.object.mode_set(mode='EDIT')

	bone = bpy.context.active_object.data.edit_bones.new(TOE_IK_RIGHT_BONE_TIP)
	bone.head = bpy.context.active_object.data.edit_bones[TOE_IK_RIGHT_BONE].head
	bone.tail = bpy.context.active_object.data.edit_bones[TOE_IK_RIGHT_BONE].head
	bone.tail.z = bone.tail.z - TWENTIETH_LENGTH_OF_FOOT_BONE
	bone.parent = bpy.context.active_object.data.edit_bones[TOE_IK_RIGHT_BONE]
	bone.use_connect = False
	bpy.ops.object.mode_set(mode='POSE')
	#if "toe IK_R_t" in bpy.context.active_object.pose.bones.keys():
	bpy.context.active_object.pose.bones[TOE_IK_RIGHT_BONE_TIP].bone.hide = True
	if hasattr(bpy.context.active_object.pose.bones[TOE_IK_RIGHT_BONE_TIP], "mmd_bone"):
		bpy.context.active_object.pose.bones[TOE_IK_RIGHT_BONE_TIP].mmd_bone.is_visible = False
		bpy.context.active_object.pose.bones[TOE_IK_RIGHT_BONE_TIP].mmd_bone.is_controllable = False
		bpy.context.active_object.pose.bones[TOE_IK_RIGHT_BONE_TIP].mmd_bone.is_tip = True
	bpy.ops.object.mode_set(mode='EDIT')

	bpy.ops.object.mode_set(mode='POSE')

	#Adds IK constraints
	bpy.context.object.pose.bones[KNEE_LEFT].constraints.new("IK")
	bpy.context.object.pose.bones[KNEE_LEFT].constraints["IK"].target = bpy.context.active_object
	bpy.context.object.pose.bones[KNEE_LEFT].constraints["IK"].subtarget = LEG_IK_LEFT_BONE
	bpy.context.object.pose.bones[KNEE_LEFT].constraints["IK"].chain_count = 2
	bpy.context.object.pose.bones[KNEE_LEFT].constraints["IK"].use_tail = True
	bpy.context.object.pose.bones[KNEE_LEFT].constraints["IK"].iterations = 48

	bpy.context.object.pose.bones[KNEE_LEFT].constraints.new("LIMIT_ROTATION")
	bpy.context.object.pose.bones[KNEE_LEFT].constraints["Limit Rotation"].use_limit_x = True
	bpy.context.object.pose.bones[KNEE_LEFT].constraints["Limit Rotation"].use_limit_y = True
	bpy.context.object.pose.bones[KNEE_LEFT].constraints["Limit Rotation"].use_limit_z = True
	bpy.context.object.pose.bones[KNEE_LEFT].constraints["Limit Rotation"].min_x = math.pi/360 #radians = 0.5 degrees
	bpy.context.object.pose.bones[KNEE_LEFT].constraints["Limit Rotation"].max_x = math.pi #radians = 180 degrees

	bpy.context.object.pose.bones[KNEE_LEFT].constraints["Limit Rotation"].min_y = 0
	bpy.context.object.pose.bones[KNEE_LEFT].constraints["Limit Rotation"].max_y = 0
	bpy.context.object.pose.bones[KNEE_LEFT].constraints["Limit Rotation"].min_z = 0
	bpy.context.object.pose.bones[KNEE_LEFT].constraints["Limit Rotation"].max_z = 0

	bpy.context.object.pose.bones[KNEE_LEFT].constraints["Limit Rotation"].owner_space = "POSE"
	bpy.context.object.pose.bones[KNEE_LEFT].constraints["Limit Rotation"].name = "mmd_ik_limit_override"

	bpy.context.object.pose.bones[KNEE_RIGHT].constraints.new("IK")
	bpy.context.object.pose.bones[KNEE_RIGHT].constraints["IK"].target = bpy.context.active_object
	bpy.context.object.pose.bones[KNEE_RIGHT].constraints["IK"].subtarget = LEG_IK_RIGHT_BONE
	bpy.context.object.pose.bones[KNEE_RIGHT].constraints["IK"].chain_count = 2
	bpy.context.object.pose.bones[KNEE_RIGHT].constraints["IK"].use_tail = True
	bpy.context.object.pose.bones[KNEE_RIGHT].constraints["IK"].iterations = 48

	bpy.context.object.pose.bones[KNEE_RIGHT].constraints.new("LIMIT_ROTATION")
	bpy.context.object.pose.bones[KNEE_RIGHT].constraints["Limit Rotation"].use_limit_x = True
	bpy.context.object.pose.bones[KNEE_RIGHT].constraints["Limit Rotation"].use_limit_y = True
	bpy.context.object.pose.bones[KNEE_RIGHT].constraints["Limit Rotation"].use_limit_z = True
	bpy.context.object.pose.bones[KNEE_RIGHT].constraints["Limit Rotation"].min_x = math.pi/360 #radians = 0.5 degrees
	bpy.context.object.pose.bones[KNEE_RIGHT].constraints["Limit Rotation"].max_x = math.pi #radians = 180 degrees

	bpy.context.object.pose.bones[KNEE_RIGHT].constraints["Limit Rotation"].min_y = 0
	bpy.context.object.pose.bones[KNEE_RIGHT].constraints["Limit Rotation"].max_y = 0
	bpy.context.object.pose.bones[KNEE_RIGHT].constraints["Limit Rotation"].min_z = 0
	bpy.context.object.pose.bones[KNEE_RIGHT].constraints["Limit Rotation"].max_z = 0

	bpy.context.object.pose.bones[KNEE_RIGHT].constraints["Limit Rotation"].owner_space = "POSE"
	bpy.context.object.pose.bones[KNEE_RIGHT].constraints["Limit Rotation"].name = "mmd_ik_limit_override"

	# bpy.context.object.pose.bones[ANKLE_LEFT].constraints.new("DAMPED_TRACK")
	# bpy.context.object.pose.bones[ANKLE_LEFT].constraints["Damped Track"].target = bpy.context.active_object
	# bpy.context.object.pose.bones[ANKLE_LEFT].constraints["Damped Track"].subtarget = KNEE_LEFT
	# bpy.context.object.pose.bones[ANKLE_LEFT].constraints["Damped Track"].track_axis = 'TRACK_Y'
	# bpy.context.object.pose.bones[ANKLE_LEFT].constraints["Damped Track"].name = "mmd_ik_target_override"

	bpy.context.object.pose.bones[ANKLE_LEFT].constraints.new("IK")
	bpy.context.object.pose.bones[ANKLE_LEFT].constraints["IK"].target = bpy.context.active_object
	bpy.context.object.pose.bones[ANKLE_LEFT].constraints["IK"].subtarget = TOE_IK_LEFT_BONE
	bpy.context.object.pose.bones[ANKLE_LEFT].constraints["IK"].chain_count = 1
	bpy.context.object.pose.bones[ANKLE_LEFT].constraints["IK"].use_tail = True
	bpy.context.object.pose.bones[ANKLE_LEFT].constraints["IK"].iterations = 6

	# bpy.context.object.pose.bones[ANKLE_RIGHT].constraints.new("DAMPED_TRACK")
	# bpy.context.object.pose.bones[ANKLE_RIGHT].constraints["Damped Track"].target = bpy.context.active_object
	# bpy.context.object.pose.bones[ANKLE_RIGHT].constraints["Damped Track"].subtarget = KNEE_LEFT
	# bpy.context.object.pose.bones[ANKLE_RIGHT].constraints["Damped Track"].track_axis = 'TRACK_Y'
	# bpy.context.object.pose.bones[ANKLE_RIGHT].constraints["Damped Track"].name = "mmd_ik_target_override"

	bpy.context.object.pose.bones[ANKLE_RIGHT].constraints.new("IK")
	bpy.context.object.pose.bones[ANKLE_RIGHT].constraints["IK"].target = bpy.context.active_object
	bpy.context.object.pose.bones[ANKLE_RIGHT].constraints["IK"].subtarget = TOE_IK_RIGHT_BONE
	bpy.context.object.pose.bones[ANKLE_RIGHT].constraints["IK"].chain_count = 1
	bpy.context.object.pose.bones[ANKLE_RIGHT].constraints["IK"].use_tail = True
	bpy.context.object.pose.bones[ANKLE_RIGHT].constraints["IK"].iterations = 6

	if hasattr(bpy.context.object.pose.bones[KNEE_RIGHT], "mmd_bone"):
		bpy.context.object.pose.bones[KNEE_RIGHT].mmd_bone.ik_rotation_constraint = 2 # 180*2/math.pi
		bpy.context.object.pose.bones[KNEE_LEFT].mmd_bone.ik_rotation_constraint = 2 # 180*2/math.pi
		bpy.context.object.pose.bones[ANKLE_RIGHT].mmd_bone.ik_rotation_constraint = 4 #180*4/math.pi
		bpy.context.object.pose.bones[ANKLE_LEFT].mmd_bone.ik_rotation_constraint = 4 # 180*4/math.pi

	#create an 'IK' bone group and add the IK bones to it
	if 'IK' not in bpy.context.active_object.pose.bone_groups.keys():
		bpy.context.active_object.pose.bone_groups.new(name="IK")

	bpy.context.active_object.pose.bones[LEG_IK_LEFT_BONE].bone_group = bpy.context.active_object.pose.bone_groups['IK']
	bpy.context.active_object.pose.bones[LEG_IK_RIGHT_BONE].bone_group = bpy.context.active_object.pose.bone_groups['IK']
	bpy.context.active_object.pose.bones[TOE_IK_LEFT_BONE].bone_group = bpy.context.active_object.pose.bone_groups['IK']
	bpy.context.active_object.pose.bones[TOE_IK_RIGHT_BONE].bone_group = bpy.context.active_object.pose.bone_groups['IK']
	bpy.context.active_object.pose.bones[LEG_IK_LEFT_BONE_TIP].bone_group = bpy.context.active_object.pose.bone_groups['IK']
	bpy.context.active_object.pose.bones[LEG_IK_RIGHT_BONE_TIP].bone_group = bpy.context.active_object.pose.bone_groups['IK']
	bpy.context.active_object.pose.bones[TOE_IK_LEFT_BONE_TIP].bone_group = bpy.context.active_object.pose.bone_groups['IK']
	bpy.context.active_object.pose.bones[TOE_IK_RIGHT_BONE_TIP].bone_group = bpy.context.active_object.pose.bone_groups['IK']

	bpy.context.active_object.data.draw_type = 'OCTAHEDRAL'


class Add_MMD_foot_leg_IK(bpy.types.Operator):
	"""Add foot and leg IK bones and constraints to MMD model"""
	bl_idname = "object.add_foot_leg_ik"
	bl_label = "Add foot leg IK to MMD model"

	@classmethod
	def poll(cls, context):
		return context.active_object is not None

	def execute(self, context):
		clear_IK(context)
		main(context)
		return {'FINISHED'}

def register():
	bpy.utils.register_class(Add_MMD_foot_leg_IK)
	bpy.utils.register_class(Add_MMD_foot_leg_IK_Panel)


def unregister():
	bpy.utils.unregister_class(Add_MMD_foot_leg_IK)
	bpy.utils.unregister_class(Add_MMD_foot_leg_IK_Panel)


if __name__ == "__main__":
	register()