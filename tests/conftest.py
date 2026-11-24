import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIPELINE = os.path.join(ROOT, "pipeline")
SPECS = os.path.join(PIPELINE, "specs")
for p in (PIPELINE, os.path.join(ROOT, "tools")):
    if p not in sys.path:
        sys.path.insert(0, p)
