"""npm specs handed to Reflex are EXACT versions.

Reflex runs `bun add <spec>` for each lib_dependency. A bare name installs
whatever is latest at build time; consumers now build frozen from a lockfile,
where a bare spec turns every upstream release into a failed build.
"""

from __future__ import annotations

import re
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "custom_components" / "reflex_audio_capture"


def test_lib_dependencies_are_exact() -> None:
    specs = []
    for p in sorted(SRC.glob("*.py")):
        for m in re.finditer(r"lib_dependencies[^=]*=\s*\[([^\]]*)\]", p.read_text()):
            specs += re.findall(r'"([^"]+)"', m.group(1))
    assert specs, "scan found no lib_dependencies (guard against a silent no-op)"
    for spec in specs:
        assert re.match(r"^(@[^/]+/)?[^@]+@\d+\.\d+\.\d+$", spec), (
            f"{spec!r} is not name@X.Y.Z"
        )
