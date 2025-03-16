import omni.graph.core as og
import omni.usd
from pxr import Usd, Sdf

def extract_omnigraph_config():
    stage = omni.usd.get_context().get_stage()
    omnigraph_path = "/World/ActionGraph"
    omnigraph_prim = stage.GetPrimAtPath(omnigraph_path)
    if not omnigraph_prim or not omnigraph_prim.IsValid():
        print(f"OmniGraph prim not found at path: {omnigraph_path}")
        return None

    create_nodes = []
    connections = []
    set_values = []

    def traverse_node(prim):
        node_type_attr = prim.GetAttribute("node:type")
        if node_type_attr and node_type_attr.HasAuthoredValue():
            node_name = prim.GetName()
            node_type = node_type_attr.Get() if node_type_attr.HasAuthoredValue() else prim.GetTypeName()
            create_nodes.append((node_name, node_type))
            for attr in prim.GetAttributes():
                if attr.GetName().startswith("inputs:"):
                    conns = attr.GetConnections()
                    if conns:
                        for conn in conns:
                            conn_str = str(conn)  # 예: "/World/ActionGraph/OnPlaybackTick.outputs:tick"
                            parts = conn_str.split('/')
                            source_port = parts[-1] if parts else conn_str
                            dest_port = f"{node_name}.{attr.GetName()}"  # 예: "PublishJointState.inputs:execIn"
                            connections.append((source_port, dest_port))
                    else:
                        if attr.HasAuthoredValue():
                            value = attr.Get()
                            set_values.append((f"{node_name}.{attr.GetName()}", value))
        for child in prim.GetChildren():
            traverse_node(child)

    for child in omnigraph_prim.GetChildren():
        traverse_node(child)

    config = {
        og.Controller.Keys.CREATE_NODES: create_nodes,
        og.Controller.Keys.CONNECT: connections,
        og.Controller.Keys.SET_VALUES: set_values,
    }
    return config

def format_config_string(config):
    result = "import omni.graph.core as og\n\n"
    result += "og.Controller.edit(\n"
    result += "    {\"graph_path\": \"/World/ActionGraph\", \"evaluator_name\": \"execution\"},\n"
    result += "    {\n"

    result += "        og.Controller.Keys.CREATE_NODES: [\n"
    for node in config.get(og.Controller.Keys.CREATE_NODES, []):
        result += f"            {node},\n"
    result += "        ],\n\n"

    result += "        og.Controller.Keys.CONNECT: [\n"
    for conn in config.get(og.Controller.Keys.CONNECT, []):
        result += f"            {conn},\n"
    result += "        ],\n\n"

    result += "        og.Controller.Keys.SET_VALUES: [\n"
    for set_val in config.get(og.Controller.Keys.SET_VALUES, []):
        result += f"            {set_val},\n"
    result += "        ],\n"

    result += "    },\n"
    result += ")\n"
    return result

def main():
    config = extract_omnigraph_config()
    if config:
        formatted_str = format_config_string(config)
        print("Generated OmniGraph configuration:\n")
        print(formatted_str)
    else:
        print("No configuration extracted.")

if __name__ == '__main__':
    main()
