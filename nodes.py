import json


class NodeIDModifier:
    CATEGORY = "utils/ID Tools"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "workflow_json": ("STRING", {"multiline": True, "default": "{}"}),
                "old_node_id": ("STRING", {"default": ""}),
                "new_node_id": ("STRING", {"default": ""}),
            },
            "optional": {
                "id_mapping": ("STRING", {"multiline": True, "default": "{}"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("modified_workflow",)
    FUNCTION = "modify_node_id"
    OUTPUT_NODE = False

    def modify_node_id(self, workflow_json, old_node_id, new_node_id, id_mapping="{}"):
        try:
            workflow = json.loads(workflow_json)
        except json.JSONDecodeError:
            return (json.dumps({"error": "Invalid JSON format in workflow_json"}, indent=2),)

        try:
            mapping = json.loads(id_mapping) if id_mapping.strip() else {}
        except json.JSONDecodeError:
            mapping = {}

        if old_node_id and new_node_id:
            mapping[str(old_node_id)] = str(new_node_id)

        if not mapping:
            return (json.dumps(workflow, indent=2),)

        modified_workflow = self._rename_node_ids(workflow, mapping)

        return (json.dumps(modified_workflow, indent=2),)

    def _rename_node_ids(self, workflow, id_mapping):
        if isinstance(workflow, dict):
            if "nodes" in workflow and "links" in workflow:
                return self._process_ui_format(workflow, id_mapping)
            else:
                return self._process_api_format(workflow, id_mapping)
        return workflow

    def _process_api_format(self, workflow, id_mapping):
        result = {}
        for key, value in workflow.items():
            new_key = id_mapping.get(key, key)
            
            if isinstance(value, dict):
                result[new_key] = self._process_dict_recursive(value, id_mapping)
            else:
                result[new_key] = self._replace_id_in_value(value, id_mapping)
        return result

    def _process_ui_format(self, workflow, id_mapping):
        result = workflow.copy()
        
        if "nodes" in workflow:
            result["nodes"] = []
            for node in workflow["nodes"]:
                new_node = node.copy()
                if "id" in new_node and str(new_node["id"]) in id_mapping:
                    new_node["id"] = int(id_mapping[str(new_node["id"])])
                result["nodes"].append(self._process_dict_recursive(new_node, id_mapping))
        
        if "links" in workflow:
            result["links"] = []
            for link in workflow["links"]:
                new_link = list(link) if isinstance(link, (list, tuple)) else link
                if isinstance(new_link, list) and len(new_link) >= 5:
                    if str(new_link[1]) in id_mapping:
                        new_link[1] = int(id_mapping[str(new_link[1])])
                    if str(new_link[3]) in id_mapping:
                        new_link[3] = int(id_mapping[str(new_link[3])])
                result["links"].append(new_link)
        
        return result

    def _process_dict_recursive(self, d, id_mapping):
        result = {}
        for key, value in d.items():
            if isinstance(value, dict):
                result[key] = self._process_dict_recursive(value, id_mapping)
            elif isinstance(value, list):
                result[key] = self._process_list(value, id_mapping)
            else:
                result[key] = self._replace_id_in_value(value, id_mapping)
        return result

    def _process_list(self, lst, id_mapping):
        result = []
        for item in lst:
            if isinstance(item, list) and len(item) >= 2 and isinstance(item[0], str):
                if item[0] in id_mapping:
                    item = [id_mapping[item[0]]] + item[1:]
                result.append(item)
            elif isinstance(item, dict):
                result.append(self._process_dict_recursive(item, id_mapping))
            elif isinstance(item, str):
                result.append(id_mapping.get(item, item))
            else:
                result.append(item)
        return result

    def _replace_id_in_value(self, value, id_mapping):
        if isinstance(value, str):
            return id_mapping.get(value, value)
        return value


class BatchNodeIDModifier:
    CATEGORY = "utils/ID Tools"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "workflow_json": ("STRING", {"multiline": True, "default": "{}"}),
                "id_mapping": ("STRING", {"multiline": True, "default": "{}"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("modified_workflow",)
    FUNCTION = "batch_modify_node_ids"
    OUTPUT_NODE = False

    def batch_modify_node_ids(self, workflow_json, id_mapping="{}"):
        try:
            workflow = json.loads(workflow_json)
        except json.JSONDecodeError:
            return (json.dumps({"error": "Invalid JSON format in workflow_json"}, indent=2),)

        try:
            mapping = json.loads(id_mapping) if id_mapping.strip() else {}
        except json.JSONDecodeError:
            return (json.dumps({"error": "Invalid JSON format in id_mapping"}, indent=2),)

        if not mapping:
            return (json.dumps(workflow, indent=2),)

        modified_workflow = self._rename_node_ids(workflow, mapping)

        return (json.dumps(modified_workflow, indent=2),)

    def _rename_node_ids(self, workflow, id_mapping):
        if isinstance(workflow, dict):
            if "nodes" in workflow and "links" in workflow:
                return self._process_ui_format(workflow, id_mapping)
            else:
                return self._process_api_format(workflow, id_mapping)
        return workflow

    def _process_api_format(self, workflow, id_mapping):
        result = {}
        for key, value in workflow.items():
            new_key = id_mapping.get(key, key)
            
            if isinstance(value, dict):
                result[new_key] = self._process_dict_recursive(value, id_mapping)
            else:
                result[new_key] = self._replace_id_in_value(value, id_mapping)
        return result

    def _process_ui_format(self, workflow, id_mapping):
        result = workflow.copy()
        
        if "nodes" in workflow:
            result["nodes"] = []
            for node in workflow["nodes"]:
                new_node = node.copy()
                if "id" in new_node and str(new_node["id"]) in id_mapping:
                    new_node["id"] = int(id_mapping[str(new_node["id"])])
                result["nodes"].append(self._process_dict_recursive(new_node, id_mapping))
        
        if "links" in workflow:
            result["links"] = []
            for link in workflow["links"]:
                new_link = list(link) if isinstance(link, (list, tuple)) else link
                if isinstance(new_link, list) and len(new_link) >= 5:
                    if str(new_link[1]) in id_mapping:
                        new_link[1] = int(id_mapping[str(new_link[1])])
                    if str(new_link[3]) in id_mapping:
                        new_link[3] = int(id_mapping[str(new_link[3])])
                result["links"].append(new_link)
        
        return result

    def _process_dict_recursive(self, d, id_mapping):
        result = {}
        for key, value in d.items():
            if isinstance(value, dict):
                result[key] = self._process_dict_recursive(value, id_mapping)
            elif isinstance(value, list):
                result[key] = self._process_list(value, id_mapping)
            else:
                result[key] = self._replace_id_in_value(value, id_mapping)
        return result

    def _process_list(self, lst, id_mapping):
        result = []
        for item in lst:
            if isinstance(item, list) and len(item) >= 2 and isinstance(item[0], str):
                if item[0] in id_mapping:
                    item = [id_mapping[item[0]]] + item[1:]
                result.append(item)
            elif isinstance(item, dict):
                result.append(self._process_dict_recursive(item, id_mapping))
            elif isinstance(item, str):
                result.append(id_mapping.get(item, item))
            else:
                result.append(item)
        return result

    def _replace_id_in_value(self, value, id_mapping):
        if isinstance(value, str):
            return id_mapping.get(value, value)
        return value


class WorkflowIDNormalizer:
    CATEGORY = "utils/ID Tools"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "workflow_json": ("STRING", {"multiline": True, "default": "{}"}),
                "start_id": ("INT", {"default": 1, "min": 1, "max": 99999}),
                "step": ("INT", {"default": 1, "min": 1, "max": 100}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("normalized_workflow",)
    FUNCTION = "normalize_ids"
    OUTPUT_NODE = False

    def normalize_ids(self, workflow_json, start_id=1, step=1):
        try:
            workflow = json.loads(workflow_json)
        except json.JSONDecodeError:
            return (json.dumps({"error": "Invalid JSON format in workflow_json"}, indent=2),)

        if not isinstance(workflow, dict):
            return (json.dumps({"error": "Workflow must be a JSON object"}, indent=2),)

        id_mapping = {}
        if "nodes" in workflow and "links" in workflow:
            node_ids = sorted([str(n.get("id")) for n in workflow["nodes"] if "id" in n])
        else:
            node_ids = sorted([k for k in workflow.keys() if isinstance(k, str) and k.isdigit()])

        if not node_ids:
            return (json.dumps(workflow, indent=2),)

        current_id = start_id
        for old_id in node_ids:
            id_mapping[old_id] = str(current_id)
            current_id += step

        modified_workflow = self._rename_node_ids(workflow, id_mapping)

        return (json.dumps(modified_workflow, indent=2),)

    def _rename_node_ids(self, workflow, id_mapping):
        if isinstance(workflow, dict):
            if "nodes" in workflow and "links" in workflow:
                return self._process_ui_format(workflow, id_mapping)
            else:
                return self._process_api_format(workflow, id_mapping)
        return workflow

    def _process_api_format(self, workflow, id_mapping):
        result = {}
        for key, value in workflow.items():
            new_key = id_mapping.get(key, key)
            
            if isinstance(value, dict):
                result[new_key] = self._process_dict_recursive(value, id_mapping)
            else:
                result[new_key] = self._replace_id_in_value(value, id_mapping)
        return result

    def _process_ui_format(self, workflow, id_mapping):
        result = workflow.copy()
        
        if "nodes" in workflow:
            result["nodes"] = []
            for node in workflow["nodes"]:
                new_node = node.copy()
                if "id" in new_node and str(new_node["id"]) in id_mapping:
                    new_node["id"] = int(id_mapping[str(new_node["id"])])
                result["nodes"].append(self._process_dict_recursive(new_node, id_mapping))
        
        if "links" in workflow:
            result["links"] = []
            for link in workflow["links"]:
                new_link = list(link) if isinstance(link, (list, tuple)) else link
                if isinstance(new_link, list) and len(new_link) >= 5:
                    if str(new_link[1]) in id_mapping:
                        new_link[1] = int(id_mapping[str(new_link[1])])
                    if str(new_link[3]) in id_mapping:
                        new_link[3] = int(id_mapping[str(new_link[3])])
                result["links"].append(new_link)
        
        return result

    def _process_dict_recursive(self, d, id_mapping):
        result = {}
        for key, value in d.items():
            if isinstance(value, dict):
                result[key] = self._process_dict_recursive(value, id_mapping)
            elif isinstance(value, list):
                result[key] = self._process_list(value, id_mapping)
            else:
                result[key] = self._replace_id_in_value(value, id_mapping)
        return result

    def _process_list(self, lst, id_mapping):
        result = []
        for item in lst:
            if isinstance(item, list) and len(item) >= 2 and isinstance(item[0], str):
                if item[0] in id_mapping:
                    item = [id_mapping[item[0]]] + item[1:]
                result.append(item)
            elif isinstance(item, dict):
                result.append(self._process_dict_recursive(item, id_mapping))
            elif isinstance(item, str):
                result.append(id_mapping.get(item, item))
            else:
                result.append(item)
        return result

    def _replace_id_in_value(self, value, id_mapping):
        if isinstance(value, str):
            return id_mapping.get(value, value)
        return value


NODE_CLASS_MAPPINGS = {
    "NodeIDModifier": NodeIDModifier,
    "BatchNodeIDModifier": BatchNodeIDModifier,
    "WorkflowIDNormalizer": WorkflowIDNormalizer,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "NodeIDModifier": "Modify Node ID",
    "BatchNodeIDModifier": "Batch Modify Node IDs",
    "WorkflowIDNormalizer": "Normalize Workflow IDs",
}