# code generated using https://github.com/BrendanParmer/NodeToPython

import bpy

# initialize instance_mesh_sequence node group
def instance_mesh_sequence_node_group():
    node_group_name = "Instance Mesh Sequence"
    instance_mesh_sequence = bpy.data.node_groups.get(node_group_name)
    if instance_mesh_sequence:
        return instance_mesh_sequence
    else:
        instance_mesh_sequence = bpy.data.node_groups.new(
            type="GeometryNodeTree", name=node_group_name
        )
        instance_mesh_sequence.use_fake_user = True

    instance_mesh_sequence.color_tag = "NONE"
    instance_mesh_sequence.description = ""

    instance_mesh_sequence.is_modifier = True

    # instance_mesh_sequence interface
    # Socket Geometry
    geometry_socket = instance_mesh_sequence.interface.new_socket(
        name="Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry"
    )
    geometry_socket.attribute_domain = "POINT"

    # Socket Geometry
    geometry_socket_1 = instance_mesh_sequence.interface.new_socket(
        name="Geometry", in_out="INPUT", socket_type="NodeSocketGeometry"
    )
    geometry_socket_1.attribute_domain = "POINT"

    # Socket Sequence
    sequence_socket = instance_mesh_sequence.interface.new_socket(
        name="Sequence", in_out="INPUT", socket_type="NodeSocketCollection"
    )
    sequence_socket.attribute_domain = "POINT"
    sequence_socket.description = "Collection containing each frame as a child"

    # Socket Frame Offset
    frame_offset_socket = instance_mesh_sequence.interface.new_socket(
        name="Frame Offset", in_out="INPUT", socket_type="NodeSocketInt"
    )
    frame_offset_socket.default_value = 1
    frame_offset_socket.min_value = -2147483648
    frame_offset_socket.max_value = 2147483647
    frame_offset_socket.subtype = "NONE"
    frame_offset_socket.attribute_domain = "POINT"
    frame_offset_socket.force_non_field = True
    frame_offset_socket.description = "Number of frames to offset the animation"

    # Socket Animation
    animation_socket = instance_mesh_sequence.interface.new_socket(
        name="Animation", in_out="INPUT", socket_type="NodeSocketMenu"
    )
    animation_socket.attribute_domain = "POINT"
    animation_socket.force_non_field = True
    animation_socket.description = "Behaviour for frames outside the sequence"

    # Socket Realize Instances
    realize_instances_socket = instance_mesh_sequence.interface.new_socket(
        name="Realize Instances", in_out="INPUT", socket_type="NodeSocketBool"
    )
    realize_instances_socket.default_value = False
    realize_instances_socket.attribute_domain = "POINT"
    realize_instances_socket.force_non_field = True
    realize_instances_socket.description = "Convert instances into real geometry data. Use when exporting to another format such as Alembic"

    # initialize instance_mesh_sequence nodes
    # node Group Input
    group_input = instance_mesh_sequence.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.outputs[0].hide = True
    group_input.outputs[3].hide = True
    group_input.outputs[4].hide = True
    group_input.outputs[5].hide = True

    # node Group Output
    group_output = instance_mesh_sequence.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    # node Collection Info
    collection_info = instance_mesh_sequence.nodes.new("GeometryNodeCollectionInfo")
    collection_info.name = "Collection Info"
    collection_info.transform_space = "ORIGINAL"
    # Separate Children
    collection_info.inputs[1].default_value = True
    # Reset Children
    collection_info.inputs[2].default_value = False

    # node Instance on Points
    instance_on_points = instance_mesh_sequence.nodes.new(
        "GeometryNodeInstanceOnPoints"
    )
    instance_on_points.name = "Instance on Points"
    # Selection
    instance_on_points.inputs[1].default_value = True
    # Pick Instance
    instance_on_points.inputs[3].default_value = True
    # Rotation
    instance_on_points.inputs[5].default_value = (0.0, 0.0, 0.0)
    # Scale
    instance_on_points.inputs[6].default_value = (1.0, 1.0, 1.0)

    # node Scene Time
    scene_time = instance_mesh_sequence.nodes.new("GeometryNodeInputSceneTime")
    scene_time.name = "Scene Time"

    # node Realize Instances
    realize_instances = instance_mesh_sequence.nodes.new("GeometryNodeRealizeInstances")
    realize_instances.name = "Realize Instances"
    # Selection
    realize_instances.inputs[1].default_value = True
    # Depth
    realize_instances.inputs[3].default_value = 3

    # node Math
    math = instance_mesh_sequence.nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.operation = "SUBTRACT"
    math.use_clamp = False

    # node Domain Size
    domain_size = instance_mesh_sequence.nodes.new("GeometryNodeAttributeDomainSize")
    domain_size.name = "Domain Size"
    domain_size.component = "INSTANCES"

    # node Clamp
    clamp = instance_mesh_sequence.nodes.new("ShaderNodeClamp")
    clamp.name = "Clamp"
    clamp.clamp_type = "MINMAX"
    # Min
    clamp.inputs[1].default_value = 0.0

    # node Math.001
    math_001 = instance_mesh_sequence.nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.operation = "SUBTRACT"
    math_001.use_clamp = False
    # Value_001
    math_001.inputs[1].default_value = 1.0

    # node Group Input.001
    group_input_001 = instance_mesh_sequence.nodes.new("NodeGroupInput")
    group_input_001.name = "Group Input.001"
    group_input_001.outputs[1].hide = True
    group_input_001.outputs[2].hide = True
    group_input_001.outputs[3].hide = True
    group_input_001.outputs[4].hide = True
    group_input_001.outputs[5].hide = True

    # node Group Input.002
    group_input_002 = instance_mesh_sequence.nodes.new("NodeGroupInput")
    group_input_002.name = "Group Input.002"
    group_input_002.outputs[0].hide = True
    group_input_002.outputs[1].hide = True
    group_input_002.outputs[2].hide = True
    group_input_002.outputs[3].hide = True
    group_input_002.outputs[5].hide = True

    # node Frame.001
    frame_001 = instance_mesh_sequence.nodes.new("NodeFrame")
    frame_001.label = "Credit: https://www.youtube.com/watch?v=KRxDyloJRYU"
    frame_001.name = "Frame.001"
    frame_001.label_size = 20
    frame_001.shrink = True

    # node Group Input.004
    group_input_004 = instance_mesh_sequence.nodes.new("NodeGroupInput")
    group_input_004.name = "Group Input.004"
    group_input_004.outputs[0].hide = True
    group_input_004.outputs[1].hide = True
    group_input_004.outputs[2].hide = True
    group_input_004.outputs[4].hide = True
    group_input_004.outputs[5].hide = True

    # node Menu Switch
    menu_switch = instance_mesh_sequence.nodes.new("GeometryNodeMenuSwitch")
    menu_switch.name = "Menu Switch"
    menu_switch.active_index = 1
    menu_switch.data_type = "INT"
    menu_switch.enum_items.clear()
    menu_switch.enum_items.new("Hold")
    menu_switch.enum_items[0].description = (
        "Clamp frames to start and end frames outside the sequence"
    )
    menu_switch.enum_items.new("Loop")
    menu_switch.enum_items[1].description = "Repeat frames outside the sequence"

    # Set locations
    group_input.location = (-1048.4385986328125, 134.9766845703125)
    group_output.location = (973.54443359375, 396.22882080078125)
    collection_info.location = (-834.4934692382812, 282.4392395019531)
    instance_on_points.location = (357.0714111328125, 380.6262512207031)
    scene_time.location = (-625.5517578125, -52.00232696533203)
    realize_instances.location = (708.6776123046875, 415.5988464355469)
    math.location = (-430.8601379394531, -24.98596954345703)
    domain_size.location = (-617.642333984375, 130.23944091796875)
    clamp.location = (-225.28109741210938, 169.56639099121094)
    math_001.location = (-432.2638854980469, 143.6768035888672)
    group_input_001.location = (142.75198364257812, 371.1800231933594)
    group_input_002.location = (533.3222045898438, 326.7039489746094)
    frame_001.location = (-656.0782470703125, 465.47869873046875)
    group_input_004.location = (-19.813791275024414, 169.25872802734375)
    menu_switch.location = (152.92529296875, 130.54965209960938)

    # Set dimensions
    group_input.width, group_input.height = 140.0, 100.0
    group_output.width, group_output.height = 140.0, 100.0
    collection_info.width, collection_info.height = 140.0, 100.0
    instance_on_points.width, instance_on_points.height = 140.0, 100.0
    scene_time.width, scene_time.height = 140.0, 100.0
    realize_instances.width, realize_instances.height = 140.0, 100.0
    math.width, math.height = 140.0, 100.0
    domain_size.width, domain_size.height = 140.0, 100.0
    clamp.width, clamp.height = 140.0, 100.0
    math_001.width, math_001.height = 140.0, 100.0
    group_input_001.width, group_input_001.height = 140.0, 100.0
    group_input_002.width, group_input_002.height = 140.0, 100.0
    frame_001.width, frame_001.height = 591.3014526367188, 52.82861328125
    group_input_004.width, group_input_004.height = 140.0, 100.0
    menu_switch.width, menu_switch.height = 140.0, 100.0

    # initialize instance_mesh_sequence links
    # collection_info.Instances -> instance_on_points.Instance
    instance_mesh_sequence.links.new(
        collection_info.outputs[0], instance_on_points.inputs[2]
    )
    # realize_instances.Geometry -> group_output.Geometry
    instance_mesh_sequence.links.new(
        realize_instances.outputs[0], group_output.inputs[0]
    )
    # group_input.Sequence -> collection_info.Collection
    instance_mesh_sequence.links.new(group_input.outputs[1], collection_info.inputs[0])
    # instance_on_points.Instances -> realize_instances.Geometry
    instance_mesh_sequence.links.new(
        instance_on_points.outputs[0], realize_instances.inputs[0]
    )
    # scene_time.Frame -> math.Value
    instance_mesh_sequence.links.new(scene_time.outputs[1], math.inputs[0])
    # group_input.Frame Offset -> math.Value
    instance_mesh_sequence.links.new(group_input.outputs[2], math.inputs[1])
    # collection_info.Instances -> domain_size.Geometry
    instance_mesh_sequence.links.new(collection_info.outputs[0], domain_size.inputs[0])
    # math_001.Value -> clamp.Max
    instance_mesh_sequence.links.new(math_001.outputs[0], clamp.inputs[2])
    # math.Value -> clamp.Value
    instance_mesh_sequence.links.new(math.outputs[0], clamp.inputs[0])
    # domain_size.Instance Count -> math_001.Value
    instance_mesh_sequence.links.new(domain_size.outputs[5], math_001.inputs[0])
    # group_input_001.Geometry -> instance_on_points.Points
    instance_mesh_sequence.links.new(
        group_input_001.outputs[0], instance_on_points.inputs[0]
    )
    # group_input_002.Realize Instances -> realize_instances.Realize All
    instance_mesh_sequence.links.new(
        group_input_002.outputs[4], realize_instances.inputs[2]
    )
    # group_input_004.Animation -> menu_switch.Menu
    instance_mesh_sequence.links.new(group_input_004.outputs[3], menu_switch.inputs[0])
    # clamp.Result -> menu_switch.Hold
    instance_mesh_sequence.links.new(clamp.outputs[0], menu_switch.inputs[1])
    # math.Value -> menu_switch.Loop
    instance_mesh_sequence.links.new(math.outputs[0], menu_switch.inputs[2])
    # menu_switch.Output -> instance_on_points.Instance Index
    instance_mesh_sequence.links.new(
        menu_switch.outputs[0], instance_on_points.inputs[4]
    )

    animation_socket.default_value = "Hold"  # nodes need to be connected first

    return instance_mesh_sequence
