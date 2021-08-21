import bpy

from . import register_wrap
from . import model
from . import import_csv

def __items(display_item_frame):
    return getattr(display_item_frame, 'data', display_item_frame.items)

@register_wrap
class MmdToolsDisplayPanelGroupsPanel(bpy.types.Panel):
	"""Mass add bone names and shape key names to display panel groups"""
	bl_idname = "OBJECT_PT_mmd_add_display_panel_groups"
	bl_label = "Create Display Panel Groups and Add Items"
	bl_space_type = "VIEW_3D"
	bl_region_type = "TOOLS" if bpy.app.version < (2,80,0) else "UI"
	bl_category = "mmd_tools_helper"

	def draw(self, context):
		layout = self.layout
		row = layout.row()

		row.label(text="Add MMD Display Panel Groups", icon="ARMATURE_DATA")
		row = layout.row()
		layout.prop (context.scene, "display_panel_options")
		row = layout.row()
		row.operator("object.add_display_panel_groups", text = "Add MMD display panel items")
		row = layout.row()

def delete_empty_display_panel_groups(root):
	bpy.context.scene.objects.active = root
	for d in range(len(bpy.context.active_object.mmd_root.display_item_frames)-1, 1, -1):
		#if bpy.context.active_object.mmd_root.display_item_frames[d].name != "Root" and bpy.context.active_object.mmd_root.display_item_frames[d].name != "表情":
		if len(__items(bpy.context.active_object.mmd_root.display_item_frames[d])) == 0:
			bpy.context.active_object.mmd_root.display_item_frames.remove(d)

def clear_display_panel_groups(root):
	bpy.context.scene.objects.active = root
	bpy.context.active_object.mmd_root.display_item_frames.clear()

def display_panel_groups_from_bone_groups(root, armature_object):
	bpy.context.scene.objects.active = armature_object
	bpy.ops.object.mode_set(mode='POSE')
	bone_groups = armature_object.pose.bone_groups.keys() + ["Other"]
	bone_groups_of_bones = []
	for b in armature_object.pose.bones:
		if b.bone_group is not None:
			if "dummy" not in b.name and "shadow" not in b.name:
				if b.name not in ["root", "全ての親", "center", "センター"]:
					bone_groups_of_bones.append((b.name, b.bone_group.name))
				if b.name in ["root", "全ての親", "center", "センター"]:
					bone_groups_of_bones.append((b.name, "Root"))
		else:
			if "dummy" not in b.name and "shadow" not in b.name:
				if b.name not in ["root", "全ての親", "center", "センター"]:
					bone_groups_of_bones.append((b.name, "Other"))
				if b.name in ["root", "全ての親", "center", "センター"]:
					bone_groups_of_bones.append((b.name, "Root"))
	# bpy.context.scene.objects.active = armature_object.parent
	bpy.context.scene.objects.active = model.findRoot(armature_object)
	group = bpy.context.active_object.mmd_root.display_item_frames.add()
	group.name = "Root"
	group.name_e = "Root"
	group.is_special = True
	group = bpy.context.active_object.mmd_root.display_item_frames.add()
	group.name = "表情"
	group.name_e = "Expressions"
	group.is_special = True
	for bg in bone_groups:
		if bg != "Root" and bg != "表情":
			group = bpy.context.active_object.mmd_root.display_item_frames.add()
			group.name = bg
			group.name_e = bg
	for bgb in bone_groups_of_bones:
		item = __items(bpy.context.active_object.mmd_root.display_item_frames[bgb[1]]).add()
		item.name = bgb[0]
		item.name_e = bgb[0]

def display_panel_groups_from_shape_keys(mesh_objects_list):
	shape_key_names = []
	for m in mesh_objects_list:
		if m.data.shape_keys is not None:
			for s in m.data.shape_keys.key_blocks:
				if 'sdef' not in s.name and s.name != 'Basis':
					if s.name not in shape_key_names:
						shape_key_names.append(s.name)
		root = model.findRoot(m)
	for skn in shape_key_names:
		if skn not in __items(root.mmd_root.display_item_frames["表情"]).keys():
			item = __items(root.mmd_root.display_item_frames["表情"]).add()
			item.type = 'MORPH'
			item.morph_type = 'vertex_morphs'
			item.name = skn

def display_panel_groups_non_vertex_morphs(root):
	bpy.context.scene.objects.active = root
	for m in root.mmd_root.bone_morphs:
		if m.name not in __items(root.mmd_root.display_item_frames["表情"]).keys():
			item = __items(root.mmd_root.display_item_frames["表情"]).add()
			item.type = 'MORPH'
			item.morph_type = "bone_morphs"
			item.name = m.name
	for m in root.mmd_root.material_morphs:
		if m.name not in __items(root.mmd_root.display_item_frames["表情"]).keys():
			item = __items(root.mmd_root.display_item_frames["表情"]).add()
			item.type = 'MORPH'
			item.morph_type = "material_morphs"
			item.name = m.name
	for m in root.mmd_root.uv_morphs:
		if m.name not in __items(root.mmd_root.display_item_frames["表情"]).keys():
			item = __items(root.mmd_root.display_item_frames["表情"]).add()
			item.type = 'MORPH'
			item.morph_type = "uv_morphs"
			item.name = m.name
	for m in root.mmd_root.group_morphs:
		if m.name not in __items(root.mmd_root.display_item_frames["表情"]).keys():
			item = __items(root.mmd_root.display_item_frames["表情"]).add()
			item.type = 'MORPH'
			item.morph_type = "group_morphs"
			item.name = m.name

#from pymeshio's englishmap.py
MMD_Standard_Display_Panel_Groups=[
("Root", "Root"),
("Exp", "表情"),
("IK", "ＩＫ"),
("Body[u]", "体(上)"),
("Hair", "髪"),
("Arms", "腕"),
("Fingers", "指"),
("Body[l]", "体(下)"),
("Legs", "足"),
]

My_Display_Panel_Groups =[
("Root", "Root"),
("Expressions", "表情"),
("IK", "ＩＫ"),
("Head", "頭"),
("Fingers", "指"),
("Hair", "髪"),
("Skirt", "スカト"),
("Body", "体"),
("Other", "Other"),
]

# by name, children of head bone, IK constraint

def display_panel_groups_create(root, armature_object):
	BONE_NAMES_DICTIONARY = import_csv.use_csv_bones_dictionary()
	FINGER_BONE_NAMES_DICTIONARY = import_csv.use_csv_bones_fingers_dictionary()

	bpy.context.scene.objects.active = armature_object

	items_added = []

	head_names = ["Head", "head", "頭", "eye", "nose", "tongue", "lip", "jaw", "brow", "cheek", "mouth", "nostril"]
	hair_names = ["Hair", "hair", "髪"]
	skirt_names = ["Skirt", "skirt", "スカト", "スカート"] # 
	
	root_names = BONE_NAMES_DICTIONARY[1] # + ["center", "Center", "センター"]
	body_names = []
	finger_names = []
	ik_names = [] # ["IK", "ik", ＩＫ"]

	for b in BONE_NAMES_DICTIONARY:
		if BONE_NAMES_DICTIONARY.index(b) not in [0,1,3]:
			# not in [0,1,3] , not a bonemap ID, not a root bone, not a head bone
			body_names = body_names + list(b)
	for f in FINGER_BONE_NAMES_DICTIONARY:
		finger_names = finger_names + list(f)

	bpy.ops.object.mode_set(mode='POSE')
	for pb in bpy.context.active_object.pose.bones:
		for c in pb.constraints:
			if c.type == "IK":
				if c.subtarget != '':
					if c.subtarget not in ik_names:
						ik_names.append(c.subtarget)

	groups_names_1 = [("ＩＫ", ik_names), ("髪", hair_names), ("頭", head_names),  ("スカト", skirt_names)]
	groups_names_2 = [("Root", root_names), ("指", finger_names),  ("体", body_names)]

	bpy.context.scene.objects.active = root
	for g in My_Display_Panel_Groups:
		if g[1] not in bpy.context.active_object.mmd_root.display_item_frames.keys():
			group = bpy.context.active_object.mmd_root.display_item_frames.add()
			group.name = g[1]
			group.name_e = g[0]


	for b in armature_object.data.bones.keys():
		for g in groups_names_1:
			for n in g[1]:
				if n in b:
					if b not in __items(root.mmd_root.display_item_frames[g[0]]).keys():
						if b not in items_added:
							item = __items(root.mmd_root.display_item_frames[g[0]]).add()
							item.name = b
							items_added.append(b)

	for b in armature_object.data.bones.keys():
		for g in groups_names_2:
			for n in g[1]:
				if n == b:
					if b not in __items(root.mmd_root.display_item_frames[g[0]]).keys():
						item = __items(root.mmd_root.display_item_frames[g[0]]).add()
						item.name = b
						items_added.append(b)

	for b in armature_object.data.bones.keys():
		if b not in items_added:
			if "shadow" not in b and "dummy" not in b:
				if b not in __items(root.mmd_root.display_item_frames[g[0]]).keys():
					item = __items(root.mmd_root.display_item_frames["Other"]).add()
					item.name = b
					items_added.append(b)


	# finger_names = ["finger", "Finger", "指", "thumb", "Thumb", "index", "Index", "mid", "Mid", "middle", "Middle", "Ring", "ring", "Pinky", "pinky", "Fore", "fore", "little", "Little", "Third", "third", "親指", "人指", "中指", "薬指", "小指", "palm"] #not forearm

def main(context):
	armature_object = model.findArmature(bpy.context.active_object)
	bpy.context.scene.objects.active = armature_object
	if model.findRoot(bpy.context.active_object) is None:
		bpy.ops.mmd_tools.convert_to_mmd_model()
	root = model.findRoot(bpy.context.active_object)
	mesh_objects_list = model.findMeshesList(bpy.context.active_object)

	if bpy.context.scene.display_panel_options == 'no_change':
		pass
	if bpy.context.scene.display_panel_options == 'display_panel_groups_from_bone_groups':
		clear_display_panel_groups(root)
		display_panel_groups_from_bone_groups(root, armature_object)
		display_panel_groups_from_shape_keys(mesh_objects_list)
		display_panel_groups_non_vertex_morphs(root)
		delete_empty_display_panel_groups(root)
	if bpy.context.scene.display_panel_options == 'add_display_panel_groups':
		clear_display_panel_groups(root)
		display_panel_groups_create(root, armature_object)
		display_panel_groups_from_shape_keys(mesh_objects_list)
		display_panel_groups_non_vertex_morphs(root)
		delete_empty_display_panel_groups(root)

@register_wrap
class MmdToolsDisplayPanelGroups(bpy.types.Operator):
	"""Mass add bone names and shape key names to display panel groups"""
	bl_idname = "object.add_display_panel_groups"
	bl_label = "Create Display Panel Groups and Add Items"

	bpy.types.Scene.display_panel_options = bpy.props.EnumProperty(items = [('no_change', 'No Change', 'Make no changes to display panel groups'), ('display_panel_groups_from_bone_groups', 'Display Panel Groups from Bone Groups', 'Add Display Panel Groups from Bone Groups'), ('add_display_panel_groups', 'Add Display Panel Groups', 'Display panel groups and items are created and added by this add-on')], name = "MMD Display Panel Groups :", default = 'no_change')

	@classmethod
	def poll(cls, context):
		return context.active_object is not None

	def execute(self, context):
		main(context)
		return {'FINISHED'}
