---
title: "Finding Lyapunov function and region of attraction using convex optimization"
summary: "This post shows how to utilize sum-of-squares optimization to find Lyapunov function to prove global or local stability."
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

{{< paragraph name="ex:simple-nonlinear-system" >}}

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

{{< colab "simple-nonlinear-system.ipynb" >}}

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

{{< colab "simple-nonlinear-system.ipynb" >}}

Solving this SOS program also yields the same Lyapunov function.

{{< /paragraph >}}

Notice that in the example above, the system's dynamics are polynomial functions. However, rigid-body dynamics typically involve trigonometric functions. This can be mitigated by introducing new variables $s_i = \sin\theta_i$ and $c_i = \cos\theta_i$, along with the constraint $s_i^2 + c_i^2 = 1$.
The following example illustrates this approach.

{{< paragraph name="ex:pendulum-global-stability" >}}

<b>Example.</b> (Global stability of a pendulum)

{{< media src="figures/pendulum.svg" width="10rem" >}}

Consider the damped pendulum shown in the figure. Its equation of motion is given by

$$
ml^2 \ddot{\theta} + b \dot{\theta} + mgl \sin\theta = 0 .
$$

We introduce a coordinate transformation from $\begin{bmatrix} \theta & \dot{\theta} \end{bmatrix}^\top$ to $\bm{z} = \begin{bmatrix} s & c & \dot{\theta} \end{bmatrix}^\top$, where $s = \sin\theta$ and $c = \cos\theta$. In this new coordinate system, the system dynamics become

$$
\dot{\bm{z}} =
\begin{bmatrix} c \dot{\theta} \\ -s \dot{\theta} \\ -\frac{g}{l} s - \frac{b}{ml^2} \dot{\theta} \end{bmatrix} .
$$

To prove the global stability of the system, we parameterize the Lyapunov function as a second-degree polynomial in $\bm{z}$:

$$
V(\bm{z}) = \alpha_0 + \alpha_1 s + \alpha_2 c + \alpha_3 \dot{\theta} + \alpha_4 s^2 + \dots + \alpha_9 \dot{\theta}^2 .
$$

Its time derivative is given by

$$
\dot{V}(\bm{z}) = \frac{\partial V(\bm{z})}{\partial \bm{z}} \dot{\bm{z}} .
$$

To determine $V(\bm{z})$, we solve the following SOS optimization problem:

$$
\begin{align*}
  & \text{find} && \alpha_0, \dots, \alpha_9, \lambda_0, \dots, \lambda_9  \\
  & \text{subject to} && V(\bm{z})  \text{ is SOS}  \\
  &                   && -\dot{V}(\bm{z}) + \lambda(\bm{z}) (s^2+c^2-1) \text{ is SOS}  \\
  &                   && V(\begin{bmatrix} 0 & 1 & 0 \end{bmatrix}^\top) = 0 ,
\end{align*}
$$

where $\lambda(\bm{z})$ is a second-degree polynomial of the form:

$$
\lambda(\bm{z}) = \lambda_0 + \lambda_1 s + \dots + \lambda_9 \dot{\theta}^2 .
$$

The second SOS constraint ensures that

$$
-\dot{V}(\bm{z}) \geq -\lambda(\bm{z}) (s^2 + c^2 - 1) ,
$$

which implies $-\dot{V}(\bm{z}) \geq 0$ whenever $s^2 + c^2 = 1$.

{{< colab "pendulum-global-stability.ipynb" >}}

Solving the SOS program for $m=1$, $l=1$, $g=9.81$, and $b=0$ gives the Lyapunov function:

$$
\begin{split}
V &= 0.5 \dot{\theta}^{2} + 4.905 s^2 + 4.905 (1 - c)^2  \\
  &= 0.5 \dot{\theta}^{2} + 9.81 (1 - c) .
\end{split}
$$

This turns out to be the total energy of the system.

{{< /paragraph >}}


## Finding the region of attraction

Sometimes, global stability is too much to ask for. For example, when balancing a robot using a controller, a disturbance that deviates the robot from its equilibrium configuration too much can still cause it to fall. Therefore, we aim to identify the largest region in which the system remains Lyapunov stable.

For a given dynamical system

$$
\dot{\bm{x}} = f(\bm{x}),
$$

where $f$ is continuous. If there exists a scalar function $V(\bm{x})$ such that

$$
V(\bm{x}) > 0 \quad \forall \bm{x} \neq \bm{0}, \quad V(\bm{0}) = 0,
$$

then a bounded sublevel set

$$
\mathcal{G} = \bigl\{ \bm{x} \mid V(\bm{x}) \leq \rho \bigr\}
$$

defines a region of attraction (ROA), provided that

$$
\dot{V}(\bm{x}) \leq 0 \quad \forall \bm{x} \in \mathcal{G}.
$$


### Known Lyapunov function
<a name="sec:roa-with-known-lyapunov"></a>

In this section, we assume that the Lyapunov function is known exactly. This is not necessarily a bad assumption, as several methods provide explicit Lyapunov functions. For example, in a closed-loop system with an LQR controller, the cost-to-go function serves as a Lyapunov function. Alternatively, we can linearize a system at its equilibrium point, yielding the linearized system matrix $\mathbf{A}$. The solution $\mathbf{P}$ to the Lyapunov equation

$$
\mathbf{A}^\top \mathbf{P} + \mathbf{P} \mathbf{A} = -\mathbf{Q}
$$

where $\mathbf{Q} \succ 0$, provides a quadratic Lyapunov function of the form

$$
V(\bm{x}) = \bm{x}^\top \mathbf{P} \bm{x}.
$$

Nonetheless, we will later relax this requirement.

**Formulation 1**

To determine the ROA, we can formulate the following optimization problem:

$$
\begin{align*}
  & \text{maximize}   && \rho  \\
  & \text{subject to} && -\dot{V}(\bm{x}) + \lambda(\bm{x}) (V(\bm{x}) - \rho) \text{ is SOS}  \\
  &                   && \lambda(\bm{x}) \text{ is SOS}.
\end{align*}
$$

In this formulation, $V(\bm{x})$ and $\dot{V}(\bm{x})$ are known and fixed, while the decision variables are $\rho$ and the coefficients of the polynomial $\lambda(\bm{x})$. The first SOS constraint ensures that

$$
\dot{V}(\bm{x}) \leq \lambda(\bm{x}) (V(\bm{x}) - \rho) ,
$$

which implies $\dot{V}(\bm{x}) \leq 0$ for all $\bm{x}$ satisfying $V(\bm{x}) \leq \rho$. However, this optimization problem is not convex, as it involves bilinear terms in the decision variables.

**Formulation 2**

An alternative formulation of the optimization problem is

$$
\begin{align*}
  & \text{maximize}   && \rho  \\
  & \text{subject to} && (\bm{x}^\top \bm{x})^d (V(\bm{x}) - \rho) - \lambda(\bm{x}) \dot{V}(\bm{x}) \text{ is SOS}  \\
  &                   && \lambda(\bm{x}) \text{ is SOS} ,
\end{align*}
$$

where $d$ is a fixed positive integer.
The first SOS constraint ensures that

$$
\lambda(\bm{x}) \dot{V}(\bm{x}) \leq (\bm{x}^\top \bm{x})^d (V(\bm{x}) - \rho) ,
$$

which implies $\dot{V}(\bm{x}) \leq 0$ for all $\bm{x}$ satisfying $V(\bm{x}) \leq \rho$.
Unlike the previous formulation, this optimization problem is convex and can be solved efficiently to determine the ROA, given by $\{ \bm{x} \mid V(\bm{x}) \leq \rho \}$.

**Formulation 3**

We claim that the SOS constraint on $\lambda(\bm{x})$ is unnecessary, leading to the simplified optimization problem:

$$
\begin{align*}
  & \text{maximize}   && \rho  \\
  & \text{subject to} && (\bm{x}^\top \bm{x})^d (V(\bm{x}) - \rho) + \lambda(\bm{x}) \dot{V}(\bm{x}) \text{ is SOS} .
\end{align*}
$$

Why is this possible? First, note that $\dot{V}(\bm{x}) < 0$ in the vicinity of the origin, except at the origin itself.
Additionally, observe that whenever $\dot{V}(\bm{x}) = 0$, we have $V(\bm{x}) - \rho \geq 0$. Since $\dot{V}(\bm{x})$ is continuous, it follows that $\dot{V}(\bm{x}) < 0$ for all $\bm{x}$ satisfying $V(\bm{x}) - \rho < 0$, except at the origin.

The following example shows how this formulation can be used to find the ROA.

{{< paragraph name="ex:van-der-pol" >}}

<b>Example.</b> (Time-reversed van der Pol oscillator)

The time-reversed van der Pol oscillator is governed by

$$
\begin{align*}
  \dot{x}_1 &= -x_2 ,  \\
  \dot{x}_2 &= x_1 + (x_1^2 - 1) x_2 .
\end{align*}
$$

The phase portrait of the system is shown in the figure below.

{{< media src="figures/van-der-pol-phase-portrait.svg" width="25rem" >}}

The system has an equilibrium at the origin and a ROA highlighted in red. Near the origin, the linearized system is

$$
\begin{bmatrix} \dot{x}_1 \\ \dot{x}_2 \end{bmatrix} =
\underbrace{\begin{bmatrix} 0 & -1 \\ 1 & -1 \end{bmatrix}}_{\mathbf{A}}
\begin{bmatrix} x_1 \\ x_2 \end{bmatrix} .
$$

Solving the Lyapunov equation $\mathbf{A}^\top \mathbf{P} + \mathbf{P} \mathbf{A} = -\mathrm{diag}(\begin{bmatrix} 1 & 2 \end{bmatrix})$ gives us a Lyapunov function $V(\bm{x}) = \bm{x}^\top \mathbf{P} \bm{x}$.

Solving the SOS optimization problem

$$
\begin{align*}
  & \text{maximize}   && \rho  \\
  & \text{subject to} && (\bm{x}^\top \bm{x})^d (V(\bm{x}) - \rho) + \lambda(\bm{x}) \dot{V}(\bm{x}) \text{ is SOS} ,
\end{align*}
$$

gives the ROA: $\{ \bm{x} \mid V(\bm{x}) \leq \rho \}$.

{{< colab "van-der-pol.ipynb" >}}

<br>

{{< media src="figures/van-der-pol-contour.svg" width="25rem" >}}

The solved ROA (highlighted in yellow) is a subset of the true ROA (highlighted in red). We can clearly see in the figure that for all $\bm{x}$ satisfying $\dot{V}(\bm{x}) = 0$, $V(\bm{x}) \geq \rho$.

{{< /paragraph >}}


### Searching for both Lyapunov function and ROA

The [previous section](#known-lyapunov-function) assumes that the Lyapunov function is known exactly. Is this section, we relax this requirement and simultaneously search for both the Lyapunov function and the ROA.

We formulate the following optimization problem:

$$
\begin{align*}
  & \text{maximize}   && \mathrm{vol}(\{ \bm{x} \mid V(\bm{x}) \leq \rho \})  \\
  & \text{subject to} && (\bm{x}^\top \bm{x})^d (V(\bm{x}) - \rho) + \lambda(\bm{x}) \dot{V}(\bm{x}) \text{ is SOS}  \\
  &                   && V(\bm{x}) \text{ is SOS} ,
\end{align*}
$$

Here, we maximize the volume of the sublevel set. The decision variables in this optimization problem are $\rho$, the coefficients of $\lambda(\bm{x})$, and the coefficients of $V(\bm{x})$, which also determine $\dot{V}(\bm{x})$.  However, this optimization problem is not convex due to the presence of bilinear terms in the decision variables.

To address this, we employ [coordinate decent](https://wikipedia.org/wiki/Coordinate_descent).  We partition the decision variables into two coordinate blocks:
- $\rho$ and the coefficients of $\lambda(\bm{x})$ in one block,
-  coefficients of $V(\bm{x})$ in the other block.

At iteration $(k+1)$, the algorithm proceeds as follows:

1. **Update $\rho^{(k+1)}$ and $\lambda^{(k+1)}(\bm{x})$**\
Solve following SOS optimization problem:

$$
\begin{align*}
  & \text{maximize}   && \rho  \\
  & \text{subject to} && (\bm{x}^\top \bm{x})^d (V^{(k)}(\bm{x}) - \rho) + \lambda(\bm{x}) \dot{V}^{(k)}(\bm{x}) \text{ is SOS} .
\end{align*}
$$

2. **Update $V^{(k+1)}(\bm{x})$**\
Solve the following optimization problem:

$$
\begin{align*}
  & \text{maximize}   && \mathrm{vol}(\{ \bm{x} \mid V(\bm{x}) \leq \rho^{(k+1)} \})  \\
  & \text{subject to} && (\bm{x}^\top \bm{x})^d (V(\bm{x}) - \rho^{(k+1)}) + \lambda^{(k+1)}(\bm{x}) \dot{V}(\bm{x}) \text{ is SOS}  \\
  &                   && V(\bm{x}) \text{ is SOS} .
\end{align*}
$$

This optimization problem is usually non-convex in the objective. Fortunately, in coordinate decent, a sufficient decent in each coordinate direction is enough to guarantee convergence. Therefore, suppose $V^{(k)}(\bm{x}) = \bm{x}^\top \mathbf{P}^{(k)} \bm{x}$, what we usually do in step 2 of the algorithms is to first assign

$$
\mathbf{P}^{(k+\tfrac{1}{2})} = \frac{1}{\rho^{(k+1)}} \mathbf{P}^{(k)} .
$$

Next, we solve for $\mathbf{P}^{(k+1)}$ using

$$
\begin{align*}
  & \text{maximize}   && (\det\mathbf{P}^{(k+\frac{1}{2})})^{-\frac{1}{2}} - \tfrac{1}{2} (\det\mathbf{P}^{(k+\frac{1}{2})})^{-\frac{1}{2}} \mathrm{Tr}\bigl( (\mathbf{P}^{(k+\frac{1}{2})})^{-1} (\mathbf{P} - \mathbf{P}^{(k+\frac{1}{2})}) \bigr)  \\
  & \text{subject to} && (\bm{x}^\top \bm{x})^d (V(\bm{x}) - 1) + \lambda^{(k+1)}(\bm{x}) \dot{V}(\bm{x}) \text{ is SOS}  \\
  &                   && V(\bm{x}) \text{ is SOS}  \\
  &                   && V(\bm{x}) = \bm{x}^\top \mathbf{P} \bm{x} .
\end{align*}
$$

Here, the objective is the linearization of $(\det\mathbf{P})^{-\frac{1}{2}}$ at $\mathbf{P} = \mathbf{P}^{(k+\frac{1}{2})}$ [[2](#ref2), Eq. 42], which is proportional to the volume of $\{ \bm{x} \mid V(\bm{x}) \leq 1 \}$.

<!-- Finally, we perform an [Armijo line search](https://wikipedia.org/wiki/Backtracking_line_search) to ensure sufficient decent. Given a parameter $\alpha \in (0,1)$, we start with $t=1$ and iteratively update

$$
t \gets 0.5 t , \qquad
\mathbf{P}^{(k+1)} = \mathbf{P}^{(k+\tfrac{1}{3})} + t (\mathbf{P}^{(k+\tfrac{2}{3})} - \mathbf{P}^{(k+\tfrac{1}{3})}) ,
$$

until the following condition is met:

$$
\begin{split}
(\det\mathbf{P}^{(k+1)})^{-\frac{1}{2}} &< (\det\mathbf{P}^{(k+\tfrac{1}{3})})^{-\frac{1}{2}} \\ &\qquad - \alpha \tfrac{1}{2} (\det\mathbf{P}^{(k+\frac{1}{3})})^{-\frac{1}{2}} \mathrm{Tr}\bigl( (\mathbf{P}^{(k+\frac{1}{3})})^{-1} (\mathbf{P}^{(k+1)} - \mathbf{P}^{(k+\frac{1}{3})}) \bigr) .
\end{split}
$$ -->

This approach can be readily extended to other forms of $V(\bm{x})$ beyond the quadratic form $V(\bm{x}) = \bm{x}^\top \mathbf{P} \bm{x}$ by selecting an alternative volume metric in place of $(\det\mathbf{P})^{-\frac{1}{2}}$.


{{< paragraph name="ex:van-der-pol-revisited" >}}

<b>Example.</b> (Time-reversed van der Pol oscillator revisited)

The time-reversed van der Pol oscillator is governed by

$$
\begin{align*}
  \dot{x}_1 &= -x_2 ,  \\
  \dot{x}_2 &= x_1 + (x_1^2 - 1) x_2 .
\end{align*}
$$

We apply the described method above to find a quadratic Lyapunov function of the form $V(\bm{x}) = \bm{x}^\top \mathbf{P} \bm{x}$ and determine the ROA.

{{< colab "van-der-pol-lyapunov-search.ipynb" >}}

<br>

{{< media src="figures/van-der-pol-quadratic-roa.svg" width="20rem" >}}

The green region represents the computed ROA, while the yellow region corresponds to the solution from the [previous example](#ex:van-der-pol). By allowing the Lyapunov function to vary, we obtain a larger ROA compared to the fixed Lyapunov function approach.

Can we get a better approximation?

{{< /paragraph >}}


## References

{{< references

"H. K. Khalil, *Nonlinear Systems*, 3 ed. Pearson, 2001."

"K. B. Petersen and M. S. Pedersen. [*The Matrix Cookbook*](http://www2.compute.dtu.dk/pubdb/edoc/imm3274.pdf), Technical University of Denmark, 2012."

"R. Tedrake. [*Underactuated Robotics: Algorithms for Walking, Running, Swimming, Flying, and Manipulation*](https://underactuated.csail.mit.edu), 2025."

>}}