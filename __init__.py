import bpy
import os
import glob
import bpy_extras

from . import geo_nodes


def find_beamng_user_folder():
    path = r"~\AppData\Local\BeamNG.drive"
    expanded_path = os.path.expanduser(path)
    if expanded_path != path:
        return expanded_path
    else:
        return ""

def _log(*args):
    print("beamng_gltf_sequence.import:", *args)

class ImportBeamNGglTFSequence(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):
    """Import BeamNG glTF Sequence"""  # Use this as a tooltip for menu items and buttons.

    bl_idname = "beamng_gltf_sequence.import"  # Unique identifier for buttons and menu items to reference.
    bl_label = "Import BeamNG glTF Sequence"  # Display name in the interface.
    bl_options = {"REGISTER", "UNDO"}  # Enable undo for the operator.

    filter_glob: bpy.props.StringProperty(default="*.glb;*.gltf", options={'HIDDEN'})  # type: ignore

    files: bpy.props.CollectionProperty(
        name="File Path",
        type=bpy.types.OperatorFileListElement,
    )  # type: ignore

    name: bpy.props.StringProperty(
        name="Sequence Name",
        default="vehicle",
        description="Name to give this sequence",
        ) # type: ignore
    join_meshes: bpy.props.BoolProperty(
        name="Join Meshes",
        default=True,
        description="Join objects into a single mesh per frame",
        ) # type: ignore
    only_selected: bpy.props.BoolProperty(
        name="Only Selected Frames",
        default=False,
        description="Limit the sequence to just the chosen files",
        ) # type: ignore
    find_textures: bpy.props.BoolProperty(
        name="Locate Textures in BeamNG User Folder",
        default=True,
        description="Search in the BeamNG user folder for any textures referenced in the glTF files",
        ) # type: ignore
    beamng_user_folder: bpy.props.StringProperty(
        name="BeamNG User Folder",
        subtype='DIR_PATH',
        default=find_beamng_user_folder(),
        description="Path to your user folder for the purpose of finding textures",
        ) # type: ignore

    def draw(self, context):
        layout = self.layout

        subrow = layout.row()
        subrow.use_property_split = True
        subrow.prop(self, 'name')
        layout.prop(self, 'join_meshes')
        layout.prop(self, 'only_selected')
        layout.prop(self, 'find_textures')
        subrow = layout.row()
        subrow.active = self.find_textures
        subrow.prop(self, "beamng_user_folder", text="")

    def execute(self, context):
        scene = context.scene

        name = self.name
        join_meshes = self.join_meshes

        dirname = os.path.dirname(self.filepath)
        if self.only_selected:
            filepaths = [os.path.join(dirname, f.name) for f in self.files]
        else:
            import re
            # Glob frame number to get whole sequence.
            # Assumes frame number is the last group of digits in the filename
            filename = bpy.path.basename(self.filepath)
            pattern = re.sub(r"\d+", "*", filename[::-1], count=1)[::-1]
            filepaths = sorted(glob.glob(os.path.join(dirname, pattern)))

        file_count = len(filepaths)
        if not file_count:
            self.report(
                {'ERROR'}, f"No glTF files found in the chosen directory."
            )
            return {'CANCELLED'}

        progress_steps = file_count + 1
        context.window_manager.progress_begin(0, progress_steps)

        sequence_collection = bpy.data.collections.new(name=f"{name} sequence")
        scene.collection.children.link(sequence_collection)
        sequence_collection.hide_render = True

        prior_materials = set(bpy.data.materials.values())
        keep_materials = set()
        prior_images = set(bpy.data.images.values())
        keep_images = set()

        for i, filepath in enumerate(filepaths):
            filename = os.path.splitext(bpy.path.basename(filepath))[0]

            bpy.ops.import_scene.gltf(filepath=filepath, import_pack_images=False)
            context.window_manager.progress_update(i + 0.5)

            if join_meshes:
                bpy.ops.object.parent_clear(type="CLEAR_KEEP_TRANSFORM")
            else:
                # Rename root empty
                context.active_object.name = f"{name}_{filename}"
                new_name = context.active_object.name
                frame_collection = bpy.data.collections.new(name=new_name)
                sequence_collection.children.link(frame_collection)

            # Add objects to collection
            mesh_active = False
            imported_objects = context.selected_objects
            if join_meshes:
                imported_meshes = [o.data for o in imported_objects if o.type=='MESH']
            for o in imported_objects:
                if join_meshes:
                    if o.type == "EMPTY":
                        bpy.data.objects.remove(o, do_unlink=True)
                        continue
                    sequence_collection.objects.link(o)
                    scene.collection.objects.unlink(o)
                    if not mesh_active and o.type == "MESH":
                        context.view_layer.objects.active = o
                        mesh_active = True
                else:
                    frame_collection.objects.link(o)
                    scene.collection.objects.unlink(o)

            if join_meshes:
                bpy.ops.object.join()

                for mesh in imported_meshes:
                    if mesh.users == 0:
                        bpy.data.meshes.remove(mesh)

                context.active_object.name = f"{name}_{filename}"

            # The rest of the loop checks for duplicate materials/images being imported
            # and merges them. Could be faster without the sets but it works for now.
            if i == 0:  # first frame
                keep_materials = set(bpy.data.materials) - prior_materials
                keep_images = set(bpy.data.images.values()) - prior_images
            else:
                new_materials = (
                    set(bpy.data.materials.values()) - prior_materials - keep_materials
                )
                new_images = set(bpy.data.images.values()) - prior_images - keep_images

                # map from duplicates to originals
                material_dupes = {
                    m_new: m_og
                    for m_new in new_materials
                    for m_og in keep_materials
                    if os.path.splitext(m_new.name)[0] == os.path.splitext(m_og.name)[0]
                    # compare material names without duplicate suffix
                }
                image_dupes = {
                    i_new: i_og
                    for i_new in new_images
                    for i_og in keep_images
                    if os.path.splitext(i_new.name)[0] == i_og.name
                }

                for m_new, m_og in material_dupes.items():
                    m_new.user_remap(m_og)
                    bpy.data.materials.remove(m_new)
                for i_new, i_og in image_dupes.items():
                    i_new.user_remap(i_og)
                    bpy.data.images.remove(i_new)

                keep_materials |= new_materials - material_dupes.keys()
                keep_images |= new_images - image_dupes.keys()

            context.window_manager.progress_update(i + 1)
            _log(f"Imported frame '{filename}' ({i+1} / {file_count}).")

        context.window_manager.progress_update(progress_steps - 0.5)
        _log("Finished importing glTF files. Creating instancer object")

        context.view_layer.layer_collection.children[
            sequence_collection.name
        ].exclude = True

        # Set up the instancer for the collection
        vert = bpy.data.meshes.new(name=f"{name}_instancer")
        vert.vertices.add(1)
        instancer_obj = bpy_extras.object_utils.object_data_add(
            context, vert, name=name
        )
        for mat in keep_materials:
            instancer_obj.data.materials.append(mat)

        modifier: bpy.types.NodesModifier = instancer_obj.modifiers.new(
            name="GeometryNodes", type="NODES"
        )
        modifier.node_group = geo_nodes.instance_mesh_sequence_node_group()
        modifier["Socket_2"] = sequence_collection

        if self.find_textures:
            _log(f"Searching for missing textures in '{self.beamng_user_folder}' ...")
            result = bpy.ops.file.find_missing_files(directory=self.beamng_user_folder, filter_image=True)
            _log(f"Finished searching. (returned {result})")

        context.window_manager.progress_end()
        self.report({"INFO"}, f"Imported glTF sequence '{name}' ({file_count} frames)")
        _log(f"Finished")

        return {'FINISHED'}


def menu_func_import(self, context):
    self.layout.operator(ImportBeamNGglTFSequence.bl_idname, text="BeamNG glTF Sequence (.glb/.gltf)")


def register():
    bpy.utils.register_class(ImportBeamNGglTFSequence)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

def unregister():
    bpy.utils.unregister_class(ImportBeamNGglTFSequence)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
