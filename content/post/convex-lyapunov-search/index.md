---
title: "Finding Lyapunov function and region of attraction using convex optimization"
summary: "This post shows how to utilize convex optimization to find Lyapunov function to prove global or local stability."
date: 2025-01-24
lastmod: 2025-01-24
draft: false
authors:
  - Wei-Chen Li
---

Lyapunov analysis is a method used to evaluate the stability of a dynamical system described by

$$
\dot{\bm{x}} = f(\bm{x}),
$$

where $\bm{x} \in \mathbb{R}^n$, and the system has an equilibrium point at $\bm{x} = \bm{0}$. If the equilibrium point is not located at the origin, a change of coordinates can shift it to $\bm{x} = \bm{0}$.

For a region $\mathcal{D}$ surrounding the origin, the system is considered stable in the sense of Lyapunov (i.s.L.) if a function $V: \mathbb{R}^n \to \mathbb{R}$ can be found such that:

1. $V(\bm{x}) > 0 \quad \forall \bm{x} \in \mathcal{D} \setminus \{\bm{0}\}, \quad V(\bm{0}) = 0$,
2. $\dot{V}(\bm{x}) \leq 0 \quad \forall \bm{x} \in \mathcal{D} \setminus \{\bm{0}\}, \quad \dot{V}(\bm{0}) = 0$.

In this case, $V(\bm{x})$ is known as a Lyapunov function. For more details and formal proofs, refer to [[1](#ref1), Ch 4].



## Finding Lyapunov function

When I first learned about Lyapunov functions, I was told they are notoriously difficult to find—so much so that discovering one could be worthy of publication. Surprisingly, convex optimization offers a practical method for finding Lyapunov functions. The approach involves parameterizing a set of candidate Lyapunov functions and then optimizing these parameters to search within the candidate set. The key advantage is that the optimization problem is convex in the parameter space, allowing for straightforward feasibility results. This is best demonstrated using an example.

<div class="rounded-border">

<b>Example.</b> Consider the nonlinear system:

$$
\begin{align*}
  \dot{x}_1 &= -x_1 - 2 x_2^2 ,  \\
  \dot{x}_2 &= -x_2 - x_1 x_2 - 2 x_2^3 .
\end{align*}
$$

To certify the stability of this system, we seek a Lyapunov function $V(\bm{x})$ that is positive and ensure $\dot{V}(\bm{x})$ is negative. We parameterize $V(\bm{x})$ as

$$
V(\bm{x}) = \frac{1}{2} \bm{x}^\top \underbrace{\begin{bmatrix} p_{11} & p_{21} \\ p_{21} & p_{22} \end{bmatrix}}_{\mathbf{P}} \bm{x} ,
$$

Here, $V(\bm{x})$ is positive if $\mathbf{P} \succeq 0$. The time derivative of $V(\bm{x})$ is given by

$$
\begin{split}
  \dot{V}(\bm{x})
  &= \bm{x}^\top \mathbf{P} \dot{\bm{x}}  \\
  &= -p_{11} x_1^2 -2 p_{11} x_1 x_2^2 -p_{21} x_1^2 x_2 \\
  &\hspace{4mm} -2 p_{21} x_1 x_2^3 -2 p_{21} x_1 x_2 -2 p_{21} x_2^3 \\
  &\hspace{4mm} -p_{22} x_1 x_2^2 -2 p_{22} x_2^4 -p_{22} x_2^2 .
\end{split}
$$

To ensure $\dot{V}(\bm{x})$ is negative, we parameterize it as

$$
\dot{V}(\bm{x}) = -
  \begin{bmatrix} x_1 \\ x_2 \\ x_1x_2 \\ x_2^2 \end{bmatrix}^\top
  \underbrace{\begin{bmatrix} q_{11} &&& \text{symm} \\ q_{21} & q_{22} && \\ q_{31} & q_{32} & q_{33} & \\ q_{41} & q_{42} & q_{43} & q_{44} \end{bmatrix}}_{\mathbf{Q}}
  \begin{bmatrix} x_1 \\ x_2 \\ x_1x_2 \\ x_2^2 \end{bmatrix} .
$$

Here, $\dot{V}(\bm{x})$ is negative if $\mathbf{Q} \succeq 0$.
To find a Lyapunov function that proves stability, we solve the following convex optimization problem:

$$
\begin{align*}
  & \text{find} && p_{11}, p_{21}, p_{22}, q_{11}, \dots, q_{44}  \\
  & \text{subject to} && \mathbf{P} \succeq 0 \\
  &                   && \mathbf{Q} \succeq 0 \\
  &                   && q_{11} = p_{11} \quad q_{21} = p_{21} \quad q_{22} = p_{22} \quad q_{31} = \tfrac{1}{2} p_{21} \\
  &                   && q_{32} + q_{41} = p_{11} + \tfrac{1}{2} p_{22} \\
  &                   && q_{33} = 0 \quad q_{42} = p_{21} \quad q_{43} = 2 p_{21} \quad q_{44} = 2 p_{22} .
\end{align*}
$$

<a target="_blank" href="https://colab.research.google.com/github/wei-chen-li/wei-chen-li.github.io/blob/main/content/post/convex-lyapunov-search/notebooks/simple-nonlinear-system.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open in Colab" class="no-margin"/>
</a>

Solving this semi-definite program (SDP) yields $p_{11}=1, p_{21}=0, p_{22}=2$. The resulting Lyapunov function is

$$
V(\bm{x}) = \frac{1}{2} \bm{x}^\top \begin{bmatrix} 1 & 0 \\ 0 & 2 \end{bmatrix} \bm{x} .
$$

This technique, which involves expressing a function as a quadratic form and ensuring the associated matrix is positive semi-definite, is encapsulated as sum-of-squares (SOS) programming. Hence, we can alternatively solve the following SOS optimization problem:

$$
\begin{align*}
  & \text{find} && p_{11}, p_{21}, p_{22}  \\
  & \text{subject to} && V(\bm{x}) \text{ is SOS} \\
  &                   && -\dot{V}(\bm{x}) \text{ is SOS} .
\end{align*}
$$

<a target="_blank" href="https://colab.research.google.com/github/wei-chen-li/wei-chen-li.github.io/blob/main/content/post/convex-lyapunov-search/notebooks/simple-nonlinear-system.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open in Colab" class="no-margin"/>
</a>

Solving this SOS program also yields the same Lyapunov function.
</div>


## References

[1]	H. K. Khalil, *Nonlinear Systems*, 3 ed. Pearson, 2001. <a name="ref1"></a>