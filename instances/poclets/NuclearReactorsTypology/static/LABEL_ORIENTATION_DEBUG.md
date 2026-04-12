# Label Orientation Debugging - Nuclear Reactor Typology 3D Enneagram

## Problem Statement

In the 3D visualization of the Nuclear Reactor Typology enneagram (BabylonJS), reactor labels needed to be positioned radially around a circle in the XZ plane and oriented **perpendicular to their radial position** (tangent to the circle).

**Initial Issue**: Labels were not parallel to the red debug lines (which represented the correct perpendicular orientation). Labels appeared tilted or incorrectly rotated despite multiple rotation attempts.

---

## Context & Geometry

### Coordinate System
- **XZ Plane**: Horizontal plane at `Y = Y_LEVEL` (constant)
- **Circle Center**: `(OFFSET_X, Y_LEVEL, 0)`
- **Radius**: `R_CIRCLE + distance_offset`

### Label Requirements
1. Position: Radial position at angle `θ` from center
2. Orientation: **Perpendicular to radial direction** (tangent to circle)
3. Plane: Flat in XZ plane (no tilt out of plane)
4. Readability: Text should face outward and be readable from standard camera angles

### Key Angles
For each pole at index `i`:
```javascript
const angle = ANGLES[i];              // Radial angle (pole position)
const perpAngle = angle + Math.PI/2;  // Perpendicular angle (label orientation)
```

---

## Failed Approaches

### Attempt 1: Rotation Matrices from Direction Vectors
**Strategy**: Compute rotation matrix from `forward` and `up` vectors.

```javascript
const forward = new BABYLON.Vector3(Math.cos(perpAngle), 0, Math.sin(perpAngle));
const up = new BABYLON.Vector3(0, 1, 0);
const right = BABYLON.Vector3.Cross(up, forward);
const rotMatrix = BABYLON.Matrix.FromValues(
  right.x, right.y, right.z, 0,
  up.x, up.y, up.z, 0,
  forward.x, forward.y, forward.z, 0,
  0, 0, 0, 1
);
plane.rotation = rotMatrix.toEulerAngles();
```

**Result**: ❌ Labels tilted out of XZ plane, not flat.

---

### Attempt 2: Sequential Euler Rotations (Y then X)
**Strategy**: First rotate around Y to orient, then rotate around X to lay flat.

```javascript
plane.rotation.y = perpAngle;
plane.rotation.x = -Math.PI / 2;
```

**Result**: ❌ Inconsistent orientations, labels not perpendicular to radials.

---

### Attempt 3: Quaternion Multiplication
**Strategy**: Combine rotations using quaternions to avoid gimbal lock.

```javascript
const quatY = BABYLON.Quaternion.RotationAxis(BABYLON.Axis.Y, perpAngle);
const quatX = BABYLON.Quaternion.RotationAxis(BABYLON.Axis.X, -Math.PI / 2);
plane.rotationQuaternion = quatY.multiply(quatX);
```

**Result**: ❌ Still incorrect, labels not in XZ plane.

---

### Attempt 4: Simple Euler (Y + X)
**Strategy**: Simplified version of Attempt 2.

```javascript
plane.rotation.y = perpAngle;
plane.rotation.x = -Math.PI / 2;
```

**Result**: ❌ Labels rotated but not perpendicular to radials.

---

### Attempt 5: Parent/Child Hierarchy
**Strategy**: Create parent node with Y rotation, child plane with X rotation.

```javascript
const parent = new BABYLON.TransformNode();
parent.rotation.y = perpAngle;
plane.parent = parent;
plane.rotation.x = -Math.PI / 2;
```

**Result**: ❌ Axes rotated incorrectly, still not achieving desired orientation.

---

## Debug Strategy: Geometric Reference Meshes

### The Breakthrough
Instead of relying on rotation logic, we **geometrically constructed rectangles** from the red debug line endpoints to visualize the target orientation:

```javascript
// Red debug line endpoints (perpendicular to radial)
const halfWidth = labelWidth / 2;
const p1 = labelPos.add(perpDir.scale(-halfWidth));
const p2 = labelPos.add(perpDir.scale(halfWidth));

// Construct blue rectangle from 4 corners (NO rotations)
const h = 0.01;  // Small height for visibility
const corners = [
  p1.add(new BABYLON.Vector3(0, h, 0)),
  p2.add(new BABYLON.Vector3(0, h, 0)),
  p2.add(new BABYLON.Vector3(0, -h, 0)),
  p1.add(new BABYLON.Vector3(0, -h, 0))
];

const bluePlane = BABYLON.MeshBuilder.CreatePolygon('debug_rect_' + i, {
  shape: corners,
  sideOrientation: BABYLON.Mesh.DOUBLESIDE
}, scene);
```

**Key Insight**: These geometrically-constructed rectangles were **perfectly oriented** without any rotations. By comparing the label planes to these reference rectangles, we could isolate the rotation issue.

---

## The Solution

### Discovery: Axis Transformation After rotation.x
The crucial insight came from observing that after applying `rotation.x = -Math.PI/2` to lay the plane flat in the XZ plane, **the plane's local "forward" axis (+Y in the plane's local space) becomes aligned with the global +Z axis**.

Therefore, orientation around this "forward" axis requires rotation around the **Z-axis**, not the Y-axis.

### Final Working Code
```javascript
plane.position = labelPos;
plane.rotation.x = -Math.PI / 2;   // Lay flat in XZ plane
plane.rotation.z = -perpAngle;      // Orient (rotation around Z after laying flat)
```

### Why It Works
1. **Step 1** (`rotation.x = -Math.PI/2`): The plane, initially in the XY plane (facing +Z), rotates 90° around X to lie flat in the XZ plane (facing +Y).
2. **Step 2** (`rotation.z = -perpAngle`): Now that the plane is flat, rotating around the Z-axis spins it within the XZ plane to achieve the perpendicular orientation to the radial.

### BabylonJS Euler Rotation Order
BabylonJS applies Euler rotations in the order: **Z → X → Y**. Understanding this order was critical to solving the orientation issue.

---

## Additional Refinements

### Conditional Flip for Readability
Labels at certain pole positions needed to be flipped 180° to ensure text was readable (not upside-down):

```javascript
let finalAngle = -perpAngle;

// Normalize angle to [0, 2π]
const normalizedAngle = ((angle % (2 * Math.PI)) + (2 * Math.PI)) % (2 * Math.PI);

// Flip labels in bottom half or specific poles for readability
if (poleIndex === 3 || poleIndex === 4 || poleIndex === 5 || poleIndex === 6 ||
    normalizedAngle < Math.PI / 2 || normalizedAngle > 3 * Math.PI / 2) {
  finalAngle += Math.PI;
}

plane.rotation.z = finalAngle;
```

### Label Sizing & Positioning
- **Size increased 17%**: `width = 1.29`, `height = 0.41` (from 1.1×0.35)
- **Distance reduced**: `R_CIRCLE + 0.55` (from 0.8) - closer to poles for better visual balance
- **Camera target raised 18%**: Better framing of the enneagram

---

## Lessons Learned

### 1. Geometric Construction > Trial-and-Error Rotations
Creating reference meshes geometrically (from vertex positions) provided immediate visual feedback and isolated the rotation logic issue without the confusion of compounding transformations.

### 2. Axis Transformations in 3D Rotations
When applying sequential rotations, the local coordinate frame changes with each rotation. After `rotation.x = -Math.PI/2`, the plane's local axes are transformed, requiring subsequent rotations around different axes than initially expected.

### 3. Euler Rotation Order Matters
BabylonJS's Z→X→Y order means that setting `rotation.z` after `rotation.x` affects the final orientation differently than other engines (e.g., Unity uses Z→X→Y by default as well, but other engines may differ).

### 4. Debug Visualization is Essential
- Red perpendicular lines showed target orientation
- Blue geometric rectangles confirmed correct orientation without rotations
- Yellow radial lines provided spatial reference

Without these debug visuals, the rotation issue would have taken significantly longer to resolve.

---

## Final Solution Summary

**Problem**: Labels not oriented perpendicular to radial positions in XZ plane.

**Root Cause**: Misunderstanding of how sequential Euler rotations transform the local coordinate frame, specifically that `rotation.x = -Math.PI/2` changes which axis controls in-plane orientation.

**Solution**: 
```javascript
plane.rotation.x = -Math.PI / 2;   // Lay flat in XZ plane
plane.rotation.z = -perpAngle;      // Orient perpendicular to radial
```

**Key Insight**: After laying the plane flat with `rotation.x`, use `rotation.z` (not `rotation.y`) for in-plane orientation because the plane's "forward" axis is now aligned with global +Z.

---

## Files Modified
- `M0_NuclearReactorTypology.html`
  - `makeLabel()` function: Final rotation solution
  - `buildDebugLabelLines()` function: Debug visualization (red lines + blue rectangles)
  - Camera target raised for better framing

---

## References
- BabylonJS Rotation Documentation: https://doc.babylonjs.com/features/featuresDeepDive/mesh/transforms/center_origin/rotation
- Euler Angles and Gimbal Lock: https://en.wikipedia.org/wiki/Gimbal_lock
- TSCG Framework: Transdisciplinary System Construction Game

---

**Author**: Claude + Michel (Echopraxium)  
**Date**: April 2026  
**Project**: Nuclear Reactor Typology - 3D Enneagram Visualization
