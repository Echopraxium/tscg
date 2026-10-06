#!/usr/bin/env python3
"""render_graph.py - rebuild TSCG_RemainingWork.png from its Graphviz sources.

Author : Echopraxium with the collaboration of Claude AI
Date   : 2026-10-03

Renders TSCG_RemainingWork.dot (main graph) and legend.dot (legend) with Graphviz,
then pastes the legend in the bottom-right corner (Graphviz cannot pin a legend to a
corner reliably).

Requirements: Graphviz `dot` on the PATH, and Pillow (pip install pillow).
Usage (from this folder):  python render_graph.py
"""
import os
import subprocess
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DPI = "110"


def render(dot_file, png_file):
    subprocess.run(["dot", "-Tpng", f"-Gdpi={DPI}", dot_file, "-o", png_file],
                   check=True, cwd=HERE)


def main():
    main_png = os.path.join(HERE, "_main.png")
    legend_png = os.path.join(HERE, "_legend.png")
    out_png = os.path.join(HERE, "TSCG_RemainingWork.png")
    try:
        render("TSCG_RemainingWork.dot", main_png)
        render("legend.dot", legend_png)
    except FileNotFoundError:
        sys.exit("Graphviz 'dot' not found on the PATH.")
    m = Image.open(main_png).convert("RGB")
    lg = Image.open(legend_png).convert("RGB")
    width = max(m.width, lg.width + 40)
    height = m.height + lg.height + 30
    out = Image.new("RGB", (width, height), "white")
    out.paste(m, (0, 0))
    out.paste(lg, (width - lg.width - 20, height - lg.height - 15))
    out.save(out_png)
    os.remove(main_png)
    os.remove(legend_png)
    print(f"written {out_png} ({width}x{height})")


if __name__ == "__main__":
    main()
