<!-- 从 torch-topk.html 迁移的资料快照；原始 HTML SHA-256: 122dac0dd83db1b0e0dea637803e707bdd44320f7ae98a9e3cb412f452533bbd。 -->

- [](../index.html)
- [Reference API](../pytorch-api.html)
- [torch](../torch.html)
- torch.topk

Rate this Page

★ ★ ★ ★ ★

<a id="torch-topk"></a>

# torch.topk
torch.topk(*input*, *k*, *dim=None*, *largest=True*, *sorted=True*, *\**, *out=None*)[\#](#torch.topk "Link to this definition")  
Returns the `k` largest elements of the given `input` tensor along a given dimension.

If `dim` is not given, the last dimension of the input is chosen.

If `largest` is `False` then the k smallest elements are returned.

A namedtuple of (values, indices) is returned with the values and indices of the largest k elements of each row of the input tensor in the given dimension dim.

The boolean option `sorted` if `True`, will make sure that the returned k elements are themselves sorted

Note

When using torch.topk, the indices of tied elements are not guaranteed to be stable and may vary across different invocations.

Parameters:  
- **input** ([*Tensor*](../tensors.html#torch.Tensor "torch.Tensor")) – the input tensor.

- **k** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – the k in “top-k”

- **dim** ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")*,* *optional*) – the dimension to sort along

- **largest** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")*,* *optional*) – controls whether to return largest or smallest elements

- **sorted** ([*bool*](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")*,* *optional*) – controls whether to return the elements in sorted order

Keyword Arguments:  
**out** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple "(in Python v3.14)")*,* *optional*) – the output tuple of (Tensor, LongTensor) that can be optionally given to be used as output buffers

Example:

    >>> x = torch.arange(1., 6.)
    >>> x
    tensor([ 1.,  2.,  3.,  4.,  5.])
    >>> torch.topk(x, 3)
    torch.return_types.topk(values=tensor([5., 4., 3.]), indices=tensor([4, 3, 2]))

Rate this Page

★ ★ ★ ★ ★

Send Feedback

[](torch.sort.html "previous page")

previous

torch.sort

[](torch.msort.html "next page")

next

torch.msort

Built with the [PyData Sphinx Theme](https://pydata-sphinx-theme.readthedocs.io/en/stable/index.html) 0.15.4.

[](torch.sort.html "previous page")

previous

torch.sort

[](torch.msort.html "next page")

next

torch.msort

On this page

- [`topk()`](#torch.topk)

[ Show Source](../_sources/generated/torch.topk.rst.txt)

PyTorch Libraries

- [ExecuTorch](https://docs.pytorch.org/executorch)
- [Helion](https://docs.pytorch.org/helion)
- [torchao](https://docs.pytorch.org/ao)
- [kineto](https://github.com/pytorch/kineto)
- [torchtitan](https://github.com/pytorch/torchtitan)
- [TorchRL](https://docs.pytorch.org/rl)
- [torchvision](https://docs.pytorch.org/vision)
- [torchaudio](https://docs.pytorch.org/audio)
- [tensordict](https://docs.pytorch.org/tensordict)
- [PyTorch on XLA Devices](https://docs.pytorch.org/xla)
