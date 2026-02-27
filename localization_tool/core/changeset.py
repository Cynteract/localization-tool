def calculate_changeset(english_data, target_data):

    # compareing english json and target json and creating a changeset

    create, update, delete = [], [], []

    english_keys = english_data.get("keys", {})
    target_keys = target_data.get("keys", {})

    # detect create and update
    for key, english_entry in english_keys.items():
        if key not in target_keys:
            create.append({
                "key": key,
                "value": english_entry["value"],
            })
        else:
            target_entry = target_keys[key]
            if english_entry.get("value") != target_entry.get("value"):
                update.append({
                    "key": key,
                    "old_value": target_entry.get("value"),
                    "new_value": english_entry.get("value")
                })

    # detect delete
    for key, target_entry in target_keys.items():
        if key not in english_keys:
            delete.append({
                "key": key,
                "value": target_entry.get("value")
            })

    return {
        "create": create,
        "update": update,
        "delete": delete
    }