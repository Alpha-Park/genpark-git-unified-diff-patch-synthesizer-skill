"""
MCP Server for genpark-git-unified-diff-patch-synthesizer-skill
Standard JSON-RPC 2.0 protocol over stdio.
"""

import sys
import json
from client import UnifiedDiffPatchSynthesizerClient

client = UnifiedDiffPatchSynthesizerClient()

def handle_request(req):
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "create_patch",
                        "description": "Create unified diff patch from original and modified code.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "original_text": {"type": "string"},
                                "modified_text": {"type": "string"},
                                "filename": {"type": "string"}
                            },
                            "required": ["original_text", "modified_text"]
                        }
                    },
                    {
                        "name": "apply_patch_fuzzy",
                        "description": "Apply patch to code with line drift tolerance.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "original_text": {"type": "string"},
                                "patch_text": {"type": "string"},
                                "max_drift": {"type": "integer"}
                            },
                            "required": ["original_text", "patch_text"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "create_patch":
            res = client.create_patch(args.get("original_text", ""), args.get("modified_text", ""), args.get("filename", "file.py"))
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": res}]}}
        elif tool_name == "apply_patch_fuzzy":
            res = client.apply_patch_fuzzy(args.get("original_text", ""), args.get("patch_text", ""), args.get("max_drift", 5))
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
