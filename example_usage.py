"""
Demonstration of genpark-git-unified-diff-patch-synthesizer-skill
"""

from client import UnifiedDiffPatchSynthesizerClient

def main():
    patcher = UnifiedDiffPatchSynthesizerClient()

    orig_doc = """def compute_total(items):
    subtotal = sum(i['price'] for i in items)
    tax = subtotal * 0.08
    return subtotal + tax
"""

    mod_doc = """def compute_total(items, discount=0.0):
    subtotal = sum(i['price'] for i in items)
    discounted = subtotal * (1.0 - discount)
    tax = discounted * 0.08
    return discounted + tax
"""

    patch = patcher.create_patch(orig_doc, mod_doc, "pricing.py")
    print("=== SYNTHESIZED UNIFIED DIFF PATCH ===")
    print(patch)

    print("=== APPLYING PATCH FUZZILY ===")
    res = patcher.apply_patch_fuzzy(orig_doc, patch)
    print(f"Status: {res['status']}")
    print(f"Applied Hunks: {res['applied_hunks']} / {res['total_hunks']}")
    print("Resulting Patched Code:
", res['patched_text'])

if __name__ == "__main__":
    main()
