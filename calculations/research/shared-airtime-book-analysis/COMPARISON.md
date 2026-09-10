# 完整共享空口对照

Fixed legacy OFDM reference, no MAC failures; not measured Wi-Fi, TCP/TACK or complete C69 acceptance.

| 场景 | 完整图片 s | 无线预约服务 s | WAN IP B | 已播块 | 缺音 s | 截图可用 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| image-baseline | 15.993881866 | 13.428800 | 40656000 | — | — | — |
| mixed-fifo-immediate | 15.993881866 | 13.434468 | 40673160 | 0 | 0.16 | False |
| mixed-fifo-aggregate | 15.669243112 | 11.109970 | 39077236 | 0 | 0.16 | False |
| mixed-priority-immediate | 15.920135004 | 13.437956 | 40683720 | 8 | 0.00 | False |
| mixed-priority-aggregate | 15.585252555 | 11.112922 | 39087428 | 8 | 0.00 | False |

精确分数、各自无无线基线、输入配对与逐轨迹审查身份见 comparison.json。
WAN和无线可以流水重叠，累计无线服务不能直接加到基线完成时刻；业务完成后可能仍有确认服务。
五例仅新增 wireless_access；四格之间只改变 source send scheduling 与 transport ACK policy。
队列排空不证明音频按时播放或截图动作有效。结果不外推为生产无线吞吐或等质量编解码性能。
