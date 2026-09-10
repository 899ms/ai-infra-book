<!-- 从 linear-transformers.html 迁移的资料快照；原始 HTML SHA-256: d58a917e4d89f55570de40ade1d2d3748ebe0ee3ed9ff98c8352cbbea508cee7。 -->

# Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention

[Angelos Katharopoulos^(1,2)](https://angeloskath.github.io/) [Apoorv Vyas^(1,2)](https://apoorv2904.github.io/) [Nikolaos Pappas³](https://nik0spapp.github.io/) [François Fleuret^(1,2)](https://fleuret.org/francois)

¹ Idiap Research Institute ² École Polytechnique Fédérale de Lausanne ³ University of Washington

ICML 2020

[  
Paper](https://arxiv.org/pdf/2006.16236.pdf) [![](imgs/colab_logo.png)  
Colab](https://colab.research.google.com/drive/1BV4OaWRAHYGeimO0cqHD86GfnfgUaKD4?usp=sharing) [  
Code](https://github.com/idiap/fast-transformers) [  
Docs](https://fast-transformers.github.io) [  
Video](https://youtu.be/KBWh7XCUAi8) [  
Slides](http://idiap.ch/~katharas/pdfs/linear-transformers-slides.pdf)

Transformers achieve remarkable performance in several tasks but due to their quadratic complexity, with respect to the input's length, they are prohibitively slow for very long sequences. To address this limitation, we express the self-attention as a linear dot-product of kernel feature maps and make use of the associativity property of matrix products to reduce the complexity from \$\bigO{N^2}\$ to \$\bigO{N}\$, where \$N\$ is the sequence length. We show that this formulation permits an iterative implementation that dramatically accelerates autoregressive transformers and reveals their relationship to recurrent neural networks. Our *linear transformers* achieve similar performance to vanilla transformers and they are up to 4000x faster on autoregressive prediction of very long sequences.

Video presentation

Interactive Demo

In our paper, we show that replacing the softmax attention with a linear dot product of kernel feature maps \$\fe{Q}\$ and \$\fe{K}\$ allows us to express any transformer as a recurrent neural network with the following update equations, where \$x_i\$ denotes the \$i\$-th input, \$y_i\$ the \$i\$-th output and \$s_i\$, \$z_i\$ the hidden state at timestep \$i\$ (see section 3 of the paper for a detailed description): \$\$ \begin{aligned} s_0 &= 0, \\ z_0 &= 0, \\ s_i &= s\_{i-1} + \fe{x_i W_K} \left(x_i W_V\right)^T, \\ z_i &= z\_{i-1} + \fe{x_i W_K}, \\ y_i &= f_l\left(\frac{\fe{x_i W_Q}^T s_i}{\fe{x_i W_Q}^T z_i} + x_i\right). \end{aligned} \$\$

The above formulation allows for efficient autoregressive inference with linear time complexity and constant memory. To showcase the efficiency of our model we load in the browser a transformer trained for autoregressive image generation and perform unconditional image generation with JavaScript in the browser. The loaded transformer has 8 layers and 8 heads per layer.

The following demo does not compare with any baselines; if you want to compare our formulation with the standard transformer [try our colab](https://colab.research.google.com/drive/1BV4OaWRAHYGeimO0cqHD86GfnfgUaKD4?usp=sharing). However, this demo runs on your device and not on any server, you could even try it on your phone.

Unconditional Samples Generator

Load the transformer

Batch size:

Go!

Concurrent Work

If you are interested in our work, you might also be interested in highly related concurrent work:

- [Efficient Attention: Attention with Linear Complexities](https://arxiv.org/abs/1812.01243)
- [Linformer: Self-Attention with Linear Complexity](https://arxiv.org/abs/2006.04768)
- [Masked Language Modeling for Proteins via Linearly Scalable Long-Context Transformers](https://arxiv.org/abs/2006.03555)

Acknowledgements

![SNSF logo](imgs/SNF_RGB_F_POS.png) Angelos Katharopoulos and Apoorv Vyas are supported by [SNSF](http://www.snf.ch/) for their research.
