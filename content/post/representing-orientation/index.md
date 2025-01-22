---
title: "Representing orientation: $SO(3)$ matrix and quaternion"
summary: "Proper ways to represent rigid body orientation"
date: 2025-01-22
draft: true
authors:
  - Wei-Chen Li
---

In this blog post, we will see how to represent the orientation of a rigid body with $SO(3)$ matrix and quaternion, their time derivatives, and how to formulate them in an optimization problem.

## Orientation of a rigid body

We attach a frame (a set of three orthogonal unit vectors) to a rigid body, and describe its orientation as the transformation from this frame to the world frame.

### SO(3) matrix
The $SO(3)$ is the set of all $3 \times 3$ matrices defined by

$$
  SO(3) \coloneqq \{ \mathbf{T} \in \mathbb{R}^{3 \times 3} \,\vert\, \mathbf{T}^\top \mathbf{T} = \mathbf{T} \mathbf{T}^\top = \mathbf{I}, \mathrm{det}(\mathbf{T}) = 1 \} .
$$

### Quaternion
