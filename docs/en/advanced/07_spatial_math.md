# Spatial Transforms and SteamVR Coordinates

Consider a VR window as a scaleed paper. The application knows where the buttons are on the paper, SteamVR knows the position of the paper in the room, and the controller emits a beam of light with a starting point and direction. The so-called spatial UI aims to use the same geometric language for these three phenomena. By rotating the paper, moving it along with the controller, or bending the paper into an arc, the position of the buttons is still defined by the scale on the paper.

This chapter unfolds along a continuous problem. First, send the pixels into space, then backwardly determine which pixel the laser hits, and finally use the same coordinate transformation to explain window movement, rotation, scaling, and curvature adjustment. When reading, you can consider the paper, pen, and table edge as the coordinate axes. In the following text, `X/Y/Z` represents the three spatial axes, `left/top` represents the logical pixels on the window, `R` represents rotation or the radius in the cylindrical section, and `T` represents the pose that includes both rotation and translation.

## 1. First, establish the coordinate system

### The origin defines where to measure, and the axes define how to measure

Place the upper left corner of the paper on a point on the tabletop, defining rightward movement as positive and downward movement as positive as well. `(120,80)` on the paper represents two directional displacements. With a different paper, `(120,80)` on the paper can describe the same layout, but it falls in another place on the tabletop. The upper left corner of the paper can be moved, and the direction of the paper can also be rotated. These are translation and rotation in three-dimensional transformation.

The three-dimensional coordinate system has one more axis than paper. After taking two perpendicular unit axes, the third axis can have two opposite directions. The right-handed system defines `eX × eY = eZ`. The right index finger points to `+X`, the middle finger to `+Y`, and the thumb gives the direction of `+Z`. If the left-handed system maintains the same first two axes, the third axis has the opposite direction. Handedness is the relative convention of the three axes. When an object rotates in space, its three axes rotate together. The axis group originally in the right-handed system remains right-handed after rotation. Only flipping one axis changes handedness. When looking in a mirror, the left and right images are swapped, which is why you can't directly insert a mirror rotation into quaternions as a regular rotation.

SteamVR tracking is represented in the right-handed system. When the headset pose is rotated, `+X` points to the right, and `+Y` points upward. According to the right-hand rule, `+Z` points to the side of the wearer, so the line of sight ahead is represented by `−Z`. This is the alignment convention between the local axes of the device and the tracking space when it rotates at zero. After turning the head, the front is the result of the headset rotation acting on `(0,0,−1)`. For example, according to the right-hand rule, rotating `90°` around `+Y` changes the line of sight originally along `−Z` to `−X`. Conducting an experiment with this simple set of directions is more reliable than remembering "if the yaw angle is positive, it points in that direction," because users may also refer to left and right turns with different terms.

Another often confused quantity is position and direction. Position `(0,1.6,−1)` indicates how far a point is from the origin. Direction `(0,0,−1)` indicates which direction to go. If the entire coordinate system is translated by one meter, the position coordinates of the point will be affected by the translation, and the three components of direction only need to be recalculated when the axes rotate. The starting point of the laser belongs to the former, and direction belongs to the latter. The intersection calculation transforms these two quantities separately.

![is SteamVR's right-handed axis and the window logical pixel axis](/images/en/advanced_coord_systems.png)

### Conversion between logical pixels and meters

Let `w` and `h` be the logical window dimensions and `s = physical_scale` its physical scale. The following three quantities are used throughout.

```text
m = s / LOGICAL_PIXELS_PER_METER = s / 1000
W = w · m
H = h · m
```

The unit of `m` is meters per logical pixel, while `W` and `H` are physical width and height. The SDK defines `LOGICAL_PIXELS_PER_METER` in `render_style.h`, and `window::get_physical_width()` and `window::get_physical_height()` are calculated according to this formula. The Engine's `service_runtime::get_physical_width()` also uses `1000` as a reference. There is an exception for input auxiliary surfaces: when the Engine has the current window, it uses the `physical_scale` of the having window.

When `s = 1`, one logical pixel corresponds to one millimeter. The physical size of a `640×360` window is `0.64×0.36` meters. When moving `s` from `1` to `1.5` on the same window, the physical size becomes `0.96×0.54` meters. This operation changes the size of the window in VR, while the control rectangle remains at the original logical pixels. Changing the resolution from `640×360` to `960×540` while still using `s = 1` will also result in a physical size of `0.96×0.54` meters, but the drawing target and control layout coordinates will change. The spatial dimensions of the two results can be the same, but the interaction and resource consumption will differ. If you want to change the logical resolution while retaining the physical width, adjust `s` in the reverse ratio of the new and old logical widths.

With the top-left corner as the origin, the local spatial coordinate of a point on the plane is `(m·left, −m·top, 0)`. The negative sign comes from the difference between the downward increase of `top` on paper and the upward increase of `+Y` in VR. With the center of the window as the origin, first convert the pixel coordinates relative to the center, then convert them to meters.

```text
Point relative to top-left origin A  pA = (m·left, −m·top, 0)
Offset from top left to center       cA = (W/2, −H/2, 0)
Point relative to center origin C    pC = (m·(left − w/2), m·(h/2 − top), 0)
Relationship between the two forms       pA = cA + pC
```

Here, `w/2` represents the midpoint of two boundaries, which is `320` when the width is `640`. Continuous coordinates are used for window positioning, so `left` can be equal to `120.25`. Pixel positions are used for layout and hit detection, and which discrete texture pixel the drawing sample falls on is determined by rendering processing. If the fall point is rounded at the beginning, some lines and hit edges may jitter near the threshold.

`window.position` and `metadata.position` in the protocol describe the translation of the top-left corner position in the reference frame. The `resolve_pose()` of the Engine and `get_anchor()` of the SDK restore this top-left corner position. The `get_center_pose()` of the Engine and `get_world_pose()` of the SDK combine the center offset. The public `window::get_world_transform()` calls `get_world_pose()`, resulting in the center position in the world space. When directly comparing the translation parts of `position` and `get_world_transform()`, first confirm whether their reference frames and origins are consistent.

For example, in a unit reference frame with zero rotation, the top-left corner is `A = (0,1.6,−1)`, with the same width and height as the previous example. The center is `C = (0.32,1.42,−1)`, and `(left,top) = (120,80)` relative to the center is `(−0.20,0.10,0)`, resulting in the world coordinate `(0.12,1.52,−1)`. If `A` is mistakenly considered `C`, the result will be a half-width and half-height offset overall. If only the negative sign of `top` is forgotten, the vertical direction will be mirrored. The same model can diagnose these two errors separately.

## 2. Use vectors for projection, determine orientation, and construct coordinate axes

### Dot product extracts a component in a certain direction

Vectors can be read as directed arrows. `a = (3,4,0)` can represent moving three steps to the right and four steps up from the starting point. Its length is `sqrt(3² + 4²) = 5`. `vec3_t::get_length()` is calculated with three parameters `hypot(x,y,z)`. The difference in coordinates gives the displacement between two points, and the sum of coordinates can be used for “starting point plus displacement”. Multiplying a direction vector by a negative number reverses the direction, while multiplying by a positive number only changes the length.

The dot product of `a·b = ax·bx + ay·by + az·bz` is also equal to `|a|·|b|·cos(φ)`, where `φ` is the angle between two non-zero vectors. After normalizing `b` to the unit vector `b̂`, `a·b̂` becomes the signed length of `a` along this axis. If `a = (3,4,0)` and `b̂ = (1,0,0)`, the projection length is `3`, corresponding to the projection vector `(3,0,0)`. If the base axis is changed to `(−1,0,0)`, the length becomes `−3`, and the projection vector remains `(3,0,0)`. The sign is used to describe the orientation relative to the specified positive direction.

In Cartesian coordinates, given a point and three orthogonal unit axes, multiplying the point by each axis individually yields three specific quantities. For the plane normal `n` and the ray direction `d`, `d·n = 0` indicates that the ray is parallel to the tangent plane; approaching zero means very steeply incident. `d·n < 0` represents the ray directed in the opposite direction to the normal, hitting the surface from the side opposite to the normal. `d·n > 0` corresponds to backside incidence. The SDK uses `vec3_t::calculate_dot_product()` to calculate these quantities. When discussing surfaces later, the normal changes with lateral position, so the front and back sides depend on the normal at the point of interest.

To calculate the actual angle from two unit vectors, `acos(clamp(a·b,−1,1))` can be used. The restricted range is to prevent rounding from turning the theoretical `1` into a number slightly greater than `1`. If only comparing “which one is more forward,” direct dot product calculations save work and avoid converting a single comparison into inverse trigonometric operations for angles. To express signed angles, it's necessary to define the axis direction, using `atan2` in the subsequent phase formula to distinguish between positive and negative directions around the axis.

### The cross product gives the perpendicular axis, with positive and negative signs determined by order.

The cross product outputs a vector. The expression is as follows.

```text
a × b = (ay·bz − az·by, az·bx − ax·bz, ax·by − ay·bx)
|a × b| = |a|·|b|·sin(φ)
```

Substituting `a = (1,0,0)` and `b = (0,1,0)` gives `(0,0,1)`. Swapping them results in `(0,0,−1)`. The SDK's `vec3_t::calculate_cross_product()` uses the same component notation. The cross product also provides the area of the parallelogram and the perpendicular direction. When the input arrows are almost parallel, the area approaches zero, and the perpendicular result is very short. Magnifying this to unit vectors also amplifies measurement noise.

A common construction is to know the required forward unit vector `f` and roughly “upward” `u`, and to generate the right-hand right, up, and backward axes. Since local `−Z` is forward, first take `z = −f`, then set `x = normalize(u × z)`, and finally set `y = z × x`. Before use, check if `u` and `z` are nearly parallel. If a stable construction is needed, choose an axis with a larger direction difference from other reference axes when degeneration occurs, or temporarily retain the direction from the previous frame. After three valid orthogonal unit axes are given, the SDK's `quat_t::create_from_axis_basis(a,b,c)` converts them into quaternions using the three columns of the rotation matrix. The source code first calculates the matrix trace `a.x + b.y + c.z`; when the trace is positive, the remaining components are found through scalar components. In other cases, the largest diagonal component is chosen as the stable entry, and finally normalized. Reversing the rows and columns would incorrectly represent a local-to-world rotation as its inverse rotation.

Strictly speaking, the vector representing the local `X` axis in world coordinates is the first column of the matrix. Matrix multiplication with `(1,0,0)` selects this column. Multiplying with `(2,3,0)` is equivalent to moving two units along the first column and three along the second. This is also the most useful way to verify that “the columns of the rotation matrix represent the axes.”

### Normalization first stabilizes the numerical range.

Typically, dividing a vector by its length is called normalization. When calculating the length of `(1e300,1e300,0)`, direct squaring may cause overflow first. Very small values may overflow to zero during squaring. The SDK's `vec3_t::get_normalized()` first checks for finite values, then finds the absolute value of the largest component, `M`. After scaling with `M`, the absolute values of all components are within `[0,1]`, and at least one has an absolute value of `1`. Then, the length is obtained using `get_length()` within the scaled range, and finally normalized. This process changes the calculation path while retaining the mathematical result, as both scaling operations are positive.

For example, `(30,40,0)` is first divided by `40` to get `(0.75,1,0)` and length `1.25`, then divided again to get `(0.6,0.8,0)`. For zero vectors and non-finite components, the SDK reports `zero_direction`. Quaternion normalization also starts with scaling the largest component, but the error key is `invalid_rotation`. When “direction cannot be defined,” the caller must resolve measurement or input conditions by adding a random decimal, which may introduce direction jumps.

`numeric_limits<double>::epsilon()` describes the double-precision resolution when approaching `1.0`. From the source code, it is determined that their uses are different. `vec3_t::is_equal()` is used for comparing components, while `epsilon·max(1,|a|,|b|)` is used for SDK plane intersection. `epsilon` is used to check the local `z` in the direction, and the minimum effective projection length during double-handed rotation uses the actual physical threshold of `0.02` meters. Mixing these three thresholds into one constant will result in the loss of both units and actual meaning. The numerical precision threshold addresses floating-point boundaries, and the physical threshold addresses device noise and gesture stability.

## 3. Pose connects two coordinate systems.

### First rotate the point, then translate it.

Let `T_WA` represent converting the values in coordinate system `A` into values in the tracking space `W`. It includes rotation `R_WA` and displacement `t_WA`. For a point, first replace the local base axis with the world base axis, then translate the result to the world position of the local origin.

```text
P_W = R_WA · P_A + t_WA
D_W = R_WA · D_A
```

`pose_t::transform_point()` essentially performs `position + rotation.rotate(v)`. Only `rotation.rotate()` is used for direction transformation. For example, after translating `(1,0,0)`, the local origin `(0,0,0)` moves to `(1,0,0)`. The tangents of the same trajectory still follow the original direction. If the function of the transformation point is called for the direction, the resulting ray will change direction as the window moves away from the global origin, resulting in a sudden distortion after the window moves to another location.

In the notation of this article, `T_WA · T_AB` represents first moving from `B` to `A`, and then from `A` to `W`. Expanding the two expressions gives combined translation and rotation.

```text
P_A = R_AB · P_B + t_AB
P_W = R_WA · (R_AB · P_B + t_AB) + t_WA
R_WB = R_WA · R_AB
t_WB = t_WA + R_WA · t_AB
```

This is the implementation of `pose_t::operator*()` in two ways. The displacement of the smaller coordinate system belongs to the local direction of the larger coordinate system and needs to be rotated first. Imagine holding a piece of paper in the left hand, with the paper ten centimeters to the right of the handle. After turning the hand, these ten centimeters are still to the right of the handle itself, but their direction changes in the room coordinates. Directly adding the two `position` terms will fix these ten centimeters to the exact right side of the room.

### To go from the world to the local, a complete inverse pose is required.

Solve `P_A = R⁻¹·(P_W−t)` from `P_W = R·P_A+t`. Therefore, the inverse rotation is `R⁻¹`, and the translation is `−R⁻¹·t`. SDK's `pose_t::get_inverse()` first calculates the quaternion inverse, then computes `q.rotate(position * −1.0)`. Here, translation and rotation must be reversed in pairs. For a graph that always follows the coordinate axis, subtracting the position might be correct, but problems will become apparent after turning the hand or head.

A complete link can be calculated manually. Let the position of the reference frame `A` be `(1.00,1.50,−0.80)`, and rotate `90°` around the world `+Z`. The upper left corner of the window is at `(0.20,0.10,−0.50)` in the reference frame, with zero rotation relative to the reference frame. The window is wide `600`, high `400`, and `s = 1`.

1. In the world, reference frame `+X` becomes `+Y`, and reference frame `+Y` becomes `−X`. Therefore, after rotating the local translation of the window around `Z`, we get `(−0.10,0.20,−0.50)`, plus the reference frame origin. The upper left corner of the window in the world is `A_W = (0.90,1.70,−1.30)`.
2. The center of the window surface is a local `(0.30,−0.20,0)` relative to the upper left corner. After converting to world increment, it becomes `(0.20,0.30,0)`, so the center is `C_W = (1.10,2.00,−1.30)`.
3. The logical coordinates of the button center, `(150,100)`, are a local `(0.15,−0.10,0)` relative to the upper left corner, and `(−0.15,0.10,0)` relative to the center of the window surface. Using the first method, the world increment is `(0.10,0.15,0)`, and the world point of the button is `(1.00,1.85,−1.30)`. Using the second method, the world increment is `(−0.10,−0.15,0)`, and adding it to the center results in the same point.
4. When calculating backwards, subtract `C_W` from the button world point to get `(−0.10,−0.15,0)`. Reversing `90°` yields `(−0.15,0.10,0)` for the window center system. Converting back to pixels, we get `left = 300 − 150 = 150`, `top = 200 − 100 = 100`. If the reverse rotation is forgotten, the world point `(−0.10,−0.15)` will be directly treated as the window `x/y`, resulting in a calculated value of `(200,350)`. The deviation of hits can change with rotation, which can be used to identify such implementation errors.

Represent each window's forward chain using a framework, with the top-left pose of the window being `T_WA = T_WR · T_RA`. `R` here represents a reference system for a particular window. If calculating a plane point from the center system, multiply it by the fixed offset `T_AC` from the top-left to the center. The reverse process is `P_C = T_AC⁻¹ · T_RA⁻¹ · T_WR⁻¹ · P_W`. The world point can be converted sequentially using this formula. To avoid redundant calculations, the source code synthesizes the center pose directly and performs one reverse calculation. Finally, convert from the center local coordinates to pixels. There are five optional reference systems in the tracking space, and only one of them is selected as the intermediate coordinate system for each window.

### Switching reference systems, tracking loss, and reset

`world` uses Engine's `world_origin`, which allows the application to represent windows in easily positioned local coordinates. When obtaining the initial headset (HMD) pose, `initialize_world_origin()` places the origin at the HMD position plus the standing axis `(0,0,−1.2)`, with the initial direction being unit rotation. Here, the offset follows the tracking space's `−Z`, without multiplying by the HMD rotation first. `head` uses the real-time HMD pose, with the local `−Z` rotating together with the HMD. `left` and `right` use the tracking poses of the corresponding controllers, with Engine's `is_eligible()` limiting the hit to the laser of the opposite hand. When the device loses tracking, the reference can be empty. Retaining the previous transformation prevents hits from becoming floating, so this path must handle unavailable poses first.

`body` is based on the real-time HMD position and a fixed reference direction. `BODY_HEAD_TO_NECK_OFFSET = (0,−0.075,0.08)` points the HMD origin to a nominal neck pivot. Rotating this vector according to the current HMD pose and adding it to the HMD position yields an estimated neck position. Then, using a fixed direction, subtract the reverse offset from "neck to HMD" to get the reference point for window positioning. Mathematically, this is `p_body = p_head + R_head·d − R_body·d`, with the reference system direction given by `R_body`. When turning the head, the two position compensations reduce the translation caused by the HMD's movement around the neck. The compensation uses a fixed human approximation, and should be distinguished from the actual position changes due to movement during debugging. `reset_body_center()` records the complete HMD rotation during reset.

The processing of `Ctrl+Alt+Pause` can also reset `world_origin`. Assuming the initial calibration saves `B = T_world_initial⁻¹ · T_head_initial`, measure the current HMD pose `H` before resetting. Keep the HMD relationship measured in the new reference system as `B`, solve for `T_world_new · B = H`, and obtain `T_world_new = H · B⁻¹`. `reset_world_origin()` updates the reference system based on this. Here, the reference system for Overlay is moved, while the application window retains its own local pose relationship. SteamVR's standing space and game character's map coordinates are maintained by different systems, and moving the character with the game controller does not automatically change this physical tracking pose.

`reparent(reference, keep_world=true)` solves another similar equation. First, save the window world's top-left pose `T_old` calculated from the old chain. After selecting the new reference system `T_new_ref`, to maintain the same position and direction, set `T_new_local = T_new_ref⁻¹ · T_old`. The SDK implements this in `ui_runtime::reparent()` through `get_anchor()`, `get_reference()`, and `change_transform()`. If `keep_world` is true and the reference system on either side loses tracking, the old reference state is retained, and the interface reports `reference_not_tracked`. If `keep_world` is false, the window retains local parameters while switching reference systems, which means explicitly attaching the paper to the new object.

The default center alignment applies to the initial placement. When there is no valid source window, the initial distance in front of the line of sight is set to `max(1.2,W,H)` meters. First, calculate the center, then subtract the offset after rotation to determine the upper-left corner. If there is a valid source window, the initial center and direction are based on that window, and the new window is shifted forward depending on the side of the eye. Windows that are nearly parallel or overlapping in range also participate in the depth spacing check. `STARTUP_DEPTH_OFFSET` is equal to `0.02` meters, and the offset is further restricted when approaching the eye. Remember this step when calculating the actual position of `center` using static mathematical examples, especially when multiple windows are opened consecutively.

## 4. The order of Euler angles and gimbal lock

### The three angles must be arranged in a clear order.

Start by placing a pen horizontally pointing to the right. After rotating the pen around the vertical axis of the table once, the tip changes direction. When rotating around the edge of the table again, the result depends on where the pen was rotated in the first step. The two rotations generally cannot be swapped. Take `eZ = (0,0,1)`; first rotate around `X` by `90°` to get `−eY`, then rotate around `Y` by `90°`, which still results in `−eY`. If the order is reversed, the first step yields `eX`, and the second step remains `eX`. Using this example to determine which multiplication occurs first can avoid ambiguity caused by the phrase "multiplication in sequence."

In the SDK, `quat_t::create_from_euler(v)` is input in degrees, and `v.x/v.y/v.z` represents the angle around `X/Y/Z`. The function returns `qZ·qY·qX`. When a vector enters the formula from the right, it first rotates around the fixed `X`, then around `Y`, and finally around `Z`. This is equivalent to using a grouped local intermediate axis to explain the same rotation matrix, but the reading order of the two methods is different. To avoid mistaking flight terminology for formulas, `α/β/γ` is used directly to represent the angle of `X/Y/Z` in the following text. Regardless of which axis is called pitch, yaw, or roll, only when the order matches the axis direction do the numbers make sense. The protocol's `metadata.rotation` is transmitted according to this set of three-axis degrees, while `tracking` and `pointer.rotation` transmit `[x,y,z,w]` quaternion components.

Write `R = Rz(γ)·Ry(β)·Rx(α)` using column vectors. You can compare it with the simplest matrix for rotating around `Y`, where the first column is `(cos β,0,−sin β)` and the third column is `(sin β,0,cos β)`. This indicates where the local `X` and `Z` axes point after rotation. Continuing to multiply by `Rz` and checking the first column gives `(cos γ·cos β, sin γ·cos β, −sin β)`. When the intermediate angle is `90°`, the first column simplifies to `(0,0,−1)`, which no longer changes with `γ`. The third and second columns also depend on `α` and `γ`, but only on their difference.

### Two control axes represent the same direction in a singular attitude.

Draw three rotatable iron rings on paper. Place the first ring inside the second, and then inside the third. When the outer ring is moved, the two inner rings are moved together. When standing upright, each movement can change direction. After the middle ring rotates by a right angle, one of the innermost axes will align with the axis of the outermost ring. Moving these two knobs actually involves adding or canceling angles on the same spatial axis.

The following formula provides an accurate representation using matrices. First, multiply `Ry(90°)·Rx(α)`, then multiply by `Rz(γ)`. Let `δ = α−γ`, and the result is

```text
R(α, 90°, γ) =
[  0      sin δ    cos δ ]
[  0      cos δ   −sin δ ]
[ −1        0        0   ]
```

As long as `δ` remains unchanged, adding any same value to both angles will result in the same attitude. `(0,90,0)` and `(90,90,90)` are an example. You can also consider the instantaneous axis of rotation. From the final attitude, changing the rightmost `α` will produce an increment around `Rz·Ry·eX`, while changing the leftmost `γ` always produces an increment around the fixed `eZ`. When `β = 90°`, the former is `−eZ`, and the latter is `+eZ`. The direction of parameter change is opposite, but the spatial lines are the same. The instantaneous effect of the three control knobs leaves only two independent directions, which is the degradation of degrees of freedom. When `β = −90°`, there is another combination, where the attitude depends only on `α+γ`.

The axis coincidence of Euler angles in ![and the axis-angle representation of unit quaternions in](/images/en/advanced_gimbal_lock_quaternion.png)

This explanation clarifies two easily confused issues. First, `(0,89,0)` and `(0,90,0)` differ only by the rotation around the same `Y` axis, which is `1°`. Second, although `(90,89,90)` and `(0,89,0)` have similar effects near the singular point, there is still a difference at `89°`. By substituting the values from the first column, we see that the horizontal magnitude of the former is `Y`, while that of the latter is `X`. However, near `90°`, both have very small horizontal magnitudes due to the common multiplication by `cos β`. This is also a region where numerical fluctuations are likely to occur. Even minor measurement errors can cause significant changes in two parameters of the Euler angles, but these changes cancel out, maintaining the object's direction stable.

The gimbal lock affects the independent control and reading of these angles near the point in question. The rigid body can still rotate around any axis. The so-called "loss of one degree of freedom" has practical consequences. For example, in animation systems using component addition to control the camera, under singular poses, two inputs originally assigned to `α` and `γ` become coaxial operations. If we continue with inverse calculation and then perform axis-by-axis interpolation, it may result in unnecessary large arcs. In many software, the three-axis manipulation interface allows direct incremental rotation around the world axis, so users may not feel the singularity of this parameter when dragging. To understand the internal representation, observe how changes are combined and how angles are derived from poses.

## 5. Quaternions start with an axis and an angle.

### Why use half-angles for axis-angle representation?

Using the unit vector `û` as the rotation axis and `θ` as the right-hand rotation angle. Mathematics textbooks often write quaternions as `(w, v)`, with the scalar before the vector. This mathematical notation will be used in the derivation below. In the actual SDK, the field order is `quat_t{x,y,z,w}`, with vector components first. When constructing a unit quaternion that rotates `θ` around `û`, the SDK should store `{ux·sin(θ/2), uy·sin(θ/2), uz·sin(θ/2), cos(θ/2)}`. The unit rotation is `{0,0,0,1}`. When using the scalar-before notation in textbooks, remember to switch back to the actual field order at code initialization.

Quaternion multiplication can be divided into dot product and cross product. Let `a=(s,u)` and `b=(t,v)` be given, then

```text
a · b = (s·t − u·v, s·v + t·u + u×v)
```

The dot product on the left represents quaternion multiplication, where `u·v` is the vector dot product. The field order can be verified using the first and last terms of `quat_t::operator*()`. As long as `u×v` has non-zero components, swapping the two operands will change the result. This aligns with the fact that actual rotations are non-exchangeable. Only by placing a regular vector `p` into pure quaternions `(0,p)` can quaternion multiplication be connected to vector rotation. Performing multiplication from the left only produces scalar components, changing the meaning of the problem. By applying `q·(0,p)·q⁻¹` from both sides, the scalar result is reset to zero.

Let `q = (c, û·s)` be defined, where `c = cos a` and `s = sin a` are involved. Since the axis is the unit vector `c²+s²=1`, the inverse quaternion is `(c,−û·s)`. By expanding the multiplication twice using the above product formula, the vector part becomes

```text
(c²−s²)·p + 2cs·(û×p) + 2s²·û·(û·p)
```

Now, `p` can be broken down into `p∥ = û·(û·p)` on parallel axes and `p⊥ = p−p∥` on perpendicular axes. The coefficient of the axial component becomes `c²−s²+2s² = 1`. The two terms on the perpendicular axis are `(c²−s²)·p⊥ + 2cs·(û×p⊥)`. These two vectors are equal in length and perpendicular to each other. According to trigonometric formulas `c²−s² = cos(2a)` and `2cs = sin(2a)`, they enable `p⊥` to rotate `2a` on a plane. If we want the vector to rotate `θ`, then `a=θ/2` must be used in quaternions. This is the origin of half-angles. It arises from the result of multiplying and applying to direction.

Substitute `û = eZ`, `θ = 90°`, and `p = eX`. The half-angle is `45°`, `c = s = √2/2`, and the axial projection is zero. By eliminating the first term in the equation, the coefficient of the second term is `1`, leaving `eZ×eX = eY`. Therefore, the code `quat_t::get_axis({0,0,1},90).rotate({1,0,0})` should yield a result close to `(0,1,0)`. `get_axis()` first checks that the angle is finite and the axis can be normalized, then uses `720°` to perform a modulus operation on the input and multiplies by `π/360`. This step also converts degrees to radians and performs half-angle transformation. Rotating around the same axis for `360°` will result in the same spatial rotation as `−q`. The representation value must rotate around `720°` to return to the original quaternions.

### Why can it be combined? Why use conjugate inversion?

Conjugating any quaternions changes the sign of the vector part. `q·q* = |q|²` is a pure scalar. The strict algebraic inverse is `q*/|q|²`. SDK for rotation first normalizes and then conjugates to ensure that the actual return is the inverse of a unit rotation. `quat_t::rotate()` also first normalizes the input rotation, then constructs `{v.x,v.y,v.z,0}`, executes `(q·p)·q⁻¹`, and takes the result `x/y/z`. The fields of quaternions may deviate slightly from unit length due to floating-point calculations, so these normalization steps are meaningful.

First convert `a` to a vector, then use `b` for conversion, expanding to `b·(a·p·a⁻¹)·b⁻¹`. Rearranging according to the associative law gives `(b·a)·p·(b·a)⁻¹`. Therefore, the product of quaternions indeed represents continuous rotation, with the right-hand side acting first. The combination of quaternion rotations maintains a unit norm, and in practice, regular normalization is still performed to control error accumulation. The four components of rotation are constrained by unit length, so there are actually only three degrees of freedom. The complete four values determine the pose, but `q` and `−q` represent the same pose. Looking at a single component, it is affected by both the axis direction and the half-angle, and cannot be directly read as the axis Euler angle.

### SLERP and current SDK interpolation implementation

The theoretical spherical linear interpolation first treats two unit quaternions as two points on a four-dimensional unit sphere. If the dot product is negative, the endpoint can be reversed to make the endpoints representing the same spatial pose fall on the shorter arc side. Then set `Ω = acos(a·b)`. When `0<t<1` and `sin Ω` can be stably calculated, strict SLERP uses the following formula.

```text
q(t) = sin((1−t)·Ω)/sin Ω · a + sin(t·Ω)/sin Ω · b
```

The denominator comes from the projection relationship of two endpoint vectors in the plane. The endpoint can be written as `b = cos Ω·a + sin Ω·n`, where `n` is a unit vector orthogonal to `a`. The point along the arc at the proportion of `t` is `cos(t·Ω)·a + sin(t·Ω)·n`. Eliminating `n` gives the above formula. When the two angles are very close, `sin Ω` is very small, and calculating the weight will amplify the error. Therefore, many implementations use linear approximation and then normalization in this range.

In this project, `quat_t::blend()` first performs dot product judgment and sign flipping, then calculates `a+(b−a)·t` component by component, and finally normalizes. The Python public method `quat.slerp()` is bound to this behavior. It is a normalized linear interpolation, often written as NLERP. For unit endpoints and the interval `[0,1]`, the direction changes along the same short arc, with differences in time proportion and spherical arc length proportion. Taking a fixed axis from `0°` to `120°` as an example, strict SLERP gives `30°` at `t=0.25`. At this time, the unnormalized norm and axial components of NLERP are `0.875` and approximately `0.2165`, respectively, with the ratio maintained. The inverse calculated angle is approximately `27.8°`. The poses at both ends are the same, but the speed in the middle is different. If the application requires a constant angular velocity, use the strict SLERP formula and retain the near-end point branch. SDK rotates the two handgrips according to phase changes to directly construct axis angle quaternions, so this interaction chain does not depend on interpolation speed.

## 6. Deriving Euler angles and quaternions from source code

The forward function `create_from_euler()` has only one multiplication expression, and the order of operations is already specified. To understand the inverse function, let’s define `a = α/2`, `b = β/2`, and `c = γ/2`. Use `sx/cx` to represent `sin a/cos a`, `sy/cy`, and `sz/cz`, respectively. First, write the four-dimensional quaternion with only one axis, then expand it according to `qZ·qY·qX` to obtain:

```text
x = sx·cy·cz − cx·sy·sz
y = cx·sy·cz + sx·cy·sz
z = cx·cy·sz − sx·sy·cz
w = cx·cy·cz + sx·sy·sz
```

The key to finding the inverse solution is to combine the components. Extract common factors from the expanded expression using `cy+sy` and `cy−sy`, then apply the sum and difference formulas.

```text
(w+y, x−z) = (cy+sy) · (cos(a−c), sin(a−c))
(w−y, x+z) = (cy−sy) · (cos(a+c), sin(a+c))
```

The first step for `quat_t::get_euler_angle_vector()` is `get_normalized()`. Next, calculate the lengths of the two pairs above, `difference = hypot(w+y,x−z)` and `sum = hypot(w−y,x+z)`. In the normalized branch `β∈[−90°,90°]`, `b` is in `[−45°,45°]`. Therefore, both `cy+sy` and `cy−sy` are non-negative, and the length is these two coefficients. It can be written using the sum formula as:

```text
difference = √2 · sin(b+π/4)
sum        = √2 · cos(b+π/4)
b+π/4      = atan2(difference,sum)
β          = 2·atan2(difference,sum) − π/2
```

This is the calculation formula for the source code `ry`. For the remaining two angles, calculate `first = atan2(x−z,w+y)` and `second = atan2(x+z,w−y)` from the source code. The former restores `a−c`, and the latter restores `a+c`, so `rx = first+second`, `rz = second−first`. The code uses `remainder(角度,2π)` to bring it close to the main value, then converts radians to degrees. If `β` is outside the normalized branch, the same pose can be expressed with another triplet. The inverse solution gives the representation on that branch. If comparing round trips, one should compare the rotated axis or the pose itself.

Also explain two singular point branches. When `β=90°`, `cy−sy=0`, the length of the second pair, `sum`, is zero, only `first` is defined. The code sets `second=first`, thus `rz=0`, and combines the original `α−γ` into `rx`. When `β=−90°`, the length of the first pair, `difference`, is zero, the code sets `first=second`, so still choose `rz=0`, and combine `α+γ` into `rx`. Implement using `epsilon` to determine lengths approaching zero. It selects a repeatable representative value under singularly shaped poses. For a continuous trajectory, this representative value may jump to another set of angles after passing the boundary, so rendering, tracking, and continuous interaction should be calculated first on the rotated representation, with angles suitable for configuration and display.

The verification formula can be done in three groups of calculations. A single-axis `(0,30°,0)` corresponds to `q = {0,sin 15°,0,cos 15°}`. The sine components in both pairs are zero, so `rx=rz=0`, only `30°` is inverted. The second group, `(20°,90°,10°)`, gives `rx≈10°、ry≈90°、rz=0°`. The third group takes `(20°,−90°,10°)`, with the representative value being `(30°,−90°,0°)`. By rotating the same group of three unit base axes with two poses, they can be verified to be equivalent. Near singular points, instead of comparing a single angle displayed, it’s better to check whether the local forward and upward vectors are in the same direction.

## 7. How does a cylinder curve out from a flat window

### Keep the arc length scale aligned with the same central plane

Place the center of the flat window at `(0,0,0)`; the surface is uncurved at `z=0`. Mark it with an arc length in the physical width direction at `u` and a vertical meter coordinate at `v`. Let the unit of positive curvature `κ` be per meter, and the radius `R=1/κ`. The center of the horizontal cross-section is at `(0,R)`. If the arc angle is defined as `φ = κ·u`, then the local center point is

```text
u = (left / w − 1/2)·W
v = (h/2 − top)·(W/w)
x = R·sin φ
y = v
z = R·(1 − cos φ)
```

At `u=0`, `x=z=0`, so the center and its tangent plane coincide with those of a flat window. As `|u|` grows toward either edge, `z` increases and the edges bend toward the front side at the center. The points satisfy `x²+(z−R)²=R²`. Arc length follows from the central angle: `u = R·φ`. The whole window spans `Θ=κW`, with the two edges at `−Θ/2` and `+Θ/2`. If `Θ` reaches one full turn, the edges overlap and a single point in space maps to more than one horizontal logical position. `window::set_curvature()`, physical size settings, and Engine's `present()` require `κ≥0` and `κW<2π`. The resize handle limits the total angle to just under `160°`. The SDK's `get_maximum_handle_curvature()` uses `nextafter` toward zero. The programmatic range and the interactive limit serve distinct purposes.

`service_runtime::get_surface_local_point()` directly returns `(u,v,0)` at `κ=0`. When bending, write `z` as `2·sin²(φ/2)/κ`. The identity `1−cos φ = 2·sin²(φ/2)` shows that they are equivalent. When the angle is very small, `cos φ` is close to `1`, and direct subtraction would discard many significant digits. The half-angle method reduces this reduction. Engineering can also check whether the surface scale is deformed through differentiation. Fixing `v`, differentiating along `u` gives `(cos φ,0,sin φ)`, with a constant length of `1`. Therefore, the horizontal pixels are still evenly distributed according to arc length. The front normal can be written as `n=(-sin φ,0,cos φ)`, returning to `+Z` at the center. Geometrically, this is a unit axis perpendicular to both the horizontal tangent and vertical directions.

![cylindrical cross-section, laser intersection, and arc length scale](/images/en/advanced_cylinder_raycast.png)

## 8. Reverse calculate the laser world point back to window pixels

### First transform the ray, then solve the plane

The ray is defined by the starting point `o` and direction `d`, with points along the ray being `p(t)=o+t·d`. If `d` has been normalized, `t` is measured in meters. `t≥0` only takes the side from the starting point towards the laser emission direction. Apply the inverse effect of the central pose to the starting point, only applying the rotation effect of the inverse pose to the direction. Thus, the ray in the window center system is written as `o′+t·d′`. The `z=0` on the flat window gives `o′z+t·d′z=0`, hence `t=−o′z/d′z`. If `d′z` is zero, the ray is parallel to the plane. When both terms are zero, there are infinitely many coplanar points. The program usually handles no available unique hits, and whether to retain the captured target is determined by the subsequent pointer state.

The SDK's `ui_runtime::intersect_plane()` is used for tracking controls after pressing, using `abs(ray.z) ≤ epsilon` to determine approximate parallelism, rejecting `t<0`. The returned ternary value is arranged according to `{t,local_x,local_y}`. Although this return value is carried by `vec3_t`, the semantics of the `x` field are distance parameters, while the `y/z` field is the horizontal and vertical coordinates of the plane. Engine's `service_runtime::intersect()` is used to select the window, and the plane branch rejects parallelism with `local_direction.z == 0`, also rejecting `t≤0` and non-finite values during the candidate filtering stage. Both functions use the same basic line equation, but their respective tolerance domains and output contracts are determined by the purpose of the call.

For example, the starting point of the center system ray is `(0.12,0.06,0.50)`, and the direction is `(0,0,−1)`. `t=0.50` is obtained in meters, hitting `(0.12,0.06,0)`. If the width and height are `640×360` and `s=1`, recalculate `left=320+120=440`, `top=180−60=120`. When checking `top`, a positive `y` for the hit point indicates it is above the center, and the pixel row number should be smaller than `180`. This intuitive verification is easier than doing coordinate algebra once.

### Expand the cylindrical equation and stabilize the root search

The cylindrical surface can be expanded from `x²+(z−R)²=R²` to `κ(x²+z²)−2z=0`. Here, the identical `R²` on both sides is removed, and the equation is multiplied by `κ`. By substituting the values of `x=ox+t·dx` and `z=oz+t·dz` for the ray, it is merged into `at²+bt+c=0`.

```text
a = κ·(dx²+dz²)
b = 2·[κ·(ox·dx+oz·dz)−dz]
c = κ·(ox²+oz²)−2oz
Δ = b²−4ac
```

Here, the apostrophes are omitted, and all quantities are within the central system of the window surface. If the direction is only along the cylindrical axis `Y`, there will be no unique cross-section intersection point, and `a=0` will be rejected. `Δ<0` indicates that the cross-section of the ray does not intersect the circle. `Δ=0` represents the tangent line, which has only one repeated root when it is tangent to the circle. `Δ>0` will yield two candidates, and the anterior and posterior roots need to be filtered based on arc length and height.

The common direct root formula `(−b±sqrt Δ)/(2a)` has a subtraction when two large values approach each other; the smaller root may quickly lose accuracy. The Engine first calculates `q=−0.5·(b+copysign(sqrt Δ,b))`, choosing to add the same sign to avoid reduction. Then, it sets the two roots as `q/a` and `c/q`. The second term can be verified by the product of the two roots `c/a`. When `q=0` is reached, `−b/(2a)` is used to obtain the repeated root. The code also involves dimensionless angular spans `κW` and `epsilon`. When the curvature is extremely small, it is calculated based on planar candidates, and then the inverse formula for the abscissa is determined based on the actual curvature components. This approach avoids forcing a very distant second cylindrical intersection point at extremely small curvatures.

For each candidate point, the arc angle is reconstructed using `κx=sin φ` and `1−κz=cos φ`. `atan2` considers two components, allowing for the distinction between left and right semicircles and another branch with the same sine value. Let `u = atan2(κx,1−κz)/κ` be the logical pixels consumed.

```text
left = (u/W + 1/2)·w
top  = h/2 − (y/W)·w
```

Typically, `0≤left≤w` and `0≤top≤h` are required. This is equivalent to restricting the cylinder to the angular segment and vertical height occupied by the window. The source code only retains positive and finite distances and finite pixels, then selects the valid root with the smallest distance. Do not only look at the smallest root after solving the quadratic equation. The smaller root may be located outside the window's arc segment, and the other is the finite surface seen by the user.

### An example of an arc surface that can be verified step by step

With a width of `W=1` meters, `κ=1` per meter, and `w=1000`, and taking `h=400`. The arc angles at the left and right boundaries of the window are `−0.5` and `+0.5` radians. Target pixels `left=750` and `top=200` correspond to `u=0.25` meters and `v=0`, with an arc angle of `0.25` radians. Substituting these into the forward model yields `x=sin(0.25)≈0.2474` and `z=1−cos(0.25)≈0.03109`. Placing a laser at `(sin 0.25,0,0.5)` with direction `(0,0,−1)`, the two intersection points at the fixed `x` are `z`, which are approximately `0.03109` and `1.96891`. The latter is larger than the ray origin and belongs to the negative `t`. The former yields `t≈0.46891` meters. Using `atan2` to calculate backward gives the original `0.25` radians, followed by `750` and `200`. If roughly converting using `x=0.2474` meters, it would be miscalculated as around `747.4`; the greater the window curvature, the larger the error in using chord position to represent arc length.

The normal line of the front side at the same point is `(−sin 0.25,0,cos 0.25)`. Its multiplication with the point `(0,0,−1)` here is negative, indicating front-side incidence. The Engine can find intersections on both the front and back sides. For the same surface point, the pixel conversion formula is exactly the same. The reverse image seen on the back side comes from the geometry and texture direction of the back-side Overlay. When the SDK starts capturing in the space, it uses the normal to multiply with the ray point, preserving `capture.backside`. When adjusting the curvature, it can be used to reverse the lateral effect of dragging. Choosing the correct front and back sides and selecting the nearest valid root are two different things.

When the window is in capture mode, the Engine first calculates the usual finite face hit, and then allows the `outside` mode to obtain the continuous coordinates outside the face. If there are no new intersection points temporarily and the target still has a valid pose, the capture state can be maintained. When no capture is possible, the Engine finds the nearest hit between the visible and interactable surfaces and additionally allows the edge range defined by `BEAM_MARGIN_LOGICAL_PIXEL` as a candidate for laser display. This ensures that the beam can still be seen near the edge, and interactive hits are still checked against the window boundaries. Control hits occur in the SDK, where the received `left/top` and the control's geometry are used for selection. When debugging cursor deviation, it is necessary to check whether the spatial ray reaches the window surface, whether the calculated window surface pixels are correct, and which control has been hit on the interface.

## 9. How window interaction uses these geometric quantities

### The relative pose saved by single-hand movement is preserved.

When holding the grip button to capture the window, the SDK uses the handle origin and rotation to determine the hand's pose `H₀`, and reads the window's world upper-left pose `A₀`. `rebase_window_grab()` preserves the relative relationship `G=H₀⁻¹·A₀`. Then, when the hand moves to `H₁`, `update_window_grab()` calculates the new window world pose `A₁=H₁·G`. The window properties to be updated are described in the current reference frame `R`, and finally written into `R⁻¹·A₁`. These three multiplications respectively answer "where the paper is in the hand when held," "where the paper is in the room now," and "convert the result back to the window's own coordinate system."

Saving the entire relative pose can simultaneously drive translation and rotation. Imagine using two fingers to pinch a point on the paper and rotate the wrist; other positions of the paper move along an arc. When the distance is greater, the same angle change corresponds to a larger lateral displacement. This is the geometric result of maintaining the original handle-to-target relative relationship. The relative relationship is established at the start of capture, and each subsequent use of the same `G` prevents the previous rounding error from accumulating in the next transformation.

### How eight control points define the two-handed rotation axis

There are eight control points around the window, numbered from top, upper right, right, lower right, bottom, lower left, left, and upper left, with their direction arrays being `ROTATION_HANDLE_DIRECTION_LIST`. Different control points must be held by both hands at the same time. When holding relative points, `window::get_rotation_axis()` first normalizes the window plane direction where "the first point points to the second point," and then uses `+Z × direction` to obtain the rotation axis within the window surface. Therefore, when holding up and down, the axis lies in the direction of `X`; when holding left and right, the axis lies in the direction of `Y`; when holding the diagonal, the axis is an inclined axis within the plane perpendicular to that diagonal. Swapping which hand occupies which point changes the axis sign. When the two held points are not relative, the source code returns `+Z`, which is used to rotate around the window surface normal. By selecting the points, users can fine-tune on the limited axis.

Each hand saves the hit distance at the start of capture. `update_window_rotation()` uses `controller origin + current direction × capture distance` to calculate two virtual grip points, and then subtracts `span=P_right−P_left`. This difference is first converted to the local axis of the window at the start of capture. For `Z` axis rotation, take `span.x、span.y` as `atan2`. For the in-plane axis `a=(ax,ay,0)`, the lateral direction is `span·(ay,−ax,0)`, and the vertical direction is `−span.z`. These two terms are the components of the vector in two orthogonal directions perpendicular to the rotation axis. `calculate_window_rotation_phase()` calculates the phase on the plane. When the projected length is less than `ROTATION_HANDLE_MINIMUM_SEPARATION=0.02` meters, the phase reading is unreliable, and it is paused first. When a valid phase is re-obtained, a new reference is established, and the jumps during the invalid period are not added to the window at once.

The phase changes sign at `π`. For example, if the previous frame is `179°`, the next frame is recorded as `−179°`, and the actual increment should be `2°`. The source code first takes the `remainder(delta, 2π)` difference between the two frames, then accumulates it. Then, it constructs an incremental quaternion from the accumulated angle and the fixed local axis, and multiplies it by the initial window rotation. The rotation center is saved at the start, and recalculated when updated, with the upper left corner being `A=center−R_new·(W/2,−H/2,0)`. Therefore, as the window rotates around the center, the upper left corner moves reasonably with the angle. If the window always rotates around the upper left corner, players will feel that the large window is being tossed back and forth in their hands. The phase method requires an effective connection between two points, but there is no need to guess which side of the curved surface both hands are on every frame.

### The control handles for size and curvature use the same capture approach

The zoom handle at the bottom right and the curvature handle at the bottom left are captured by the trigger. The SDK retains the distance and position of the initial hit, then subtracts the current laser point from the initial point at the same distance to obtain the local `(Δx,Δy,Δz)` of the window. This ensures stable relative displacement during handle dragging, avoiding jumps caused by changing surface intersection points per frame. When the Engine receives a request with `pointer_capture` and `lock_position`, it allows the visual endpoint of the beam to follow the capture point. When dragging ends, the target loses interaction eligibility, or the capture disappears, the SDK terminates the corresponding gesture.

The scaling must maintain the aspect ratio of `r=h/w`. If the width is changed by `dW`, the ideal displacement in the bottom right corner would be `(dW,−r·dW)`. Project the actual position onto `(1,−r)`, minimize `(Δx−dW)²+(Δy+r·dW)²`, and take the first derivative of `dW`.

```text
dW = (Δx − r·Δy) / (1 + r²)
```

which is `width_delta` in `update_pointer()`. For example, if `r=0.5` is dragged by `(0.10,−0.05)`, the numerator becomes `0.125` and the denominator `1.25`, so the width increases by `0.10` meters. If only horizontally dragged by `0.10`, the same formula yields `0.08` meters, because the system absorbs the gesture along a fixed ratio direction. Write back the physical scaling with `set_window_physical_width()` using `s=1000·W/w`, and limit the minimum width to at least `0.1` meters according to the interactive minimum. Also, tighten the curvature when necessary during magnification to ensure the arc angle remains within the control range.

The curvature handle uses lateral local displacement to calculate `κ_next=clamp(κ_initial ± 4·Δx,0,κ_max)`, with opposite symbols for front and back sides. `CURVATURE_DRAG_SENSITIVITY` is equal to `4.0`. The control handle also accepts the joystick. The curvature reads the joystick value `X`, modifies the total arc angle, with a maximum of `2` radians per second. Therefore, the increment of curvature must be divided by the current physical width. The size reads the joystick value `Y`, using `W_next=W_current·2.25^a`, where `a` is obtained by multiplying the normalized joystick speed by time. Accumulating logarithmic width is equivalent to multiplying by a ratio, with an upward movement lasting one second without touching the boundary resulting in `2.25` times the original value, and the same duration downward results in the reciprocal. Compared to a fixed increase of a few millimeters per second, the relative change speed of small and large windows is closer. The joystick has `128` as the neutral point, and the code first subtracts the dead zone, then normalizes the effective range on both sides.

The decision to flatten upon double-clicking comes from the last release of the curvature handle in the same gesture. When the window ID is the same and the interval between the next press and the last effective release does not exceed `CURVATURE_DOUBLE_CLICK_INTERVAL{500}` milliseconds, the SDK sets `curvature=0` and requires releasing the current button before starting the next gesture. It updates the path submission plane with the same normal attribute, and only the subsequent Engine refresh of the Overlay reflects the display state. Thus, it is possible to record the SDK curvature changes and the final Overlay presentation separately to troubleshoot timing issues where "the window is flattened but the old arc surface still appears."

## 10. Layer alignment and practice

When "the window is not displayed," first check if the reference frame has effective tracking, then check if the initial positioning is complete. If the control is misaligned, first reproduce it with unit rotation and `s=1`, then change only one item. Deviations caused only by size are usually related to half-width or scale units, while those caused only by headset rotation are usually related to direction changes. Deviations that only occur on curved surfaces can be tested with left and right symmetric points. The symmetric point should receive the opposite `x` and the same `z`; a hit should return to the symmetric `left`. If it is unstable when grabbed from the back, record the first normal vector symbol and the fixed capture distance afterward to distinguish between changes in wing-end hits and actual rotation axis changes.

You can use the following exercises to check if you have developed intuition.

1. If `w=800`, `h=400`, and `s=0.5`, what is `(left,top)=(200,300)` in the window center's system? Each pixel is half a millimeter, with the horizontal relative center being `−200` pixels and the vertical downward being `100` pixels. The answer is `(−0.10,−0.05,0)`. If you perform physical zoom on a width change, do not change both `w` and `s` for this problem at the same time.
2. If the total bending angle of `W=0.8` meters is `90°`, what is the curvature? First, convert the angle to `π/2`, then divide by `0.8` to get `κ≈1.9635` per meter. The number of circles used by OpenVR is `Θ/(2π)=0.25`, which has a different unit from the physical curvature of `1.9635`.
3. Why can’t a plane ray with a direction of `(1,0,0)` be determined solely based on its starting point? This is because when the equation `z` is substituted into `d_z=0`, all points along the ray have the same value for `z`. If the starting point is on the plane, then every point along the ray lies in the same plane. If the starting point is not on the plane, then there are no intersection points. To find the intersection function, we need a unique distance that can be used for interaction.
4. Why do button click handlers usually not need to know quaternions after receiving `left/top`? This is because the Engine has already converted the physical ray to the local window surface and restored the logical pixels. The SDK is only responsible for the control geometry, clipping, focus, and event chain at that time. The geometric layer and the interface layer check their own contracts separately, allowing for independent verification.

When reverse-verifying the source code, start with the `geometry/vec3.cpp`, `geometry/quat.cpp`, and `geometry/pose.cpp` of the SDK, then look at the reference transformation in `core/ui_runtime.cpp`, and finally connect to the `core/service_runtime.cpp` of the Engine and the `core/ui_runtime_input.cpp`, `core/ui_runtime_grab.cpp`, and `core/ui_runtime_scroll.cpp` of the SDK. Marking each component as pixels, meters, degrees, or radians allows for independent verification of the positive and negative signs and ratios of almost every formula.