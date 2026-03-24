VALID_FLOW = ["CREATED", "ASSIGNED", "CONTACTED", "CLOSED"]

def simulate_workflow(records):
    issues = []

    for idx, record in enumerate(records):
        history = record.get("history", [])

        for i in range(len(history) - 1):
            current = history[i]
            next_state = history[i + 1]

            if current not in VALID_FLOW or next_state not in VALID_FLOW:
                issues.append({
                    "record_index": idx,
                    "error": f"Invalid state detected: {current} or {next_state}"
                })
                continue

            if VALID_FLOW.index(next_state) < VALID_FLOW.index(current):
                issues.append({
                    "record_index": idx,
                    "error": f"Invalid transition {current} → {next_state}"
                })

    return {
        "checked_records": len(records),
        "issues_found": len(issues),
        "issues": issues
    }