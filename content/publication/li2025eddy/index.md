---
title: "Eddy current defect tomography using a hybrid binary vector recovery algorithm"
authors:
- Wei-Chen Li
- Chun-Yeon Lin
date: 2025-05-20
publishDate: 2025-01-14
doi: "10.1109/TMECH.2025.3565800"

# Publication type.
# Accepts a single type but formatted as a YAML list (for Hugo requirements).
# Enter a publication type from the CSL standard.
publication_types: ["article-journal"]

# Publication name and optional abbreviated publication name.
publication: "*IEEE/ASME Transactions on Mechatronics*"

abstract: This article presents an eddy current tomography framework for imaging defects in metal structures. The tomography problem is formulated as a linear inverse problem with a binary solution vector. A Bayesian approach is utilized, incorporating a binary-inducing prior and determining the posterior probability conditioned on the measurements. Since recovering binary vectors from underdetermined linear measurements is NP-hard, an approximation to the true posterior is obtained by minimizing a (KL) divergence. Alternatively, a convex optimization approach relaxes the binary constraint and applies (ADMM) to compute a solution. The convergence of both algorithms is proven. To improve computational efficiency, the two algorithms are cascaded and augmented with a decomposition technique to form a hybrid algorithm. The proposed framework is validated experimentally with a prototype eddy current sensing probe, demonstrating the ability to image defects as small as 1 mm at various depths using a sensor array with 4 mm spacing.

tags:

featured: false

# links:
# - name: ""
#   url: ""
url_pdf: 'https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=11007757'
url_code: ''
url_dataset: ''
url_poster: ''
url_project: ''
url_slides: ''
url_source: ''
url_video: ''
---
