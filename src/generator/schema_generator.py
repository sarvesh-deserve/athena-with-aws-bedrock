import json


def load_schema(file_path: str):
    """Load schema from JSON file."""
    with open(file_path, "r") as f:
        return json.load(f)


def transform_for_llama_index(schema):
    """Transform schema into LlamaIndex format."""
    llama_schema = {"tables": []}

    for table in schema["tables"]:
        llama_table = {
            "name": table["name"],
            "columns": [f"{col['name']} ({col['type']})" for col in table["columns"]],
            "primary_key": ", ".join(table["primary_key"]),
            "description": table.get("description", ""),
        }
        llama_schema["tables"].append(llama_table)

    return llama_schema
