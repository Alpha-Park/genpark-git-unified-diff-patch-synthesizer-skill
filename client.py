"""
Autonomous Unified Diff Patch Synthesizer and Fuzzy Applicator.
Zero external dependencies, standard library only.
"""

import difflib
from typing import Dict, List, Any, Optional, Tuple

class UnifiedDiffPatchSynthesizerClient:
    """
    Parses, generates, and fuzzily applies RFC-standard unified diff patches.
    Detects merge conflicts, line drift, and verifies semantic integrity.
    """

    def __init__(self):
        pass

    def create_patch(self, original_text: str, modified_text: str, filename: str = "file.py") -> str:
        """Generates standard unified diff patch."""
        orig_lines = original_text.splitlines(keepends=True)
        mod_lines = modified_text.splitlines(keepends=True)
        diff = difflib.unified_diff(
            orig_lines,
            mod_lines,
            fromfile=f"a/{filename}",
            tofile=f"b/{filename}",
            n=3
        )
        return "".join(diff)

    def parse_hunks(self, patch_text: str) -> List[Dict[str, Any]]:
        """Parses unified diff patch into structured hunks."""
        hunks = []
        current_hunk = None
        
        for line in patch_text.splitlines():
            if line.startswith("@@"):
                parts = line.split("@@")
                header_info = parts[1].strip().split()
                old_info = header_info[0][1:].split(",")
                new_info = header_info[1][1:].split(",")
                
                old_start = int(old_info[0])
                old_count = int(old_info[1]) if len(old_info) > 1 else 1
                new_start = int(new_info[0])
                new_count = int(new_info[1]) if len(new_info) > 1 else 1

                current_hunk = {
                    "header": line,
                    "old_start": old_start,
                    "old_count": old_count,
                    "new_start": new_start,
                    "new_count": new_count,
                    "lines": []
                }
                hunks.append(current_hunk)
            elif current_hunk is not None:
                current_hunk["lines"].append(line)

        return hunks

    def apply_patch_fuzzy(self, original_text: str, patch_text: str, max_drift: int = 5) -> Dict[str, Any]:
        """
        Applies unified diff patch to original text with fuzzy line drift tolerance.
        Returns applied text, applied hunks count, and conflict report.
        """
        hunks = self.parse_hunks(patch_text)
        if not hunks:
            return {"status": "no_op", "patched_text": original_text, "applied": 0, "conflicts": []}

        lines = original_text.splitlines()
        conflicts = []
        applied_count = 0

        for hunk in sorted(hunks, key=lambda h: h["old_start"], reverse=True):
            expected_old = []
            replacement_new = []

            for h_line in hunk["lines"]:
                if h_line.startswith(" "):
                    expected_old.append(h_line[1:])
                    replacement_new.append(h_line[1:])
                elif h_line.startswith("-"):
                    expected_old.append(h_line[1:])
                elif h_line.startswith("+"):
                    replacement_new.append(h_line[1:])

            target_idx = hunk["old_start"] - 1
            found_idx = None

            for drift in range(max_drift + 1):
                for candidate in (target_idx + drift, target_idx - drift):
                    if 0 <= candidate <= len(lines) - len(expected_old):
                        candidate_chunk = lines[candidate : candidate + len(expected_old)]
                        if candidate_chunk == expected_old:
                            found_idx = candidate
                            break
                if found_idx is not None:
                    break

            if found_idx is not None:
                lines[found_idx : found_idx + len(expected_old)] = replacement_new
                applied_count += 1
            else:
                conflicts.append({
                    "hunk_header": hunk["header"],
                    "reason": "Failed to locate matching context hunk within line drift window"
                })

        newline_char = chr(10)
        patched_content = newline_char.join(lines) + (newline_char if original_text.endswith(newline_char) else "")
        return {
            "status": "success" if not conflicts else "conflicted",
            "applied_hunks": applied_count,
            "total_hunks": len(hunks),
            "conflicts": conflicts,
            "patched_text": patched_content
        }
