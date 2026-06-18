import math

lines = [".section .rodata\n"]
lines.append("sin_table:\n")
for i in range(360):
    v = int(math.sin(math.radians(i)) * 65536)
    lines.append(f"  .dword {v}\n")
lines.append("cos_table:\n")
for i in range(360):
    v = int(math.cos(math.radians(i)) * 65536)
    lines.append(f"  .dword {v}\n")

with open("trig_tables.inc", "w") as f:
    f.writelines(lines)
print("Done — trig_tables.inc generated")