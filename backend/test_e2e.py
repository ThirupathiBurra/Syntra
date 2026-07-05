import urllib.request
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

def post_json(url, data):
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read().decode())

def test():
    print("Generating workflow...")
    workflow = post_json(f"{BASE_URL}/workflows/generate", {
        "user_id": "u1",
        "request": "Extract data from a file, search knowledge base, generate a report, send an email to the user, and ask for human approval."
    })
    
    wf_id = workflow["workflow_id"]
    print(f"Generated Workflow {wf_id}:")
    for n in workflow["nodes"]:
        print(f" - {n['node_id']}: {n['capability_id']}")
        
    print("\nExecuting workflow...")
    exec_res = post_json(f"{BASE_URL}/workflows/{wf_id}/execute", {})
    print(f"Execution started with session: {exec_res['session_id']}")

if __name__ == "__main__":
    test()
