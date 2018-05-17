import bpy
from . import model


class MiscellaneousToolsPanel(bpy.types.Panel):
	"""Miscellaneous Tools panel"""
	bl_label = "Miscellaneous Tools Panel"
	bl_idname = "OBJECT_PT_miscellaneous_tools"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS"
	bl_category = "mmd_tools_helper"

	def draw(self, context):
		layout = self.layout

		row = layout.row()
		layout.prop(context.scene, "selected_miscellaneous_tools")
		row = layout.row()
		row.label(text="Miscellaneous Tools", icon='WORLD_DATA')
		row = layout.row()
		row.operator("mmd_tools_helper.miscellaneous_tools", text = "Execute Function")

def all_materials_mmd_ambient_white():
	for m in bpy.data.materials:
		if "mmd_tools_rigid" not in m.name:
			m.mmd_material.ambient_color[0] == 1.0
			m.mmd_material.ambient_color[1] == 1.0
			m.mmd_material.ambient_color[2] == 1.0



def combine_2_bones_1_bone(parent_bone_name, child_bone_name):
	bpy.ops.object.mode_set(mode='EDIT')
	child_bone_tail = bpy.context.active_object.data.edit_bones[child_bone_name].tail
	bpy.context.active_object.data.edit_bones[parent_bone_name].tail = child_bone_tail
	bpy.context.active_object.data.edit_bones.remove(bpy.context.active_object.data.edit_bones[child_bone_name])
	bpy.ops.object.mode_set(mode='POSE')
	print("Combined 2 bones: ", parent_bone_name, child_bone_name)

def combine_2_vg_1_vg(parent_vg_name, child_vg_name):
	for o in bpy.context.scene.objects:
		if o.type == 'MESH':
			if parent_vg_name in o.vertex_groups.keys():
				if child_vg_name in o.vertex_groups.keys():
					for v in o.data.vertices:
						for g in v.groups:
							if o.vertex_groups[g.group] == o.vertex_groups[child_vg_name]:
								o.vertex_groups[parent_vg_name].add([v.index], o.vertex_groups[child_vg_name].weight(v.index), 'ADD')
					o.vertex_groups.remove(o.vertex_groups[child_vg_name])
					print("Combined 2 vertex groups: ", parent_vg_name, child_vg_name)

def analyze_selected_parent_child_bone_pair():
	selected_bones = []

	for b in bpy.context.active_object.pose.bones:
		if b.bone.select == True:
			selected_bones.append(b.bone.name)

	if len(selected_bones) != 2:
		print("Exactly 2 bones must be selected." , len(selected_bones), "are selected.")
		return None, None
	if len(selected_bones) == 2:

		if bpy.context.active_object.data.bones[selected_bones[0]].parent == bpy.context.active_object.data.bones[selected_bones[1]]:
			parent_bone_name = selected_bones[1]
			child_bone_name = selected_bones[0]
			return parent_bone_name, child_bone_name
			# combine_2_bones_1_bone(parent_bone, child_bone)
			# combine_2_vg_1_vg(parent_bone, child_bone)

		if bpy.context.active_object.data.bones[selected_bones[1]].parent == bpy.context.active_object.data.bones[selected_bones[0]]:
			parent_bone_name = selected_bones[0]
			child_bone_name = selected_bones[1]
			return parent_bone_name, child_bone_name
			# combine_2_bones_1_bone(parent_bone, child_bone)
			# combine_2_vg_1_vg(parent_bone, child_bone)

		if bpy.context.active_object.data.bones[selected_bones[0]].parent != bpy.context.active_object.data.bones[selected_bones[1]]:
			if bpy.context.active_object.data.bones[selected_bones[1]].parent != bpy.context.active_object.data.bones[selected_bones[0]]:
				print("Combining 2 bones to 1 bone requires a parent-child bone pair to be selected. There is no parent-child relationship between the 2 selected bones.")
				return None, None

	bpy.ops.object.mode_set(mode='POSE')

def delete_unused_bones():
	print('\n')
	bpy.ops.object.mode_set(mode='EDIT')
	bones_to_be_deleted = []

	for b in bpy.context.active_object.data.edit_bones:
		if 'unused' in b.name.lower():
			bones_to_be_deleted.append(b.name)

	for b in bones_to_be_deleted:
		bpy.context.active_object.data.edit_bones.remove(bpy.context.active_object.data.edit_bones[b])
		print("removed bone  ", b)

	bpy.ops.object.mode_set(mode='POSE')

def delete_unused_vertex_groups():
	print('\n')
	for o in bpy.context.scene.objects:
		if o.type == 'MESH':
			delete_these = []
			for vg in o.vertex_groups:
				if 'unused' in vg.name.lower():
					if vg.name not in delete_these:
						delete_these.append(vg.name)
			for vg in delete_these:
				if vg in o.vertex_groups.keys():
					o.vertex_groups.remove(o.vertex_groups[vg])
					print('removed vertex group  ', vg)

def test_is_mmd_english_armature():
	mmd_english = True
	bpy.context.scene.objects.active = model.findArmature(bpy.context.active_object)
	mmd_english_test_bone_names = ['upper body', 'neck', 'head', 'shoulder_L', 'arm_L', 'elbow_L', 'wrist_L', 'leg_L', 'knee_L', 'ankle_L', 'shoulder_R', 'arm_R', 'elbow_R', 'wrist_R', 'leg_R', 'knee_R', 'ankle_R']
	missing_mmd_english_test_bone_names = []
	for b in mmd_english_test_bone_names:
		if b not in bpy.context.active_object.data.bones.keys():
			missing_mmd_english_test_bone_names.append(b)
	if len(missing_mmd_english_test_bone_names) > 0:
		print("Missing mmd_english test bone names = ", missing_mmd_english_test_bone_names)
		print('\n')
		print("This armature appears not to be an mmd_english armature")
		mmd_english = False
	return mmd_english


def correct_root_center():
	print('\n')
	if test_is_mmd_english_armature() == True:
		bpy.ops.object.mode_set(mode='EDIT')

		# if there is no "root" bone in the armature, a root bone is added
		if "root" not in bpy.context.active_object.data.edit_bones.keys():
			root_bone = bpy.context.active_object.data.edit_bones.new('root')
			root_bone.head[:] = (0,0,0)
			root_bone.tail[:] = (0,0,1)
			if "center" in bpy.context.active_object.data.edit_bones.keys():
				bpy.context.active_object.data.edit_bones["center"].parent = bpy.context.active_object.data.edit_bones["root"]
				bpy.context.active_object.data.edit_bones["center"].use_connect = False
			print("Added MMD root bone.")
		bpy.ops.object.mode_set(mode='OBJECT')

		# if the "center" bone has a vertex group, it is renamed to "lower body"
		mesh_objects = model.find_MMD_MeshesList(bpy.context.active_object)
		for o in mesh_objects:
			if "center" in o.vertex_groups.keys():
				if "center" in bpy.context.active_object.data.bones.keys():
					bpy.context.active_object.data.bones["center"].name = "lower body"
					print("Renamed center bone to lower body bone.")
					bpy.ops.object.mode_set(mode='EDIT')
					bpy.context.active_object.data.edit_bones["lower body"].tail.z = 0.5 * (bpy.context.active_object.data.edit_bones["leg_L"].head.z + bpy.context.active_object.data.edit_bones["leg_R"].head.z)
		bpy.ops.object.mode_set(mode='OBJECT')

		# if there is no "center" bone in the armature, a center bone is added
		if "center" not in bpy.context.active_object.data.bones.keys():
			bpy.ops.object.mode_set(mode='EDIT')
			center_bone = bpy.context.active_object.data.edit_bones.new("center")
			print("Added center bone.")
			center_bone.head = 0.25 * (bpy.context.active_object.data.edit_bones["knee_L"].head + bpy.context.active_object.data.edit_bones["knee_R"].head + bpy.context.active_object.data.edit_bones["leg_L"].head + bpy.context.active_object.data.edit_bones["leg_R"].head)
			center_bone.tail.z = center_bone.head.z - 1
			center_bone.parent = bpy.context.active_object.data.edit_bones["root"]
			if "lower body" in bpy.context.active_object.data.edit_bones.keys():
				bpy.context.active_object.data.edit_bones["lower body"].parent = bpy.context.active_object.data.edit_bones["center"]
			if "upper body" in bpy.context.active_object.data.edit_bones.keys():
				bpy.context.active_object.data.edit_bones["upper body"].parent = bpy.context.active_object.data.edit_bones["center"]
		bpy.ops.object.mode_set(mode='OBJECT')
	if test_is_mmd_english_armature() == False:
		print("This operator will only work on an armature with mmd_english bone names. First rename bones to mmd_english and then try running this operator again.")


def main(context):
	# print(bpy.context.scene.selected_miscellaneous_tools)
	if bpy.context.scene.selected_miscellaneous_tools == "combine_2_bones":
		bpy.context.scene.objects.active = model.findArmature(bpy.context.active_object)
		parent_bone_name, child_bone_name = analyze_selected_parent_child_bone_pair()
		if parent_bone_name is not None:
			if child_bone_name is not None:
				combine_2_vg_1_vg(parent_bone_name, child_bone_name)
				combine_2_bones_1_bone(parent_bone_name, child_bone_name)
	if bpy.context.scene.selected_miscellaneous_tools == "delete_unused":
		bpy.context.scene.objects.active = model.findArmature(bpy.context.active_object)
		delete_unused_bones()
		delete_unused_vertex_groups()
	if bpy.context.scene.selected_miscellaneous_tools == "mmd_ambient_white":
		all_materials_mmd_ambient_white()
	if bpy.context.scene.selected_miscellaneous_tools == "correct_root_center":
		bpy.context.scene.objects.active = model.findArmature(bpy.context.active_object)
		correct_root_center()



class MiscellaneousTools(bpy.types.Operator):
	"""Miscellanous Tools"""
	bl_idname = "mmd_tools_helper.miscellaneous_tools"
	bl_label = "Miscellaneous Tools"

	bpy.types.Scene.selected_miscellaneous_tools = bpy.props.EnumProperty(items = [('none', 'none', 'none'), ("combine_2_bones", "Combine 2 bones", "Combine a parent-child pair of bones and their vertex groups to 1 bone and 1 vertex group"), ("delete_unused", "Delete unused bones and unused vertex groups", "Delete all bones and vertex groups which have the word 'unused' in them"), ("mmd_ambient_white", "All materials MMD ambient color white", "Change the MMD ambient color of all materials to white"), ("correct_root_center", "Correct MMD Root and Center bones", "Correct MMD root and center bones") ], name = "Select Function:", default = 'none')

	@classmethod
	def poll(cls, context):
		return context.active_object is not None

	def execute(self, context):
		main(context)
		return {'FINISHED'}


def register():
	bpy.utils.register_class(MiscellaneousToolsPanel)
	bpy.utils.register_class(MiscellaneousTools)


def unregister():
	bpy.utils.unregister_class(MiscellaneousToolsPanel)
	bpy.utils.unregister_class(MiscellaneousTools)


if __name__ == "__main__":
	register()



	
