#!/usr/bin/env python3
"""
Example: getTasks Caching and Manual Pagination

This example demonstrates:
1. Mandatory 5-minute caching for API protection
2. Manual pagination (only way to get >50 tasks)
3. Maximum 50 tasks per page limit
"""

from vaiz.models import GetTasksRequest
from examples.config import get_client
import time


def main():
    """Demonstrate caching and manual pagination."""
    client = get_client()
    client.verbose = True  # Show cache operations
    
    print("=== getTasks: Caching + Manual Pagination ===\n")
    
    # Test 1: Caching demonstration
    print("Test 1: Mandatory Caching (5-minute TTL)")
    request = GetTasksRequest(limit=10)
    
    print("First request (cache miss):")
    start = time.time()
    response1 = client.get_tasks(request)
    time1 = time.time() - start
    print(f"  ⏱️  Took: {time1:.3f} seconds")
    print(f"  📋 Tasks: {len(response1.payload.tasks)}")
    
    print("\nSame request again (cache hit):")
    start = time.time()
    response2 = client.get_tasks(request)
    time2 = time.time() - start
    print(f"  ⏱️  Took: {time2:.3f} seconds")
    print(f"  🚀 Speedup: {time1/time2:.0f}x faster")
    print(f"  📋 Tasks: {len(response2.payload.tasks)}")
    
    print("\n" + "="*50 + "\n")
    
    # Test 2: Manual pagination for large datasets
    print("Test 2: Manual Pagination (only way to get >50 tasks)")
    
    all_tasks = []
    page = 0
    max_pages = 3
    
    print("Fetching pages manually:")
    while page < max_pages:
        request = GetTasksRequest(limit=50, skip=page * 50)
        response = client.get_tasks(request)
        tasks = response.payload.tasks
        
        if not tasks:
            break
            
        print(f"  📄 Page {page + 1}: {len(tasks)} tasks")
        all_tasks.extend(tasks)
        page += 1
        
        if len(tasks) < 50:
            break
    
    print(f"\n📊 Total collected: {len(all_tasks)} tasks from {page} pages")
    print("💡 Each page is cached for 5 minutes")
    
    print("\n" + "="*50 + "\n")
    
    # Test 3: Cache with different filters
    print("Test 3: Different Filters = Different Cache Entries")
    
    filters = [
        ("Completed tasks", GetTasksRequest(completed=True, limit=5)),
        ("Pending tasks", GetTasksRequest(completed=False, limit=5)),
        ("Page 2", GetTasksRequest(limit=5, skip=5)),
        ("Specific board", GetTasksRequest(board="68c19e08020b3f8c50a814d6", limit=5))
    ]
    
    for name, req in filters:
        start = time.time()
        resp = client.get_tasks(req)
        elapsed = time.time() - start
        print(f"  {name}: {elapsed:.3f}s → {len(resp.payload.tasks)} tasks")
    
    print("\n💡 Each unique combination of parameters has its own cache entry")
    
    print("\n" + "="*50 + "\n")
    
    # Test 4: API Protection Limits
    print("Test 4: API Protection Limits")
    
    print("✅ Maximum 50 tasks per page (enforced by validation)")
    print("✅ Mandatory 5-minute caching (cannot be disabled)")
    print("✅ Manual pagination required for >50 tasks")
    
    try:
        GetTasksRequest(limit=51)
        print("❌ ERROR: Should reject limit > 50")
    except ValueError:
        print("✅ Correctly rejects requests for >50 tasks per page")
    
    print("\n=== Summary ===")
    print("🛡️  API Protection Features:")
    print("   • Maximum 50 tasks per request")
    print("   • Mandatory 5-minute caching")
    print("   • Manual pagination only")
    print("   • Cache per unique parameter combination")
    print("   • Prevents API abuse and excessive calls")


if __name__ == "__main__":
    main()
