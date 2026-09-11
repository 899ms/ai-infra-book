# 真实 C4 拟合的条件生命周期代理

目标 loss 2.9；输入 512 token，返回 128 token，额外 decode 127 步。训练、prefill、decode 均按 H100 SXM 80GB GPU 秒计价：每 FLOP 2.52678391e-15 GPU 秒，即 1/(989.4 TFLOP/s BF16 dense 峰值 × MFU 0.4)，费用列单位均为 GPU 秒，setup=0。

费用直线为 T(C)=6ND·r+C·2N[P+(G−1)]·r。它是声明的运算量代理，不是完整硬件费用、吞吐实测或等任务质量证明。

## primary

拟合 E=1.211242171, A=1.251253855, B=0.5234301354, α=0.1, β=0.45。

| N | 可行 | 目标 D | 训练代理 FLOPs | 每调用代理费用 | 超出 N/D 拟合框 |
|---:|---|---:|---:|---:|---|
| 1e+08 | True | 2.98578849e+11 | 1.79147309e+20 | 0.000322922984 | True (N×1, D×3.281) |
| 5e+08 | True | 2.48195922e+10 | 7.44587766e+19 | 0.00161461492 | False (N×1, D×1) |
| 1e+09 | True | 1.48956472e+10 | 8.93738833e+19 | 0.00322922984 | False (N×1, D×1) |
| 2.81e+09 | True | 8.59527407e+09 | 1.44916321e+20 | 0.00907413584 | True (N×2.563, D×1) |

| 两个 N | 交叉调用数 | 状态 | 代回相对误差 |
|---|---:|---|---:|
| 1e+08 / 5e+08 | 204789774.70332462 | nonnegative_crossing | 0.0 |
| 1e+08 / 1e+09 | 78050274.80566831 | nonnegative_crossing | 1.218062811055391e-16 |
| 1e+08 / 2.81e+09 | 9883694.131780142 | nonnegative_crossing | 0.0 |
| 5e+08 / 1e+09 | none | negative_crossing | not applicable |
| 5e+08 / 2.81e+09 | none | negative_crossing | not applicable |
| 1e+09 / 2.81e+09 | none | negative_crossing | not applicable |

| 调用数 | N | 总代理费用 | 该有限候选集合最小 N |
|---:|---:|---:|---:|
| 0 | 1e+08 | 452666.539 | 5e+08 |
| 0 | 5e+08 | 188141.239 | 5e+08 |
| 0 | 1e+09 | 225828.49 | 5e+08 |
| 0 | 2.81e+09 | 366172.228 | 5e+08 |
| 1000 | 1e+08 | 452666.862 | 5e+08 |
| 1000 | 5e+08 | 188142.853 | 5e+08 |
| 1000 | 1e+09 | 225831.72 | 5e+08 |
| 1000 | 2.81e+09 | 366181.302 | 5e+08 |
| 1000000 | 1e+08 | 452989.462 | 5e+08 |
| 1000000 | 5e+08 | 189755.854 | 5e+08 |
| 1000000 | 1e+09 | 229057.72 | 5e+08 |
| 1000000 | 2.81e+09 | 375246.364 | 5e+08 |
| 1000000000 | 1e+08 | 775589.522 | 1e+08 |
| 1000000000 | 5e+08 | 1802756.16 | 1e+08 |
| 1000000000 | 1e+09 | 3455058.33 | 1e+08 |
| 1000000000 | 2.81e+09 | 9440308.07 | 1e+08 |

## shape_N

拟合 E=1.210379631, A=1.252068734, B=0.5234384176, α=0.1, β=0.45。

| N | 可行 | 目标 D | 训练代理 FLOPs | 每调用代理费用 | 超出 N/D 拟合框 |
|---:|---|---:|---:|---:|---|
| 1e+08 | True | 2.99546229e+11 | 1.79727738e+20 | 0.000322922984 | True (N×1, D×3.292) |
| 5e+08 | True | 2.48221823e+10 | 7.4466547e+19 | 0.00161461492 | False (N×1, D×1) |
| 1e+09 | True | 1.48925655e+10 | 8.9355393e+19 | 0.00322922984 | False (N×1, D×1) |
| 2.81e+09 | True | 8.59122639e+09 | 1.44848077e+20 | 0.00907413584 | True (N×2.563, D×1) |

| 两个 N | 交叉调用数 | 状态 | 代回相对误差 |
|---|---:|---|---:|
| 1e+08 / 5e+08 | 205909997.21703526 | nonnegative_crossing | 0.0 |
| 1e+08 / 1e+09 | 78570983.01130307 | nonnegative_crossing | 0.0 |
| 1e+08 / 2.81e+09 | 10070988.642015502 | nonnegative_crossing | 0.0 |
| 5e+08 / 1e+09 | none | negative_crossing | not applicable |
| 5e+08 / 2.81e+09 | none | negative_crossing | not applicable |
| 1e+09 / 2.81e+09 | none | negative_crossing | not applicable |

| 调用数 | N | 总代理费用 | 该有限候选集合最小 N |
|---:|---:|---:|---:|
| 0 | 1e+08 | 454133.155 | 5e+08 |
| 0 | 5e+08 | 188160.873 | 5e+08 |
| 0 | 1e+09 | 225781.769 | 5e+08 |
| 0 | 2.81e+09 | 365999.79 | 5e+08 |
| 1000 | 1e+08 | 454133.478 | 5e+08 |
| 1000 | 5e+08 | 188162.487 | 5e+08 |
| 1000 | 1e+09 | 225784.998 | 5e+08 |
| 1000 | 2.81e+09 | 366008.864 | 5e+08 |
| 1000000 | 1e+08 | 454456.078 | 5e+08 |
| 1000000 | 5e+08 | 189775.488 | 5e+08 |
| 1000000 | 1e+09 | 229010.999 | 5e+08 |
| 1000000 | 2.81e+09 | 375073.926 | 5e+08 |
| 1000000000 | 1e+08 | 777056.139 | 1e+08 |
| 1000000000 | 5e+08 | 1802775.79 | 1e+08 |
| 1000000000 | 1e+09 | 3455011.61 | 1e+08 |
| 1000000000 | 2.81e+09 | 9440135.63 | 1e+08 |

## declared_D

拟合 E=1.214236397, A=1.252140054, B=0.5230029997, α=0.1, β=0.45。

| N | 可行 | 目标 D | 训练代理 FLOPs | 每调用代理费用 | 超出 N/D 拟合框 |
|---:|---|---:|---:|---:|---|
| 1e+08 | True | 3.23488636e+11 | 1.94093182e+20 | 0.000322922984 | True (N×1, D×3.556) |
| 5e+08 | True | 2.54107059e+10 | 7.62321178e+19 | 0.00161461492 | False (N×1, D×1) |
| 1e+09 | True | 1.51659493e+10 | 9.09956958e+19 | 0.00322922984 | False (N×1, D×1) |
| 2.81e+09 | True | 8.71019395e+09 | 1.4685387e+20 | 0.00907413584 | True (N×2.563, D×1) |

| 两个 N | 交叉调用数 | 状态 | 代回相对误差 |
|---|---:|---|---:|
| 1e+08 / 5e+08 | 230557636.91898242 | nonnegative_crossing | 0.0 |
| 1e+08 / 1e+09 | 89634399.22293429 | nonnegative_crossing | 0.0 |
| 1e+08 / 2.81e+09 | 13639656.005115306 | nonnegative_crossing | 0.0 |
| 5e+08 / 1e+09 | none | negative_crossing | not applicable |
| 5e+08 / 2.81e+09 | none | negative_crossing | not applicable |
| 1e+09 / 2.81e+09 | none | negative_crossing | not applicable |

| 调用数 | N | 总代理费用 | 该有限候选集合最小 N |
|---:|---:|---:|---:|
| 0 | 1e+08 | 490431.529 | 5e+08 |
| 0 | 5e+08 | 192622.089 | 5e+08 |
| 0 | 1e+09 | 229926.46 | 5e+08 |
| 0 | 2.81e+09 | 371067.996 | 5e+08 |
| 1000 | 1e+08 | 490431.852 | 5e+08 |
| 1000 | 5e+08 | 192623.703 | 5e+08 |
| 1000 | 1e+09 | 229929.689 | 5e+08 |
| 1000 | 2.81e+09 | 371077.07 | 5e+08 |
| 1000000 | 1e+08 | 490754.452 | 5e+08 |
| 1000000 | 5e+08 | 194236.704 | 5e+08 |
| 1000000 | 1e+09 | 233155.69 | 5e+08 |
| 1000000 | 2.81e+09 | 380142.132 | 5e+08 |
| 1000000000 | 1e+08 | 813354.512 | 1e+08 |
| 1000000000 | 5e+08 | 1807237.01 | 1e+08 |
| 1000000000 | 1e+09 | 3459156.3 | 1e+08 |
| 1000000000 | 2.81e+09 | 9445203.84 | 1e+08 |

## both

拟合 E=1.213370805, A=1.252957991, B=0.5230112116, α=0.1, β=0.45。

| N | 可行 | 目标 D | 训练代理 FLOPs | 每调用代理费用 | 超出 N/D 拟合框 |
|---:|---|---:|---:|---:|---|
| 1e+08 | True | 3.24580938e+11 | 1.94748563e+20 | 0.000322922984 | True (N×1, D×3.568) |
| 5e+08 | True | 2.54134081e+10 | 7.62402243e+19 | 0.00161461492 | False (N×1, D×1) |
| 1e+09 | True | 1.51627752e+10 | 9.09766509e+19 | 0.00322922984 | False (N×1, D×1) |
| 2.81e+09 | True | 8.70604953e+09 | 1.46783995e+20 | 0.00907413584 | True (N×2.563, D×1) |

| 两个 N | 交叉调用数 | 状态 | 代回相对误差 |
|---|---:|---|---:|
| 1e+08 / 5e+08 | 231823823.35884187 | nonnegative_crossing | 0.0 |
| 1e+08 / 1e+09 | 90220754.51966234 | nonnegative_crossing | 0.0 |
| 1e+08 / 2.81e+09 | 13849062.965877399 | nonnegative_crossing | 0.0 |
| 5e+08 / 1e+09 | none | negative_crossing | not applicable |
| 5e+08 / 2.81e+09 | none | negative_crossing | not applicable |
| 1e+09 / 2.81e+09 | none | negative_crossing | not applicable |

| 调用数 | N | 总代理费用 | 该有限候选集合最小 N |
|---:|---:|---:|---:|
| 0 | 1e+08 | 492087.535 | 5e+08 |
| 0 | 5e+08 | 192642.572 | 5e+08 |
| 0 | 1e+09 | 229878.338 | 5e+08 |
| 0 | 2.81e+09 | 370891.437 | 5e+08 |
| 1000 | 1e+08 | 492087.858 | 5e+08 |
| 1000 | 5e+08 | 192644.187 | 5e+08 |
| 1000 | 1e+09 | 229881.567 | 5e+08 |
| 1000 | 2.81e+09 | 370900.511 | 5e+08 |
| 1000000 | 1e+08 | 492410.458 | 5e+08 |
| 1000000 | 5e+08 | 194257.187 | 5e+08 |
| 1000000 | 1e+09 | 233107.568 | 5e+08 |
| 1000000 | 2.81e+09 | 379965.573 | 5e+08 |
| 1000000000 | 1e+08 | 815010.518 | 1e+08 |
| 1000000000 | 5e+08 | 1807257.49 | 1e+08 |
| 1000000000 | 1e+09 | 3459108.17 | 1e+08 |
| 1000000000 | 2.81e+09 | 9445027.28 | 1e+08 |

## wider_grid

拟合 E=1.211242171, A=1.251253855, B=0.5234301354, α=0.1, β=0.45。

| N | 可行 | 目标 D | 训练代理 FLOPs | 每调用代理费用 | 超出 N/D 拟合框 |
|---:|---|---:|---:|---:|---|
| 1e+08 | True | 2.98578849e+11 | 1.79147309e+20 | 0.000322922984 | True (N×1, D×3.281) |
| 5e+08 | True | 2.48195922e+10 | 7.44587766e+19 | 0.00161461492 | False (N×1, D×1) |
| 1e+09 | True | 1.48956472e+10 | 8.93738833e+19 | 0.00322922984 | False (N×1, D×1) |
| 2.81e+09 | True | 8.59527407e+09 | 1.44916321e+20 | 0.00907413584 | True (N×2.563, D×1) |

| 两个 N | 交叉调用数 | 状态 | 代回相对误差 |
|---|---:|---|---:|
| 1e+08 / 5e+08 | 204789774.70332462 | nonnegative_crossing | 0.0 |
| 1e+08 / 1e+09 | 78050274.80566831 | nonnegative_crossing | 1.218062811055391e-16 |
| 1e+08 / 2.81e+09 | 9883694.131780142 | nonnegative_crossing | 0.0 |
| 5e+08 / 1e+09 | none | negative_crossing | not applicable |
| 5e+08 / 2.81e+09 | none | negative_crossing | not applicable |
| 1e+09 / 2.81e+09 | none | negative_crossing | not applicable |

| 调用数 | N | 总代理费用 | 该有限候选集合最小 N |
|---:|---:|---:|---:|
| 0 | 1e+08 | 452666.539 | 5e+08 |
| 0 | 5e+08 | 188141.239 | 5e+08 |
| 0 | 1e+09 | 225828.49 | 5e+08 |
| 0 | 2.81e+09 | 366172.228 | 5e+08 |
| 1000 | 1e+08 | 452666.862 | 5e+08 |
| 1000 | 5e+08 | 188142.853 | 5e+08 |
| 1000 | 1e+09 | 225831.72 | 5e+08 |
| 1000 | 2.81e+09 | 366181.302 | 5e+08 |
| 1000000 | 1e+08 | 452989.462 | 5e+08 |
| 1000000 | 5e+08 | 189755.854 | 5e+08 |
| 1000000 | 1e+09 | 229057.72 | 5e+08 |
| 1000000 | 2.81e+09 | 375246.364 | 5e+08 |
| 1000000000 | 1e+08 | 775589.522 | 1e+08 |
| 1000000000 | 5e+08 | 1802756.16 | 1e+08 |
| 1000000000 | 1e+09 | 3455058.33 | 1e+08 |
| 1000000000 | 2.81e+09 | 9440308.07 | 1e+08 |

## 范围与来源

- The fitted real C4 loss is a proxy target, not demonstrated equal task quality or a trained candidate architecture.
- All costs are H100 SXM 80GB GPU-seconds: 2.52678391e-15 GPU-s per proxy FLOP = 1/(989.4 TFLOP/s BF16 dense peak x MFU 0.4); the same MFU is applied to training and serving, and MFU is a declared input rather than measured here.
- Training is 6ND. Input work is 2NP; additional decode is 2N(G-1), because the first output comes from the input phase. Attention, KV, sampling, actual heads and communication are not modeled.
- Every candidate reports its N/D fit-box extrapolation. Formula feasibility does not establish a realizable data budget or reliable prediction.
- Primary and four prespecified sensitivities are shown separately; held-out error does not select a cheaper law.
- Setup is explicitly zero for this scenario; changing assumptions requires rerunning inputs. No deployment recommendation or universal optimum follows.

训练点与来源随公共 real_scaling_fit.calculate() 实时校验和复算；下列 SHA 绑定所用数据原件。

| 文件 | SHA256 |
|---|---|
| sources/scaling-real-points/README.md | 122f89e4e3987acf6191db35631795e567f9a79815ea98f0557709e816471b7b |
| sources/scaling-real-points/hub/lm1-2b8-55b-c4-repetitions/2b855b55bc4/3431998.out | 0d25cd8e1a124d1ccb5cd1cc0965707645161c57bcea67a90d101d60e2dd8bce |
| sources/scaling-real-points/hub/lm1-8b7-178b-c4-repetitions/8b7178b178b/3430821.out | e87423b94776d752571a5ca59183110e5c2e0a43d6f9a28e533403b7fb05be69 |
| sources/scaling-real-points/hub/lm1-misc/14m100m100m/logs/3163413.out | f48ea24d544feb59e27ee9eb23ef43d7617c4673cb6f4f7fe13cf3ab48ec7e50 |
| sources/scaling-real-points/hub/lm1-misc/14m100m100m/sbatch_14m100m100m.sh | b5d8ae2e78e17de7e3470ab60149766346e32abf6eee2fcb0884861238cbaa2c |
| sources/scaling-real-points/hub/lm1-misc/196m1b51b5/logs/3163481.out | e779a9e84551753deb738842cd90ffd6876ffbb73fbf0f2e21f5bfe7b15f0d46 |
| sources/scaling-real-points/hub/lm1-misc/196m1b51b5/sbatch_196m1b51b5.sh | 23325c1e51fe35e70c017514c5ea25a928288f0f06d5078686b0e4c0e26556d3 |
| sources/scaling-real-points/hub/lm1-misc/1b1100m100m/3324218.out | 63ed0dda91136068abdffe287579cde4be96f5293b8c119b1937f0e641ca409f |
| sources/scaling-real-points/hub/lm1-misc/1b1100m100m/sbatch_1b1100m100m.sh | a9c30c85bd4f1fb51afd04bc8e23839b58f38850d749ddae806c53eb87f358af |
| sources/scaling-real-points/hub/lm1-misc/1b112b12b/2820797.out | 729ed7c037d714775c03a90e91cb6876738810b8cbe7a7d344d86f881601d1df |
| sources/scaling-real-points/hub/lm1-misc/1b112b12b/sbatch_1b112b12b.sh | 656ac35c5429ced88899098933aa994654d898a8ca82bda69b9361848fbf29fa |
| sources/scaling-real-points/hub/lm1-misc/1b11b51b5/logs/2809896.out | 02eb3e6900d7771d3ba74e1d521f7599163e484ea3793c40c57f5c2ccc43c59c |
| sources/scaling-real-points/hub/lm1-misc/1b11b51b5/sbatch_1b11b51b5.sh | 73d3eb3edeb0c1210c2dd85b93899ac0f5271eca0ec37a27d1471a960b85cb8d |
| sources/scaling-real-points/hub/lm1-misc/1b191b91b/logs/2833162.out | 1d72b2653f06c40ea18f44d6a22c5c125c75ad659f151daebd9478672ff876db |
| sources/scaling-real-points/hub/lm1-misc/1b191b91b/sbatch_1b191b91b.sh | d0513f76c3c18c72b821a7e71efe6ce8de8d1ba98f76e19ed279487b7a41a32a |
| sources/scaling-real-points/utils/parametric_fit.ipynb | 6c65d270e70c944a9ac90f5f1213a4584e1ff9d6d2781cd86900663f4ab17db9 |
| sources/scaling-real-points/independent/supplement.pdf | 86e21e48a1f9eb6aa09d8bf07c8ffe99e947ae06adf0fc050a6bbd44e026db0f |
| sources/scaling-real-points/independent/supplement.txt | 7407f4d52df1d445a7d1705154107b3f6c7f2f0044730d31deb5dad490ae2dc7 |
| sources/scaling-real-points/independent/STATISTICAL-C4-REVIEW.md | 4e5de5804332791c1443646ca88b08b56b048bde5ccb3ccd8d8ca063f7580054 |
| sources/scaling-real-points/independent/statistical-C4-eight-point-evidence.json | 397623fc5e8b2a77ee602acb561543be19967bfb4b1a810ee770d109b5ac5df2 |
| sources/scaling-real-points/independent/n-loss-sources.lock.json | e5cd8aa964f262b11e96c2d3eb0021c4fdce5ae7fb63d747bdb078fb8bbd7889 |
| configs/scaling-real-points/data.json | fb134f0ee5f54ae2812e64d28878f7f0a9865e9a554c0fe559219e4f1ea9b77f |
