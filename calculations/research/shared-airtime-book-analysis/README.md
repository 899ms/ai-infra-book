# 完整负载的分层空口账

这里从实际结果提取分层账，不推进网络，不以静态服务和替代完整业务时刻。
单图与四个混合场景均已实际完成，273,438 条包／无线尝试通过有限逐轨迹审查，
见 `../shared-airtime-trace-review/`。完整比较见 `COMPARISON.md`，精确分数与绑定见
`comparison.json`；研究范围验收为 `acceptance.json`，公共接入仍待完成。

```sh
python3 calculations/research/shared-airtime-book-analysis/summarize.py \
  --manifest calculations/research/shared-airtime-book-inputs/runs/image-baseline-manifest.json \
  --output calculations/research/shared-airtime-book-analysis/image-baseline-ledger.json
```

脚本要求完整、成功的 OFDM 交换；遇到失败或观察中途截断会拒绝，不能将未来整段
当作已观测发射。manifest 必须显示实际运行完成，结果 SHA 必须吻合。此脚本只是
聚合报告，不代替独立交换公式、逐包因果和业务质量审查。

五例总比较可复跑：

```sh
python3 calculations/research/shared-airtime-book-analysis/compare.py
```

该命令要求五例生成和独立逐轨迹审查均已完成，逐一检查新旧输入、结果、摘要及
生成 manifest，确认只有声明的无线／调度／ACK 参数不同，再输出表格。

## 单图分层计算

同一原始负载含 30,000,000 B 上传、5,000,000 B 响应。25,000 B 业务块独立分片，
实际共有 30,800 个端到端 DATA 包及 30,800 个纯 QUIC ACK 包，无 MAC 重试。
参考条件是明确选择的 legacy OFDM 54 Mbps 数据／6 Mbps MAC ACK、单帧、无聚合、
无加密、零随机 backoff；它不是实际设备的测量。

| 层次 | 从实际包数推导 | 结果 |
| --- | --- | --- |
| IP/UDP/QUIC | 30,800 × (1,228 + 92) B | 40,656,000 B |
| 承载帧 PSDU | 30,800 × (1,264 + 128) B | 42,873,600 B |
| 本跳 MAC ACK PSDU | 61,600 × 14 B | 862,400 B |
| 所有 PSDU | 上两项相加 | 43,736,000 B |
| DATA 与 QUIC ACK 承载 PPDU 发射 | 30,800 × (208 + 40) µs | 7.6384 s |
| 本跳 MAC ACK PPDU 发射 | 61,600 × 44 µs | 2.7104 s |
| 纯 RF 发射 | 上两项相加 | 10.3488 s |
| 交换前接入间隔 | 61,600 × 34 µs | 2.0944 s |
| SIFS | 61,600 × 16 µs | 0.9856 s |
| 总预约服务 | RF 发射 + 接入间隔 + SIFS | 13.4288 s |

前导和符号填充进入 PPDU 时间，不能再造出相应“线上字节”。QUIC ACK 的承载帧
自身也需要一个 MAC ACK；因此 30,800 个 QUIC ACK 与 61,600 个 MAC ACK 是不同的账。

实际完整图片到达时间为 `7996940933/500000000 = 15.993881866 s`；原独立 WAN
基线是 `14.8839358 s`。两者差 `1.109946066 s`。WAN 和无线交换可流水重叠，
不能把 13.4288 s 直接加到原时刻。该差值仅针对同一声明负载和固定参考条件。
混合业务还需分别检查音频播放、缺音和截图动作有效性，不能沿用单图成功结论。
