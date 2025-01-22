---
title: "Extension of compressive sampling for eddy current 3D reconstruction"
authors:
- Wei-Chen Li
date: "2024-08-01"
doi: "10.6342/NTU202400686"

# Publication type.
# Accepts a single type but formatted as a YAML list (for Hugo requirements).
# Enter a publication type from the CSL standard.
publication_types: ["thesis"]

# Publication name and optional abbreviated publication name.
publication: "Master's Thesis, National Taiwan University"

abstract: "With the advent of Industry 4.0, ensuring the quality inspection of large structures has become increasingly crucial. Traditional raster scanning methods necessitate sampling at more than twice the spatial frequency to achieve a desired spatial resolution. Another sampling paradigm, known as compressive sampling, exploits signal sparsity to achieve the same resolution using fewer samples than Nyquist sampling would otherwise require. However, compressive sampling, which rely solely on sparsity, encounter challenges when a detailed depth resolution is necessary. In this study, 3D reconstruction refers to reconstructing both the position and depth of defects within a structure. The key is that defects in structures are binary; they are either present (represented as 1) or absent (represented as 0). Therefore, the signal of interest is not only sparse but also binary, or in some instances, have values between 0 and 1 to indicate partial defects in certain regions.
This study focuses on the recovery of binary vectors from linear measurements with two approaches. One approach relaxes the binary constraint and employs convex optimization algorithms to solve the problem. Additionally, convergence of the algorithm is proved. Another approach introduces a Bernoulli prior on the vector and computes the variational approximation of the posterior probability of the vector conditioned on the measurements. These algorithms can be adapted to recover unit interval vectors. The convex method inherently handles the recovery of unit interval vectors, while the probabilistic inference-based algorithms can be modified with a beta prior to achieve this as well. These algorithms are tested using measurement matrices that are either Gaussian random or have collinear columns, and demonstrate superior performance compared to existing compressive sampling algorithms on binary vector recovery tasks.
On the application side, perturbation analysis is applied to linearize the relationship between the magnetic flux density measurements and the material properties of the inspected structure. The linearized sensitivity matrix is essentially the inner product of two electric fields: one induced by electric current density in the coil, and the other induced by a point magnetic current density at the magnetic sensor. For efficient calculation of the sensitivity matrices, semi-analytical solutions are derived for the electromagnetic fields in several geometries and validated against finite element methods.
Binary vector recovery algorithms are applied to provide 3D reconstructions of defects in a multilayer metal plate, using both numerically simulated and experimental data. The results show that the developed algorithms provide superior depth resolution and reconstruction quality compared to existing compressive sampling algorithms. Specifically, the sensing system is capable of reconstructing defects as small as 2~mm with a depth resolution of 0.5~mm, using a magnetic sensor array with 4~mm intervals. Another example applies unit interval vector recovery algorithms to the inspection of a metal pipe. Reconstructions are merged together as the sensing probe move along the pipe. These two examples not only highlight the potential of efficient sampling in eddy current sensing, but also establish a foundation for applying the extension of compressive sampling to a broader range of physical reconstruction problems."

tags:

featured: false

# links:
# - name: ""
#   url: ""
url_pdf: 'https://tdr.lib.ntu.edu.tw/jspui/retrieve/2743f19a-7031-46db-ba9c-0aa1b06b21c1/ntu-112-2.pdf'
url_code: ''
url_dataset: ''
url_poster: ''
url_project: ''
url_slides: ''
url_source: ''
url_video: ''
---
