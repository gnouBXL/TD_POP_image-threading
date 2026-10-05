#!/usr/bin/env python3
"""Syntax/type check of the shaders outside TouchDesigner.

TouchDesigner adds #version, the layout and all its declarations itself, so
each shader is compiled with a stub (stubs/<name>.glsl) that declares what TD
would generate. `#include "shader_common"` is resolved to ../common.glsl.
Needs glslangValidator (apt install glslang-tools).

    python glsl/tools/check_glsl.py            # every shader
    python glsl/tools/check_glsl.py pegs_uv    # one shader
"""
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
GLSL = os.path.dirname(HERE)
INCLUDES = {"shader_common": "common.glsl"}
SHADERS = {  # name -> (file, stage)
    "pegs_uv": ("pegs_uv.comp", "comp"),
    "state_init": ("state_init.comp", "comp"),
    "engine": ("engine.comp", "comp"),
    "build_threads": ("build_threads.comp", "comp"),
    "trail_id": ("trail_id.comp", "comp"),
    "debug_overlay": ("debug_overlay.frag", "frag"),
}


def source(name):
    path, stage = SHADERS[name]
    body = open(os.path.join(GLSL, path)).read()
    body = re.sub(r'#include\s+"(\w+)"',
                  lambda m: open(os.path.join(GLSL, INCLUDES[m.group(1)])).read(), body)
    head = "#version 460\n"
    if stage == "comp":
        head += f"layout(local_size_x = {256 if name == 'engine' else 64}) in;\n"
    head += open(os.path.join(HERE, "stubs", name + ".glsl")).read()
    return head + "\n#line 1\n" + body, stage


def check(name):
    src, stage = source(name)
    with tempfile.NamedTemporaryFile("w", suffix="." + stage, delete=False) as f:
        f.write(src)
    r = subprocess.run(["glslangValidator", f.name], capture_output=True, text=True)
    os.unlink(f.name)
    ok = r.returncode == 0
    out = "\n".join(l for l in r.stdout.splitlines() if l.strip() and not l.startswith("/"))
    print(f"{'OK  ' if ok else 'FAIL'} {name}" + (f"\n{out}" if out and not ok else ""))
    return ok


if __name__ == "__main__":
    names = sys.argv[1:] or list(SHADERS)
    sys.exit(0 if all([check(n) for n in names]) else 1)
