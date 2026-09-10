# HyStart++ 独立审查：限定范围 PASS

最终 `calculate.py` SHA256 为 `4eb38d1b4e09a4d5922a89a6bbcb7127ed4cfbf4678afb94323aea6eb3cb139d`。实际运行独立 `check-independent.py`，18组源自RFC/预先手算的有效边界与9个非法输入通过，详见 `independent-check.json`。期望并非调用候选 helper 计算；round trace 独立构造，明确提供每次真实发送的 SND.NXT 和唯一 RTT 样本身份。

验证包括：8样本第8次门槛、4/10/16ms阈值夹限、SS与CSS的paced/nonpaced增量、触发CSS的ACK只按SS加一次、CSS中恰等baseline不返回SS、低RTT须足够当轮样本才返回SS、partial round计1及第5轮handoff、缺RTT不充数但真实CSS round仍计时、空flight重复ACK不制造轮次、ACK越过marker只结束一次以及loss/ECN只交付退出而不暗加beta减窗。

增量对象另核重复 RTT sample ID 失败后的状态与 now 均不变。作者自查并修正了旧版先增窗再验证样本的问题；本次验收使用修正版本。非法序号/确认量、bool、零RTT、CSS divisor小于2、未知字段、handoff后继续ACK增长、发送序号倒退均被拒绝。

来源与适用边界见 `SOURCE-REVIEW.md`，官方勘误查询已留存。仅证明有限纯状态回调合同；实际TCP RTT采样资格、ACK/SACK区间及去重、真实发送/网络、后续CUBIC或NewReno接管均属外部职责。paced标志不代表实现了pacer，本模块也不能单独给出30MB传输时间。未修改公共代码或运行公共全流水线。
