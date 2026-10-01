"""
Example: Reading task history with filters and cursor pagination.
"""

import os
from datetime import datetime
from examples.config import get_client
from vaiz.models import GetHistoryRequest, CreateTaskRequest, TaskPriority
from vaiz.models.enums import Kind

BOARD_ID = os.getenv("VAIZ_BOARD_ID")
GROUP_ID = os.getenv("VAIZ_GROUP_ID")


def main():
    client = get_client()

    if not all([BOARD_ID, GROUP_ID]):
        raise RuntimeError("Set VAIZ_BOARD_ID and VAIZ_GROUP_ID in your .env")

    task = client.create_task(CreateTaskRequest(
        name="Example Task for History",
        group=GROUP_ID,
        board=BOARD_ID,
        priority=TaskPriority.Medium,
    )).task

    print("=== Basic history request ===")
    response = client.get_history(GetHistoryRequest(kind=Kind.Task, kindId=task.id))
    print(f"Events: {len(response.payload.items)}, has more: {response.payload.page.hasMore}")
    for event in response.payload.items:
        print(f"  {event.key} at {event.createdAt}: {event.data}")

    print("\n=== History with date range and event filter ===")
    filtered = client.get_history(GetHistoryRequest(
        kind=Kind.Task,
        kindId=task.id,
        dateRangeStart=datetime(2025, 1, 1),
        eventKeys=["TASK_CREATED", "TASK_COMPLETED"],
        limit=10,
    ))
    for event in filtered.payload.items:
        print(f"  {event.key} at {event.createdAt}")

    print("\n=== Paginating with nextCursor ===")
    cursor = None
    page_number = 1
    while True:
        page = client.get_history(GetHistoryRequest(
            kind=Kind.Task,
            kindId=task.id,
            limit=1,
            nextCursor=cursor,
        ))
        for event in page.payload.items:
            print(f"  page {page_number}: {event.key}")
        if not page.payload.page or not page.payload.page.hasMore:
            break
        cursor = page.payload.page.nextCursor
        page_number += 1


if __name__ == "__main__":
    main()
