
# Overview
This repository contains a script that interacts with an ActionGraph located at a specific path within an Omniverse Stage. Using the script editor, you can programmatically:

- **Create Graph Nodes**: Instantiate various nodes (such as playback tick nodes, ROS2 context, render product nodes, and camera helper nodes).
- **Insert Values**: Set specific values like namespaces, frame IDs, topic names, and dimensions.
- **Connect Nodes**: Establish connections between nodes so that the output of one feeds into the input of another, ensuring proper data flow.
---
# Visual Explanation
## Scene Setup (First Screenshot)

![Screenshot from 2025-03-16 19-32-44](https://github.com/user-attachments/assets/e0b42ea0-416b-407e-a002-0b818169f156)

This screenshot shows the scene within the Omniverse Stage where the ActionGraph is located.

## Output After Execution (Second Screenshot)

![Screenshot from 2025-03-16 19-33-01](https://github.com/user-attachments/assets/2c5da825-3274-4d1c-bb45-d4a45afbf559)

After running the script, this output displays the newly created graph nodes with their respective connections and values, as configured by the script.

---

# Code Explanation
The code below is the actual script executed via the script editor. It utilizes the og.Controller.edit function with three main sections:

1. **CREATE_NODES**:<br>
This section lists all the nodes that are created, including nodes for playback ticks, ROS2 context, rendering, and camera publishing.
(For example, the node 'on_playback_tick' of type 'omni.graph.action.OnPlaybackTick' is created to trigger actions on every playback tick.)

2. **CONNECT**:<br>
Here, the script defines how nodes are connected. It establishes the flow between nodes, such as routing the output of the playback tick to the execution input of rendering nodes, and linking ROS2 context outputs to camera helper inputs.
(For instance, the output of 'isaac_run_one_simualtion_frame' is connected to trigger rendering on the left and right cameras.)

3. **SET_VALUES**:<br>
This section assigns specific configuration values to the nodes. It sets dimensions (e.g., width and height for render products), namespaces, frame IDs, topic names, and other parameters to ensure each node operates as expected.
(For example, the left camera’s namespace is set to `front_stereo_camera/left` and its render dimensions to `640x480`.)

``` python
import omni.graph.core as og

og.Controller.edit(
    {"graph_path": "/World/ActionGraph", "evaluator_name": "execution"},
    {
        og.Controller.Keys.CREATE_NODES: [
            ('on_playback_tick', 'omni.graph.action.OnPlaybackTick'),
            ('ros2_context', 'omni.isaac.ros2_bridge.ROS2Context'),
            ('left_camera_namespace', 'omni.graph.nodes.ConstantString'),
            ('left_camera_render_product', 'omni.isaac.core_nodes.IsaacCreateRenderProduct'),
            ('right_camera_render_product', 'omni.isaac.core_nodes.IsaacCreateRenderProduct'),
            ('right_camera_publish_camera_info', 'omni.isaac.ros2_bridge.ROS2CameraHelper'),
            ('left_camera_publish_camera_info', 'omni.isaac.ros2_bridge.ROS2CameraHelper'),
            ('left_camera_publish_image', 'omni.isaac.ros2_bridge.ROS2CameraHelper'),
            ('right_camera_namespace', 'omni.graph.nodes.ConstantString'),
            ('right_camera_publish_image', 'omni.isaac.ros2_bridge.ROS2CameraHelper'),
            ('right_camera_frame_id', 'omni.graph.nodes.ConstantString'),
            ('left_camera_frame_id', 'omni.graph.nodes.ConstantString'),
            ('isaac_read_simulation_time', 'omni.isaac.core_nodes.IsaacReadSimulationTime'),
            ('isaac_run_one_simualtion_frame', 'omni.isaac.core_nodes.OgnIsaacRunOneSimulationFrame'),
            ('left_camera_publish_depth', 'omni.isaac.ros2_bridge.ROS2CameraHelper'),
            ('left_camera_publish_semantics', 'omni.isaac.ros2_bridge.ROS2CameraHelper'),
            ('left_camera_publish_depth_camera_info', 'omni.isaac.ros2_bridge.ROS2CameraHelper'),
        ],

        og.Controller.Keys.CONNECT: [
            ('isaac_run_one_simualtion_frame.outputs:step', 'left_camera_render_product.inputs:execIn'),
            ('on_playback_tick.outputs:tick', 'left_camera_render_product.inputs:execIn'),
            ('isaac_run_one_simualtion_frame.outputs:step', 'right_camera_render_product.inputs:execIn'),
            ('on_playback_tick.outputs:tick', 'right_camera_render_product.inputs:execIn'),
            ('ros2_context.outputs:context', 'right_camera_publish_camera_info.inputs:context'),
            ('right_camera_render_product.outputs:execOut', 'right_camera_publish_camera_info.inputs:execIn'),
            ('right_camera_frame_id.inputs:value', 'right_camera_publish_camera_info.inputs:frameId'),
            ('right_camera_namespace.inputs:value', 'right_camera_publish_camera_info.inputs:nodeNamespace'),
            ('right_camera_render_product.outputs:renderProductPath', 'right_camera_publish_camera_info.inputs:renderProductPath'),
            ('ros2_context.outputs:context', 'left_camera_publish_camera_info.inputs:context'),
            ('left_camera_render_product.outputs:execOut', 'left_camera_publish_camera_info.inputs:execIn'),
            ('left_camera_frame_id.inputs:value', 'left_camera_publish_camera_info.inputs:frameId'),
            ('left_camera_namespace.inputs:value', 'left_camera_publish_camera_info.inputs:nodeNamespace'),
            ('left_camera_render_product.outputs:renderProductPath', 'left_camera_publish_camera_info.inputs:renderProductPath'),
            ('ros2_context.outputs:context', 'left_camera_publish_image.inputs:context'),
            ('left_camera_render_product.outputs:execOut', 'left_camera_publish_image.inputs:execIn'),
            ('left_camera_frame_id.inputs:value', 'left_camera_publish_image.inputs:frameId'),
            ('left_camera_namespace.inputs:value', 'left_camera_publish_image.inputs:nodeNamespace'),
            ('left_camera_render_product.outputs:renderProductPath', 'left_camera_publish_image.inputs:renderProductPath'),
            ('ros2_context.outputs:context', 'right_camera_publish_image.inputs:context'),
            ('right_camera_render_product.outputs:execOut', 'right_camera_publish_image.inputs:execIn'),
            ('right_camera_frame_id.inputs:value', 'right_camera_publish_image.inputs:frameId'),
            ('right_camera_namespace.inputs:value', 'right_camera_publish_image.inputs:nodeNamespace'),
            ('right_camera_render_product.outputs:renderProductPath', 'right_camera_publish_image.inputs:renderProductPath'),
            ('on_playback_tick.outputs:tick', 'isaac_run_one_simualtion_frame.inputs:execIn'),
            ('ros2_context.outputs:context', 'left_camera_publish_depth.inputs:context'),
            ('left_camera_render_product.outputs:execOut', 'left_camera_publish_depth.inputs:execIn'),
            ('left_camera_frame_id.inputs:value', 'left_camera_publish_depth.inputs:frameId'),
            ('left_camera_render_product.outputs:renderProductPath', 'left_camera_publish_depth.inputs:renderProductPath'),
            ('ros2_context.outputs:context', 'left_camera_publish_semantics.inputs:context'),
            ('left_camera_render_product.outputs:execOut', 'left_camera_publish_semantics.inputs:execIn'),
            ('left_camera_frame_id.inputs:value', 'left_camera_publish_semantics.inputs:frameId'),
            ('left_camera_render_product.outputs:renderProductPath', 'left_camera_publish_semantics.inputs:renderProductPath'),
            ('ros2_context.outputs:context', 'left_camera_publish_depth_camera_info.inputs:context'),
            ('left_camera_render_product.outputs:execOut', 'left_camera_publish_depth_camera_info.inputs:execIn'),
            ('left_camera_frame_id.inputs:value', 'left_camera_publish_depth_camera_info.inputs:frameId'),
            ('left_camera_render_product.outputs:renderProductPath', 'left_camera_publish_depth_camera_info.inputs:renderProductPath'),
        ],

        og.Controller.Keys.SET_VALUES: [
            ('left_camera_namespace.inputs:value', 'front_stereo_camera/left'),
            ('left_camera_render_product.inputs:height', 480),
            ('left_camera_render_product.inputs:width', 640),
            ('right_camera_render_product.inputs:height', 480),
            ('right_camera_render_product.inputs:width', 640),
            ('right_camera_publish_camera_info.inputs:stereoOffset', Gf.Vec2f(-143.89889526367188, 0.0)),
            ('right_camera_publish_camera_info.inputs:topicName', 'camera_info'),
            ('right_camera_publish_camera_info.inputs:type', 'camera_info'),
            ('left_camera_publish_camera_info.inputs:topicName', 'camera_info'),
            ('left_camera_publish_camera_info.inputs:type', 'camera_info'),
            ('left_camera_publish_image.inputs:topicName', 'image_raw'),
            ('right_camera_namespace.inputs:value', 'front_stereo_camera/right'),
            ('right_camera_publish_image.inputs:topicName', 'image_raw'),
            ('right_camera_frame_id.inputs:value', 'front_stereo_camera:right_rgb'),
            ('left_camera_frame_id.inputs:value', 'front_stereo_camera:left_rgb'),
            ('left_camera_publish_depth.inputs:nodeNamespace', 'front_stereo_camera/depth'),
            ('left_camera_publish_depth.inputs:topicName', 'ground_truth'),
            ('left_camera_publish_depth.inputs:type', 'depth'),
            ('left_camera_publish_semantics.inputs:enableSemanticLabels', True),
            ('left_camera_publish_semantics.inputs:nodeNamespace', 'front_stereo_camera/semantics'),
            ('left_camera_publish_semantics.inputs:topicName', 'ground_truth'),
            ('left_camera_publish_semantics.inputs:type', 'semantic_segmentation'),
            ('left_camera_publish_depth_camera_info.inputs:nodeNamespace', 'front_stereo_camera/depth'),
            ('left_camera_publish_depth_camera_info.inputs:topicName', 'camera_info'),
            ('left_camera_publish_depth_camera_info.inputs:type', 'camera_info'),
        ],
    },
)
```
---
This code is executed in the Omniverse Stage’s script editor. It automates the setup of an ActionGraph by creating nodes, setting up their parameters, and establishing the necessary connections between them, as demonstrated by the screenshots above.
