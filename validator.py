import re
import asyncio
from rules import RULES

def apply_rule(record, rule):
    field = rule["field"]
    value = record.get(field)

    if rule["type"] == "required":
        if not value:
            return f"{field} is required"

    if rule["type"] == "regex":
        if value and not re.match(rule["value"], value):
            return f"{field} is invalid"

    return None


async def validate_single_record(record, idx):
    record_errors = []

    for rule in RULES:
        error = apply_rule(record, rule)
        if error:
            record_errors.append(error)

    return {
        "record_index": idx,
        "errors": record_errors
    }


async def validate_records(records):
    tasks = [
        validate_single_record(record, idx)
        for idx, record in enumerate(records)
    ]

    results = await asyncio.gather(*tasks)

    errors = [r for r in results if r["errors"]]
    valid_count = len(records) - len(errors)

    return {
        "total_records": len(records),
        "valid_records": valid_count,
        "invalid_records": len(errors),
        "errors": errors
    }