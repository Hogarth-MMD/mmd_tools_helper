import bpy
import math

from . import register_wrap
from . import model

@register_wrap
class Add_MMD_Hand_Arm_IK_Panel(bpy.types.Panel):
	"""Add hand and arm IK bones and constraints to active MMD model"""
	bl_idname = "OBJECT_PT_mmd_add_hand_arm_ik"
	bl_label = "Add Hand Arm IK to MMD model"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "mmd_tools_helper"

	def draw(self, context):
		layout = self.layout
		row = layout.row()

		row.label(text="Add hand arm IK to MMD model", icon="ARMATURE_DATA")
		row = layout.row()
		row.operator("object.add_hand_arm_ik", text = "Add hand_arm IK to MMD model")
		row = layout.row()


def clear_IK(context):
	IK_target_bones = []
	IK_target_tip_bones = []
	bpy.context.scene.objects.active = model.findArmature(bpy.context.active_object)
	bpy.ops.object.mode_set(mode='POSE')
	english = ["elbow_L", "elbow_R", "wrist_L", "wrist_R", "middle1_L", "middle1_R"]
	japanese = ["左ひじ", "右ひじ", "左手首", "右手首", "左中指１", "右中指１"]
	japanese_L_R = ["ひじ.L", "ひじ.R", "手首.L", "手首.R", "中指１.L", "中指１.R"]
	# IK_BONE_NAMES = ["elbow IK_L", "elbow IK_R", "middle1 IK_L", "middle1 IK_R"]
	arm_hand_bones = english + japanese + japanese_L_R
	for b in bpy.context.active_object.pose.bones.keys():
		if b in arm_hand_bones:
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
		if b in arm_hand_bones:
			for c in bpy.context.active_object.pose.bones[b].constraints:
				bpy.context.active_object.pose.bones[b].constraints.remove(c)


def armature_diagnostic():
	ENGLISH_ARM_BONES = ["elbow_L", "elbow_R", "wrist_L", "wrist_R", "middle1_L", "middle1_R"]
	JAPANESE_ARM_BONES = ["左ひじ", "右ひじ", "左手首", "右手首", "左中指１", "右中指１"]
	IK_BONE_NAMES = ["elbow IK_L", "elbow IK_R", "middle1 IK_L", "middle1 IK_R"]
	ENGLISH_OK = True
	JAPANESE_OK = True

	print('\n\n\n', 'These English bones are needed to add hand IK:', '\n')
	print(ENGLISH_ARM_BONES, '\n')
	for b in ENGLISH_ARM_BONES:
		if b not in bpy.context.active_object.data.bones.keys():
			ENGLISH_OK = False
			print('This bone is not in this armature:', '\n', b)
	if ENGLISH_OK == True:
		print('OK! All English-named bones are present which are needed to add hand IK')

	print('\n', 'OR These Japanese bones are needed to add IK:', '\n')
	print(JAPANESE_ARM_BONES, '\n')
	for b in JAPANESE_ARM_BONES:
		if b not in bpy.context.active_object.data.bones.keys():
			JAPANESE_OK = False
			print('This bone is not in this armature:', '\n', b)
	if JAPANESE_OK == True:
		print('OK! All Japanese-named bones are present which are needed to add hand IK', '\n')

	print('\n', 'hand IK bones which are already in the armature = ', '\n')
	for b in IK_BONE_NAMES:
		if b in bpy.context.active_object.data.bones.keys():
			print('This armature appears to already have hand IK bones. This bone seems to be a hand IK bone:', '\n', b)

def main(context):
	bpy.context.scene.objects.active = model.findArmature(bpy.context.active_object)

	#Lists of possible names of elbow, wrist and middle1 bones
	ARM_LEFT_BONE = ["左ひじ", "ひじ.L", "elbow_L"]
	ARM_RIGHT_BONE = ["右ひじ", "ひじ.R", "elbow_R"]
	ELBOW_LEFT_BONE = ["左手首", "手首.L", "wrist_L"]
	ELBOW_RIGHT_BONE = ["右手首", "手首.R", "wrist_R"]
	WRIST_LEFT_BONE = ["左中指１", "中指１.L", "middle1_L"]
	WRIST_RIGHT_BONE = ["右中指１", "中指１.R", "middle1_R"]

	print('\n')
	#Searches through the bones of the active armature and finds the ARM, ELBOW and WRIST bones.
	for b in bpy.context.active_object.data.bones:
		if b.name in ARM_LEFT_BONE:
			ARM_LEFT = b.name
			print('ARM_LEFT = ', ARM_LEFT)
		if b.name in ARM_RIGHT_BONE:
			ARM_RIGHT = b.name
			print('ARM_RIGHT = ', ARM_RIGHT)
		if b.name in ELBOW_LEFT_BONE:
			ELBOW_LEFT = b.name
			print('ELBOW_LEFT = ', ELBOW_LEFT)
		if b.name in ELBOW_RIGHT_BONE:
			ELBOW_RIGHT = b.name
			print('ELBOW_RIGHT = ', ELBOW_RIGHT)
		if b.name in WRIST_LEFT_BONE:
			WRIST_LEFT = b.name
			print('WRIST_LEFT = ', WRIST_LEFT)
		if b.name in WRIST_RIGHT_BONE:
			WRIST_RIGHT = b.name
			print('WRIST_RIGHT = ', WRIST_RIGHT)

	#measurements of the length of the elbow bone which will used to calculate the lengths of the IK bones.
	DOUBLE_LENGTH_OF_ELBOW_BONE = bpy.context.active_object.data.bones[ELBOW_LEFT].length * 2
	TWENTIETH_LENGTH_OF_ELBOW_BONE = bpy.context.active_object.data.bones[ELBOW_LEFT].length * 0.05

	bpy.ops.object.mode_set(mode='EDIT')


	# if ARM_LEFT == "左ひじ" or ARM_LEFT == "ひじ.L" or ARM_LEFT == "elbow_L":

	#The IK bones are created, with English bone names.
	bone = bpy.context.active_object.data.edit_bones.new("elbow_IK_L")
	bone.head = bpy.context.active_object.data.edit_bones[ELBOW_LEFT].head
	bone.tail = bpy.context.active_object.data.edit_bones[ELBOW_LEFT].head
	bone.tail.z = bpy.context.active_object.data.edit_bones[ELBOW_LEFT].head.z - DOUBLE_LENGTH_OF_ELBOW_BONE

	bone = bpy.context.active_object.data.edit_bones.new("elbow_IK_R")
	bone.head = bpy.context.active_object.data.edit_bones[ELBOW_RIGHT].head
	bone.tail = bpy.context.active_object.data.edit_bones[ELBOW_RIGHT].head
	bone.tail.z = bpy.context.active_object.data.edit_bones[ELBOW_RIGHT].head.z - DOUBLE_LENGTH_OF_ELBOW_BONE

	bone = bpy.context.active_object.data.edit_bones.new("middle1_IK_L")
	bone.head = bpy.context.active_object.data.edit_bones[WRIST_LEFT].head
	bone.tail = bpy.context.active_object.data.edit_bones[WRIST_LEFT].head
	bone.tail.z = bpy.context.active_object.data.edit_bones[WRIST_LEFT].head.z - DOUBLE_LENGTH_OF_ELBOW_BONE
	print('bone = ', bone)
	bone.parent = bpy.context.active_object.data.edit_bones["elbow_IK_L"]
	bone.use_connect = False

	bone = bpy.context.active_object.data.edit_bones.new("middle1_IK_R")
	bone.head = bpy.context.active_object.data.edit_bones[WRIST_RIGHT].head
	bone.tail = bpy.context.active_object.data.edit_bones[WRIST_RIGHT].head
	bone.tail.z = bpy.context.active_object.data.edit_bones[WRIST_RIGHT].head.z - DOUBLE_LENGTH_OF_ELBOW_BONE
	bone.parent = bpy.context.active_object.data.edit_bones["elbow_IK_R"]
	bone.use_connect = False

	bone = bpy.context.active_object.data.edit_bones.new("elbow_IK_L_t")
	bone.head = bpy.context.active_object.data.edit_bones["elbow_IK_L"].head
	bone.tail = bpy.context.active_object.data.edit_bones["elbow_IK_L"].head
	bone.tail.y = bone.tail.y + TWENTIETH_LENGTH_OF_ELBOW_BONE
	bone.parent = bpy.context.active_object.data.edit_bones["elbow_IK_L"]
	bone.use_connect = False
	bpy.ops.object.mode_set(mode='POSE')
	bpy.context.active_object.pose.bones["elbow_IK_L_t"].bone.hide = True
	if hasattr(bpy.context.active_object.pose.bones["elbow_IK_L_t"], "mmd_bone"):
		bpy.context.active_object.pose.bones["elbow_IK_L_t"].mmd_bone.is_visible = False
		bpy.context.active_object.pose.bones["elbow_IK_L_t"].mmd_bone.is_controllable = False
		bpy.context.active_object.pose.bones["elbow_IK_L_t"].mmd_bone.is_tip = True
	bpy.ops.object.mode_set(mode='EDIT')

	bone = bpy.context.active_object.data.edit_bones.new("elbow_IK_R_t")
	bone.head = bpy.context.active_object.data.edit_bones["elbow_IK_R"].head
	bone.tail = bpy.context.active_object.data.edit_bones["elbow_IK_R"].head
	bone.tail.y = bone.tail.y + TWENTIETH_LENGTH_OF_ELBOW_BONE
	bone.parent = bpy.context.active_object.data.edit_bones["elbow_IK_R"]
	bone.use_connect = False
	bpy.ops.object.mode_set(mode='POSE')
	bpy.context.active_object.pose.bones["elbow_IK_R_t"].bone.hide = True
	if hasattr(bpy.context.active_object.pose.bones["elbow_IK_R_t"], "mmd_bone"):
		bpy.context.active_object.pose.bones["elbow_IK_R_t"].mmd_bone.is_visible = False
		bpy.context.active_object.pose.bones["elbow_IK_R_t"].mmd_bone.is_controllable = False
		bpy.context.active_object.pose.bones["elbow_IK_R_t"].mmd_bone.is_tip = True
	bpy.ops.object.mode_set(mode='EDIT')

	bone = bpy.context.active_object.data.edit_bones.new("middle1_IK_L_t")
	bone.head = bpy.context.active_object.data.edit_bones["middle1_IK_L"].head
	bone.tail = bpy.context.active_object.data.edit_bones["middle1_IK_L"].head
	bone.tail.z = bone.tail.z - TWENTIETH_LENGTH_OF_ELBOW_BONE
	bone.parent = bpy.context.active_object.data.edit_bones["middle1_IK_L"]
	bone.use_connect = False
	bpy.ops.object.mode_set(mode='POSE')
	bpy.context.active_object.pose.bones["middle1_IK_L_t"].bone.hide = True
	if hasattr(bpy.context.active_object.pose.bones["middle1_IK_L_t"], "mmd_bone"):
		bpy.context.active_object.pose.bones["middle1_IK_L_t"].mmd_bone.is_visible = False
		bpy.context.active_object.pose.bones["middle1_IK_L_t"].mmd_bone.is_controllable = False
		bpy.context.active_object.pose.bones["middle1_IK_L_t"].mmd_bone.is_tip = True
	bpy.ops.object.mode_set(mode='EDIT')

	bone = bpy.context.active_object.data.edit_bones.new("middle1_IK_R_t")
	bone.head = bpy.context.active_object.data.edit_bones["middle1_IK_R"].head
	bone.tail = bpy.context.active_object.data.edit_bones["middle1_IK_R"].head
	bone.tail.z = bone.tail.z - TWENTIETH_LENGTH_OF_ELBOW_BONE
	bone.parent = bpy.context.active_object.data.edit_bones["middle1_IK_R"]
	bone.use_connect = False
	bpy.ops.object.mode_set(mode='POSE')
	bpy.context.active_object.pose.bones["middle1_IK_R_t"].bone.hide = True
	if hasattr(bpy.context.active_object.pose.bones["middle1_IK_R_t"], "mmd_bone"):
		bpy.context.active_object.pose.bones["middle1_IK_R_t"].mmd_bone.is_visible = False
		bpy.context.active_object.pose.bones["middle1_IK_R_t"].mmd_bone.is_controllable = False
		bpy.context.active_object.pose.bones["middle1_IK_R_t"].mmd_bone.is_tip = True
	bpy.ops.object.mode_set(mode='EDIT')

	bpy.ops.object.mode_set(mode='POSE')


	#Adds IK constraints
	bpy.context.object.pose.bones[ARM_LEFT].constraints.new("IK")
	bpy.context.object.pose.bones[ARM_LEFT].constraints["IK"].target = bpy.context.active_object
	bpy.context.object.pose.bones[ARM_LEFT].constraints["IK"].subtarget = "elbow_IK_L"
	bpy.context.object.pose.bones[ARM_LEFT].constraints["IK"].chain_count = 2
	bpy.context.object.pose.bones[ARM_LEFT].constraints["IK"].use_tail = True
	bpy.context.object.pose.bones[ARM_LEFT].constraints["IK"].iterations = 48
	# bpy.context.object.pose.bones[ELBOW_LEFT].constraints["IK"].use_location = False

	# bpy.context.object.pose.bones[ARM_LEFT].constraints.new("LIMIT_ROTATION")
	# bpy.context.object.pose.bones[ARM_LEFT].constraints["Limit Rotation"].use_limit_x = True
	# bpy.context.object.pose.bones[ARM_LEFT].constraints["Limit Rotation"].min_x = math.pi/360 #radians = 0.5 degrees
	# bpy.context.object.pose.bones[ARM_LEFT].constraints["Limit Rotation"].max_x = math.pi #radians = 180 degrees
	# bpy.context.object.pose.bones[ARM_LEFT].constraints["Limit Rotation"].owner_space = "POSE"
	# bpy.context.object.pose.bones[ARM_LEFT].constraints["Limit Rotation"].name = "mmd_ik_limit_override"


	bpy.context.object.pose.bones[ARM_RIGHT].constraints.new("IK")
	bpy.context.object.pose.bones[ARM_RIGHT].constraints["IK"].target = bpy.context.active_object
	bpy.context.object.pose.bones[ARM_RIGHT].constraints["IK"].subtarget = "elbow_IK_R"
	bpy.context.object.pose.bones[ARM_RIGHT].constraints["IK"].chain_count = 2
	bpy.context.object.pose.bones[ARM_RIGHT].constraints["IK"].use_tail = True
	bpy.context.object.pose.bones[ARM_RIGHT].constraints["IK"].iterations = 48
	# bpy.context.object.pose.bones[ELBOW_RIGHT].constraints["IK"].use_location = False

	# bpy.context.object.pose.bones[ARM_RIGHT].constraints.new("LIMIT_ROTATION")
	# bpy.context.object.pose.bones[ARM_RIGHT].constraints["Limit Rotation"].use_limit_x = True
	# bpy.context.object.pose.bones[ARM_RIGHT].constraints["Limit Rotation"].min_x = math.pi/360 #radians = 0.5 degrees
	# bpy.context.object.pose.bones[ARM_RIGHT].constraints["Limit Rotation"].max_x = math.pi #radians = 180 degrees
	# bpy.context.object.pose.bones[ARM_RIGHT].constraints["Limit Rotation"].owner_space = "POSE"
	# bpy.context.object.pose.bones[ARM_RIGHT].constraints["Limit Rotation"].name = "mmd_ik_limit_override"

	# bpy.context.object.pose.bones[ELBOW_LEFT].constraints.new("DAMPED_TRACK")
	# bpy.context.object.pose.bones[ELBOW_LEFT].constraints["Damped Track"].target = bpy.context.active_object
	# bpy.context.object.pose.bones[ELBOW_LEFT].constraints["Damped Track"].subtarget = ARM_LEFT
	# bpy.context.object.pose.bones[ELBOW_LEFT].constraints["Damped Track"].track_axis = 'TRACK_Y'
	# bpy.context.object.pose.bones[ELBOW_LEFT].constraints["Damped Track"].name = "mmd_ik_target_override"


	bpy.context.object.pose.bones[ELBOW_LEFT].constraints.new("IK")
	bpy.context.object.pose.bones[ELBOW_LEFT].constraints["IK"].target = bpy.context.active_object
	bpy.context.object.pose.bones[ELBOW_LEFT].constraints["IK"].subtarget = "middle1_IK_L"
	bpy.context.object.pose.bones[ELBOW_LEFT].constraints["IK"].chain_count = 1
	bpy.context.object.pose.bones[ELBOW_LEFT].constraints["IK"].use_tail = True
	bpy.context.object.pose.bones[ELBOW_LEFT].constraints["IK"].iterations = 6
	# bpy.context.object.pose.bones[WRIST_LEFT].constraints["IK"].use_location = False

	# bpy.context.object.pose.bones[ELBOW_RIGHT].constraints.new("DAMPED_TRACK")
	# bpy.context.object.pose.bones[ELBOW_RIGHT].constraints["Damped Track"].target = bpy.context.active_object
	# bpy.context.object.pose.bones[ELBOW_RIGHT].constraints["Damped Track"].subtarget = ARM_LEFT
	# bpy.context.object.pose.bones[ELBOW_RIGHT].constraints["Damped Track"].track_axis = 'TRACK_Y'
	# bpy.context.object.pose.bones[ELBOW_RIGHT].constraints["Damped Track"].name = "mmd_ik_target_override"

	bpy.context.object.pose.bones[ELBOW_RIGHT].constraints.new("IK")
	bpy.context.object.pose.bones[ELBOW_RIGHT].constraints["IK"].target = bpy.context.active_object
	bpy.context.object.pose.bones[ELBOW_RIGHT].constraints["IK"].subtarget = "middle1_IK_R"
	bpy.context.object.pose.bones[ELBOW_RIGHT].constraints["IK"].chain_count = 1
	bpy.context.object.pose.bones[ELBOW_RIGHT].constraints["IK"].use_tail = True
	bpy.context.object.pose.bones[ELBOW_RIGHT].constraints["IK"].iterations = 6
	# bpy.context.object.pose.bones[WRIST_RIGHT].constraints["IK"].use_location = False

	if hasattr(bpy.context.object.pose.bones[ARM_RIGHT], "mmd_bone"):
		bpy.context.object.pose.bones[ARM_RIGHT].mmd_bone.ik_rotation_constraint = 2 # 180*2/math.pi
		bpy.context.object.pose.bones[ARM_LEFT].mmd_bone.ik_rotation_constraint = 2 # 180*2/math.pi
		bpy.context.object.pose.bones[ELBOW_RIGHT].mmd_bone.ik_rotation_constraint = 4 #180*4/math.pi
		bpy.context.object.pose.bones[ELBOW_LEFT].mmd_bone.ik_rotation_constraint = 4 # 180*4/math.pi

	#create an 'IK' bone group and add the IK bones to it
	if 'IK' not in bpy.context.active_object.pose.bone_groups.keys():
		bpy.context.active_object.pose.bone_groups.new(name="IK")

	bpy.context.active_object.pose.bones["elbow_IK_L"].bone_group = bpy.context.active_object.pose.bone_groups['IK']
	bpy.context.active_object.pose.bones["elbow_IK_R"].bone_group = bpy.context.active_object.pose.bone_groups['IK']
	bpy.context.active_object.pose.bones["middle1_IK_L"].bone_group = bpy.context.active_object.pose.bone_groups['IK']
	bpy.context.active_object.pose.bones["middle1_IK_R"].bone_group = bpy.context.active_object.pose.bone_groups['IK']
	bpy.context.active_object.pose.bones["elbow_IK_L_t"].bone_group = bpy.context.active_object.pose.bone_groups['IK']
	bpy.context.active_object.pose.bones["elbow_IK_R_t"].bone_group = bpy.context.active_object.pose.bone_groups['IK']
	bpy.context.active_object.pose.bones["middle1_IK_L_t"].bone_group = bpy.context.active_object.pose.bone_groups['IK']
	bpy.context.active_object.pose.bones["middle1_IK_R_t"].bone_group = bpy.context.active_object.pose.bone_groups['IK']


@register_wrap
class Add_MMD_Hand_Arm_IK(bpy.types.Operator):
	"""Add hand and arm IK bones and constraints to active MMD model"""
	bl_idname = "object.add_hand_arm_ik"
	bl_label = "Add Hand Arm IK to MMD model"

	@classmethod
	def poll(cls, context):
		return context.active_object is not None

	def execute(self, context):
		clear_IK(context)
		main(context)
		return {'FINISHED'}
