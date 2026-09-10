<!-- 从 149-lab-post.html 迁移的资料快照；原始 HTML SHA-256: 3d444ec6cc47592db3b92a93a11f1af19116ed102e4ee585525f4291f46c44cf。 -->

# Einsum Trees

Mar 2, 2025

The einsum summation convention, or simply *einsum*, is a popular formalism for tensor expressions. It is available in many scientific computing and machine learning libraries, including [NumPy](https://numpy.org/doc/stable/reference/generated/numpy.einsum.html), [PyTorch](https://pytorch.org/docs/stable/generated/torch.einsum.html), [TensorFlow](https://www.tensorflow.org/api_docs/python/tf/einsum) and [JAX](https://docs.jax.dev/en/latest/_autosummary/jax.numpy.einsum.html). The beauty of einsum is that it allows us to formulate the contraction of multiple high-dimensional tensors in a simple and concise way. While einsum is widely used in user-facing frontends, many backends quickly lower it to a set of binary tensor contractions that are individually optimized without considering the big picture. In recent work, we have introduced the concept of *einsum trees*, which act as a high-level intermediate representation (IR) when compiling einsum expressions. Einsum trees provide a global view of the problem of contracting multiple input tensors to obtain a single output tensor. In this post, we cover the basics of how the IR works and how thinking in terms of einsum trees simplifies the optimization of high-dimensional dense linear algebra.

## Contraction Trees

We get started by discussing simple contraction trees that have only few input tensors. One of the simplest examples is that of a matrix-matrix multiplication: Given the matrix $`A`$ and the matrix $`B`$, we may want to compute the matrix-matrix product $`C=AB`$. This formula already encodes quite some information on the operation: We obtain a value of the output matrix $`C`$ by computing the dot-product of a row of $`A`$ and a column of $`B`$. In index notation we could write: $`C_{ij} = \sum_k A_{ik} B_{kj}`$. Keeping only the multi-indices we can shorten the equation to `ik,kj->ij`. Here, we assume that an index appearing in one or more inputs but not the output tensor is summed over. In the matrix-matrix multiplication example, index `k` is summed over. Further, the arrow `->` separates the indices of the input tensors from those of the output tensor. We can also write the expression `ik,kj->ij` as a binary tree with the two leaf nodes `ik` and `kj`, and the root node `ij`:

``` highlight
ij
├─ kj
└─ ik
```

The notation is extended easily to more complex examples. For example, we could shorten the batched matrix-matrix multiplication $`C_{lij} = \sum_k A_{lik} B_{lkj}`$ to `lik,lkj->lij`, or also write it is as a tree:

``` highlight
lij
├─ lkj
└─ lik
```

Even more interesting are cases, where more than two input tensors have to be contracted. For example, we might want to compute $`E=(AB)C`$ with input matrices $`A`$, $`B`$ and $`C`$. We can write the expression in index notation in two steps. First, an intermediate matrix $`D`$ is computed which is then multiplied with $`C`$ to obtain the output matrix $`E`$:

``` math
D_{ij} = \sum_k A_{ik} B_{kj} \\
  E_{il} = \sum_{j} D_{ij} C_{jl}
```

Once again, we can shorten the example by writing `[ik,kj->ij],jl->il` or as a tree where the three input matrices are leaf nodes:

``` highlight
il
├─ jl
└─ ij
   ├─ kj
   └─ ik
```

## Intermediate Representation

The intermediate representation Einsum Tree IR relies on a few additional properties. First, it assumes that all tensors are stored in general row-major format. This means that rightmost dimension in the multi-index of a tensor has unit stride and that the tensor has a contiguous memory format. For example, in the case of the rank-3 tensor $`A_{lik}`$ or short `lik`, the dimensions may have sizes $`|l|=2`$, $`|i|=3`$ and $`|k|=4`$. Now, the assumed general row-major format means that index `k` has unit stride, index `i` has stride 4, and index `l` has stride $`3 \cdot 4 = 12`$.

Second, the concept of a row-major memory layout implies that we can arrange the data of a tensor in different ways. For the `lik` example, we could alternatively store the data as `lki`, `ilk`, `ikl`, `kil`, or as `kli`. The IR supports changing the memory layout of the tensors through permutation nodes. Assuming that we would like to store the data of tensor `lik` as `ikl`, we simply write `lik->ikl`.

Consequently, an IR tree can now be transformed by inserting permutation nodes. For a batched matrix-matrix multiplication example, we could, for example, permute one of the input tensors before computing the contraction: `[lik->ikl],lkj->lij`. Written as a tree, we obtain:

``` highlight
lij
├─ lkj
└─ ikl
   └─ lik
```

## Lowering

We now discuss our approach to lowering binary tensor contractions, i.e. bringing the contractions into a form that can be executed in hardware.

A simple approach to lowering is nested loops, where the innermost loop performs scalar operations. Using the expression `trus,pqtu->pqrs` as an example, we could write code similar to the following:

``` highlight
for p in |p|
  for q in |q|
    for r in |q|
      for s in |s|
        for t in |t|
          for u in |u|
            out[p][q][r][s] += in0[t][r][u][s] * in1[p][q][t][u]
```

If translated directly into machine code, this code will have poor performance due to missing optimizations for parallelization and data reuse. Instead, we could follow standard optimization steps and perform sophisticated transformations to obtain fast code. Example steps include loop reordering, loop tiling, loop fusion, loop unrolling, packing, and unpacking.

All of this sounds difficult to achieve in software. We still lack the simplicity promised by thinking in terms of einsum trees. This is because *our approach to lowering einsum trees is primitive-based, i.e. we lower to primitives instead of scalar operations*. In particular, for the `trus,pqtu->pqrs` example, we can loop over matrix-matrix multiplications:

``` highlight
for r in |r|
  for t in |t|
    GEMM( A   = in0[t][r],
          B   = in1[0][0][t],
          C   = out[0][0][r],
          m   = |s|,
          n   = |p|*|q|,
          k   = |u|,
          ldA = |s|,
          ldB = |t| * |u|,
          ldC = |r| * |s| )
```

In the pseudocode, the naming of the `GEMM` parameters follows the convention of the [BLAS GEMM routines](https://www.netlib.org/blas/). We see that many of the low-level optimizations, such as register blocking or vectorization, can now be done by the primitive-providing library.

Of course, there will be many cases where our primitive-based mapping to GEMMs fails when working with arbitrary tensor contractions. This means that we need a simple way to identify GEMMs in tensor contractions, so that we can guide our tree-level optimization accordingly. Here, thinking in terms of einsum becomes incredibly helpful. We need to identify three blocks in the einsum string. One block corresponding to `m` in the `GEMM` call, one corresponding to `n`, and one corresponding to `k`. This boils down to finding the following pattern in the einsum expression:

``` highlight
[...]K[...]M,[...]N[...]K->[...]N[...]M
```

In the example, we have `M=s`, `N=pq` and `K=u`, i.e. we can rewrite the contraction as `trKM,NtM->NrM`. This allows us to clearly see where the GEMM operates in the tensors.

## Optimization

So far, we have introduced Einsum Tree IR and derived a straightforward way to lower contraction nodes in the IR to loops over primitives. The question now is whether and how we can modify IR trees to make our primitive-based lowering work. Spoiler alert: it is possible, and can be done using a remarkably simple heuristic. We will write a tutorial on this later, but for now we refer interested readers to our ASPLOS 2025 presentation in the ML compilers session: [Einsum Trees: An Abstraction for Optimizing the Execution of Tensor Expressions](https://www.asplos-conference.org/asplos2025/preliminary-program/).

We also invite you to try thinking in einsum trees and to check out the [Einsum Tree Visualizer](https://scalable.uni-jena.de/opt/einsum-vis/) developed by undergraduate student Thorsten Kröhl. To get you started, [here](https://scalable.uni-jena.de/opt/einsum-vis/?e=H4sIAAAAAAAAA1OKLtEp0inVKY7ViS7QKdQp0SmN1bUDM4uAgkoAPq41fCAAAAA%3D&s=H4sIAAAAAAAAA6tWKlCyMjTTUSqEUEUQqhhClUCoUhBVCwCdh1BLKwAAAA%3D%3D) is the `trus,pqtu->pqrs` example. And for a more complex tree, you can see the [initial version](https://scalable.uni-jena.de/opt/einsum-vis/?e=H4sIAAAAAAAAAzWLwQ3AIAwDd%2BHtSoGQEj5dxMr%2Ba%2BA%2B%2BN2d5UYmDBuzwIHEi13PR8PAlGSpky7tMHFH3N2FKo51Swh%2FXnqG%2FlntAMkOoOZhAAAA&s=H4sIAAAAAAAAAx3KsQ3AMAzEwF1Yq4hlWXZ%2BtSC755GGwAF8uFBWMFCdINHIYKLVQaFpLdReGvnYrnF%2B3Gjn%2BwFxOdvwRQAAAA%3D%3D) and a corresponding [optimized one](https://scalable.uni-jena.de/opt/einsum-vis/?e=H4sIAAAAAAAAAz2Myw3AIAxDd%2BHsSoGU36WLWNl%2FDRKoONl%2BL0oiOSCYeO35uAuGGciCgYYZuKG4cPx3uUek%2Bs6QUOrF5RYZNVBFtpN6laIH6lA7WY%2FavfmK52kBLyWi1poAAAA%3D&s=H4sIAAAAAAAAAx3KsQ3AMAzEwF1Yq4hlWXZ%2BtSC755GGwAF8uFBWMFCdINHIYKLVQaFpLdReGvnYrnF%2B3Gjn%2BwFxOdvwRQAAAA%3D%3D) by opening the links.

[](/research/2025/03/02/einsum-trees.html)
