---
title: "Finding Lyapunov function and region of attraction using convex optimization"
summary: "This post shows how to perform Lyapunov analysis using convex optimization."
date: 2025-01-24
lastmod: 2025-01-24
draft: false
authors:
  - Wei-Chen Li
---

## Finding Lyapunov functions

<div class="rounded-border">

<b>Example.</b> Consider the nonlinear system:

$$
\begin{align*}
  \dot{x}_1 &= -x_1 - 2 x_2^2 ,  \\
  \dot{x}_2 &= -x_2 - x_1 x_2 - 2 x_2^3 .
\end{align*}
$$

To certify the stability of this system, we seek a Lyapunov function $V(\bm{x})$ that is positive-definite and ensure $\dot{V}(\bm{x})$ is negative-definite. We parameterize $V(\bm{x})$ as

$$
V(\bm{x}) = \frac{1}{2} \bm{x}^\top \underbrace{\begin{bmatrix} a_{11} & a_{21} \\ a_{21} & a_{22} \end{bmatrix}}_{\mathbf{A}} \bm{x} ,
$$

Here, $V(\bm{x})$ is positive-definite if $\mathbf{A} \succeq 0$. The time derivative of $V(\bm{x})$ is given by

$$
\begin{split}
  \dot{V}(\bm{x})
  &= \bm{x}^\top \mathbf{A} \dot{\bm{x}}  \\
  &= -a_{11} x_1^2 -2 a_{11} x_1 x_2^2 -a_{21} x_1^2 x_2 \\
  &\hspace{4mm} -2 a_{21} x_1 x_2^3 -2 a_{21} x_1 x_2 -2 a_{21} x_2^3 \\
  &\hspace{4mm} -a_{22} x_1 x_2^2 -2 a_{22} x_2^4 -a_{22} x_2^2 .
\end{split}
$$

To ensure $\dot{V}(\bm{x})$ is negative-definite, we parameterize it as

$$
\dot{V}(\bm{x}) = -
  \begin{bmatrix} x_1 \\ x_2 \\ x_1x_2 \\ x_2^2 \end{bmatrix}^\top
  \underbrace{\begin{bmatrix} b_{11} &&& \text{symm} \\ b_{21} & b_{22} && \\ b_{31} & b_{32} & b_{33} & \\ b_{41} & b_{42} & b_{43} & b_{44} \end{bmatrix}}_{\mathbf{B}}
  \begin{bmatrix} x_1 \\ x_2 \\ x_1x_2 \\ x_2^2 \end{bmatrix} .
$$

Here, $\dot{V}(\bm{x})$ is negative-definite if $\mathbf{B} \succeq 0$.
To find a Lyapunov function that proves stability, we solve the following convex optimization problem:

$$
\begin{align*}
  & \text{find} && a_{11}, a_{21}, a_{22}, b_{11}, \dots, b_{44}  \\
  & \text{subject to} && \mathbf{A} \succeq 0 \\
  &                   && \mathbf{B} \succeq 0 \\
  &                   && b_{11} = a_{11} \quad b_{21} = a_{21} \quad b_{22} = a_{22} \quad b_{31} = \tfrac{1}{2} a_{21} \\
  &                   && b_{32} + b_{41} = a_{11} + \tfrac{1}{2} a_{22} \\
  &                   && b_{33} = 0 \quad b_{42} = a_{21} \quad b_{43} = 2 a_{21} \quad b_{44} = 2 a_{22} .
\end{align*}
$$

[Solving this semi-definite program (SDP)](https://colab.research.google.com/drive/1TSDaUau11-rVg7fH8REdvzqAWLlLPS9n) yields $a_{11}=1, a_{21}=0, a_{22}=2$. The resulting Lyapunov function is

$$
V(\bm{x}) = \frac{1}{2} \bm{x}^\top \begin{bmatrix} 1 & 0 \\ 0 & 2 \end{bmatrix} \bm{x} .
$$

This technique, which involves expressing a function as a quadratic form and ensuring the associated matrix is positive semi-definite, is encapsulated as sum-of-squares (SOS) programming. Hence, we can alternatively solve the following SOS optimization problem:

$$
\begin{align*}
  & \text{find} && a_{11}, a_{21}, a_{22}  \\
  & \text{subject to} && V(\bm{x}) \text{ is SOS} \\
  &                   && -\dot{V}(\bm{x}) \text{ is SOS} .
\end{align*}
$$
[Solving this SOS program](https://colab.research.google.com/drive/1TSDaUau11-rVg7fH8REdvzqAWLlLPS9n) also yields the same Lyapunov function.
</div>
