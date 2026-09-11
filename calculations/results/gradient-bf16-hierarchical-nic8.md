# 真实梯度的两级集合通信

参数：`model.layers.0.mlp.gate_proj.weight`；形状 [12288, 4096]；每rank 100,663,296 bytes；参与者 16。
组织：hierarchical；每服务器 8 rank、8 NIC（one NIC per rank）；NIC 50,000,000,000 bytes/s，本地 450,000,000,000 bytes/s，共享出口 None。

| 阶段 | 轮数 | 发送 bytes | 跨服务器发送 bytes | 串行屏障下界 seconds（精确） |
| --- | ---: | ---: | ---: | ---: |
| local_reduce_scatter | 7 | 1409286144 | 0 | 15117389/75000000000 |
| cross_server_allreduce | 2 | 201326592 | 201326592 | 3166553/12500000000 |
| local_all_gather | 7 | 1409286144 | 0 | 15117389/75000000000 |

全网发送 3,019,898,880 bytes；跨服务器 201,326,592 bytes（每方向 100,663,296）；标量归约加法 754,974,720 次；每服务器用到 8 张 NIC。
串行屏障下界 3077131/4687500000 seconds；预算未被此必要下界排除：True。实际训练期限是否可行仍未知。

| 物理资源 | bytes | 声明 bytes/s | 必要服务 seconds（精确） |
| --- | ---: | ---: | ---: |
| cut.0->1 | 100663296 | 400000000000 | 12288/48828125 |
| cut.1->0 | 100663296 | 400000000000 | 12288/48828125 |
| local.0->1 | 176160768 | 450000000000 | 57344/146484375 |
| local.1->2 | 176160768 | 450000000000 | 57344/146484375 |
| local.10->11 | 176160768 | 450000000000 | 57344/146484375 |
| local.11->12 | 176160768 | 450000000000 | 57344/146484375 |
| local.12->13 | 176160768 | 450000000000 | 57344/146484375 |
| local.13->14 | 176160768 | 450000000000 | 57344/146484375 |
| local.14->15 | 176160768 | 450000000000 | 57344/146484375 |
| local.15->8 | 176160768 | 450000000000 | 57344/146484375 |
| local.2->3 | 176160768 | 450000000000 | 57344/146484375 |
| local.3->4 | 176160768 | 450000000000 | 57344/146484375 |
| local.4->5 | 176160768 | 450000000000 | 57344/146484375 |
| local.5->6 | 176160768 | 450000000000 | 57344/146484375 |
| local.6->7 | 176160768 | 450000000000 | 57344/146484375 |
| local.7->0 | 176160768 | 450000000000 | 57344/146484375 |
| local.8->9 | 176160768 | 450000000000 | 57344/146484375 |
| local.9->10 | 176160768 | 450000000000 | 57344/146484375 |
| rank0.rx | 188743680 | 450000000000 | 4096/9765625 |
| rank0.tx | 188743680 | 450000000000 | 4096/9765625 |
| rank1.rx | 188743680 | 450000000000 | 4096/9765625 |
| rank1.tx | 188743680 | 450000000000 | 4096/9765625 |
| rank10.rx | 188743680 | 450000000000 | 4096/9765625 |
| rank10.tx | 188743680 | 450000000000 | 4096/9765625 |
| rank11.rx | 188743680 | 450000000000 | 4096/9765625 |
| rank11.tx | 188743680 | 450000000000 | 4096/9765625 |
| rank12.rx | 188743680 | 450000000000 | 4096/9765625 |
| rank12.tx | 188743680 | 450000000000 | 4096/9765625 |
| rank13.rx | 188743680 | 450000000000 | 4096/9765625 |
| rank13.tx | 188743680 | 450000000000 | 4096/9765625 |
| rank14.rx | 188743680 | 450000000000 | 4096/9765625 |
| rank14.tx | 188743680 | 450000000000 | 4096/9765625 |
| rank15.rx | 188743680 | 450000000000 | 4096/9765625 |
| rank15.tx | 188743680 | 450000000000 | 4096/9765625 |
| rank2.rx | 188743680 | 450000000000 | 4096/9765625 |
| rank2.tx | 188743680 | 450000000000 | 4096/9765625 |
| rank3.rx | 188743680 | 450000000000 | 4096/9765625 |
| rank3.tx | 188743680 | 450000000000 | 4096/9765625 |
| rank4.rx | 188743680 | 450000000000 | 4096/9765625 |
| rank4.tx | 188743680 | 450000000000 | 4096/9765625 |
| rank5.rx | 188743680 | 450000000000 | 4096/9765625 |
| rank5.tx | 188743680 | 450000000000 | 4096/9765625 |
| rank6.rx | 188743680 | 450000000000 | 4096/9765625 |
| rank6.tx | 188743680 | 450000000000 | 4096/9765625 |
| rank7.rx | 188743680 | 450000000000 | 4096/9765625 |
| rank7.tx | 188743680 | 450000000000 | 4096/9765625 |
| rank8.rx | 188743680 | 450000000000 | 4096/9765625 |
| rank8.tx | 188743680 | 450000000000 | 4096/9765625 |
| rank9.rx | 188743680 | 450000000000 | 4096/9765625 |
| rank9.tx | 188743680 | 450000000000 | 4096/9765625 |
| server0.nic0.rx | 12582912 | 50000000000 | 12288/48828125 |
| server0.nic0.tx | 12582912 | 50000000000 | 12288/48828125 |
| server0.nic1.rx | 12582912 | 50000000000 | 12288/48828125 |
| server0.nic1.tx | 12582912 | 50000000000 | 12288/48828125 |
| server0.nic2.rx | 12582912 | 50000000000 | 12288/48828125 |
| server0.nic2.tx | 12582912 | 50000000000 | 12288/48828125 |
| server0.nic3.rx | 12582912 | 50000000000 | 12288/48828125 |
| server0.nic3.tx | 12582912 | 50000000000 | 12288/48828125 |
| server0.nic4.rx | 12582912 | 50000000000 | 12288/48828125 |
| server0.nic4.tx | 12582912 | 50000000000 | 12288/48828125 |
| server0.nic5.rx | 12582912 | 50000000000 | 12288/48828125 |
| server0.nic5.tx | 12582912 | 50000000000 | 12288/48828125 |
| server0.nic6.rx | 12582912 | 50000000000 | 12288/48828125 |
| server0.nic6.tx | 12582912 | 50000000000 | 12288/48828125 |
| server0.nic7.rx | 12582912 | 50000000000 | 12288/48828125 |
| server0.nic7.tx | 12582912 | 50000000000 | 12288/48828125 |
| server1.nic0.rx | 12582912 | 50000000000 | 12288/48828125 |
| server1.nic0.tx | 12582912 | 50000000000 | 12288/48828125 |
| server1.nic1.rx | 12582912 | 50000000000 | 12288/48828125 |
| server1.nic1.tx | 12582912 | 50000000000 | 12288/48828125 |
| server1.nic2.rx | 12582912 | 50000000000 | 12288/48828125 |
| server1.nic2.tx | 12582912 | 50000000000 | 12288/48828125 |
| server1.nic3.rx | 12582912 | 50000000000 | 12288/48828125 |
| server1.nic3.tx | 12582912 | 50000000000 | 12288/48828125 |
| server1.nic4.rx | 12582912 | 50000000000 | 12288/48828125 |
| server1.nic4.tx | 12582912 | 50000000000 | 12288/48828125 |
| server1.nic5.rx | 12582912 | 50000000000 | 12288/48828125 |
| server1.nic5.tx | 12582912 | 50000000000 | 12288/48828125 |
| server1.nic6.rx | 12582912 | 50000000000 | 12288/48828125 |
| server1.nic6.tx | 12582912 | 50000000000 | 12288/48828125 |
| server1.nic7.rx | 12582912 | 50000000000 | 12288/48828125 |
| server1.nic7.tx | 12582912 | 50000000000 | 12288/48828125 |
| shared_cut.bidirectional | 201326592 | 800000000000 | 12288/48828125 |

- One real first-layer gate parameter gradient per rank; each rank contributes different sample data to the same coordinates. Not activations, whole-model gradients, or framework buckets.
- FP32/BF16 are declared gradient wire/operand widths. Rank contribution identities prove algebraic sum coverage, not floating-point reassociation equivalence or backend accumulation precision.
- Two servers each own 8 fixed ranks. Hierarchy executes local RS over 8 ranks, corresponding-owner two-rank AR, local AG with stage/round barriers; no overlapping stages or unmodeled algorithm substitutions.
- Every rank owns one NIC: a remote message leaves through the sender NIC and enters through the receiver NIC, never striped or relayed. The switch cut between the servers carries the aggregate NIC rate; no shared server egress is declared.
- All rates and startup are declared inputs. Each round bound is max(resource bytes/rate)+startup; serialized barrier bounds omit reduction work, propagation, buffering, topology latency and interference. They are not executable timing or deadline guarantees.
- Logical network sends count payload once. Endpoint receive, NIC, ingress and cut counters represent distinct resource demands; their sum is not additional gradient payload or HBM traffic.
- No padding is introduced. Missing paths/resources or invalid rates reject. Budget pass only means this communication lower bound has not excluded the candidate; real training feasibility remains unknown.

完整逐轮消息、NIC区间和贡献身份：

```json
{
  "calculation": "hierarchical-gradient",
  "scenario": {
    "model": "qwen3-8b",
    "gradient_dtype": "BF16",
    "algorithm": "hierarchical",
    "ranks_per_server": 8,
    "nics_per_server": 8,
    "nic_bytes_per_second": 50000000000,
    "local_bytes_per_second": 450000000000,
    "shared_egress_bytes_per_second": null,
    "nic_assignment": "one NIC per rank",
    "startup_ns": 833,
    "budget_ns": 3000000,
    "bandwidth_overrides": null
  },
  "sources": [
    {
      "file": "configs/models/qwen3-8b/config.json",
      "url": "https://huggingface.co/Qwen/Qwen3-8B/resolve/b968826d9c46dd6066d109eabc6255188de91218/config.json",
      "revision": "b968826d9c46dd6066d109eabc6255188de91218",
      "sha256": "f7c4eadfbbf522470667b797a3c89be2524832d2d599797248dc304fff447c30"
    },
    {
      "file": "sources/qwen3-8b/model.safetensors.index.json",
      "url": "https://huggingface.co/Qwen/Qwen3-8B/resolve/b968826d9c46dd6066d109eabc6255188de91218/model.safetensors.index.json",
      "revision": "b968826d9c46dd6066d109eabc6255188de91218",
      "sha256": "f9fdbcb91c23971c13ec5d5f2573d2349e8f61f2f049371ec699281748fdb1bc"
    },
    {
      "file": "sources/qwen3/modeling_qwen3.py",
      "url": "https://raw.githubusercontent.com/huggingface/transformers/0720e206c6ba28887e4d60ef60a6a089f6c1cc76/src/transformers/models/qwen3/modeling_qwen3.py",
      "revision": "0720e206c6ba28887e4d60ef60a6a089f6c1cc76",
      "sha256": "704c914530530a1acb0b443add1f520404e3ac2c28c0ab7e16f80f86cfe8ccb2"
    },
    {
      "file": "sources/qwen3/modeling_qwen3_moe.py",
      "url": "https://raw.githubusercontent.com/huggingface/transformers/0720e206c6ba28887e4d60ef60a6a089f6c1cc76/src/transformers/models/qwen3_moe/modeling_qwen3_moe.py",
      "revision": "0720e206c6ba28887e4d60ef60a6a089f6c1cc76",
      "sha256": "3af43d01f9f902c8009b6dd7d7b8b563561b53dd0aa54175f585ae90d049fdb8"
    }
  ],
  "gradient": {
    "parameter": "model.layers.0.mlp.gate_proj.weight",
    "template": "model.layers.{layer}.mlp.gate_proj.weight",
    "shape": [
      12288,
      4096
    ],
    "elements": 50331648,
    "bytes_per_element": 2,
    "bytes_per_rank": 100663296,
    "selected_parameter_copies": 1,
    "template_layer_copies": 36,
    "initial_contributors_per_rank": 1,
    "participants": 16,
    "chunks": 16,
    "chunk_elements": 3145728,
    "chunk_bytes": 6291456
  },
  "rank_mapping": [
    {
      "rank": 0,
      "server": 0,
      "card": 0,
      "nic": 0
    },
    {
      "rank": 1,
      "server": 0,
      "card": 1,
      "nic": 1
    },
    {
      "rank": 2,
      "server": 0,
      "card": 2,
      "nic": 2
    },
    {
      "rank": 3,
      "server": 0,
      "card": 3,
      "nic": 3
    },
    {
      "rank": 4,
      "server": 0,
      "card": 4,
      "nic": 4
    },
    {
      "rank": 5,
      "server": 0,
      "card": 5,
      "nic": 5
    },
    {
      "rank": 6,
      "server": 0,
      "card": 6,
      "nic": 6
    },
    {
      "rank": 7,
      "server": 0,
      "card": 7,
      "nic": 7
    },
    {
      "rank": 8,
      "server": 1,
      "card": 0,
      "nic": 0
    },
    {
      "rank": 9,
      "server": 1,
      "card": 1,
      "nic": 1
    },
    {
      "rank": 10,
      "server": 1,
      "card": 2,
      "nic": 2
    },
    {
      "rank": 11,
      "server": 1,
      "card": 3,
      "nic": 3
    },
    {
      "rank": 12,
      "server": 1,
      "card": 4,
      "nic": 4
    },
    {
      "rank": 13,
      "server": 1,
      "card": 5,
      "nic": 5
    },
    {
      "rank": 14,
      "server": 1,
      "card": 6,
      "nic": 6
    },
    {
      "rank": 15,
      "server": 1,
      "card": 7,
      "nic": 7
    }
  ],
  "flat_ring_order": null,
  "rounds": [
    {
      "round": 0,
      "stage": "local_reduce_scatter",
      "phase": "reduce_scatter",
      "step": 0,
      "messages": [
        {
          "sender": 0,
          "receiver": 1,
          "operation": "reduce",
          "chunks": [
            0,
            1
          ],
          "element_start": 0,
          "element_stop": 6291456,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 0,
              "contributors": [
                0
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                0
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r0:local",
              "receiver": "r1:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 0,
              "element_stop": 6291456,
              "path": [
                "rank0.tx",
                "local.0->1",
                "rank1.rx"
              ]
            }
          ]
        },
        {
          "sender": 1,
          "receiver": 2,
          "operation": "reduce",
          "chunks": [
            2,
            3
          ],
          "element_start": 6291456,
          "element_stop": 12582912,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 2,
              "contributors": [
                1
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                1
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r1:local",
              "receiver": "r2:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 6291456,
              "element_stop": 12582912,
              "path": [
                "rank1.tx",
                "local.1->2",
                "rank2.rx"
              ]
            }
          ]
        },
        {
          "sender": 2,
          "receiver": 3,
          "operation": "reduce",
          "chunks": [
            4,
            5
          ],
          "element_start": 12582912,
          "element_stop": 18874368,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 4,
              "contributors": [
                2
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                2
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r2:local",
              "receiver": "r3:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 12582912,
              "element_stop": 18874368,
              "path": [
                "rank2.tx",
                "local.2->3",
                "rank3.rx"
              ]
            }
          ]
        },
        {
          "sender": 3,
          "receiver": 4,
          "operation": "reduce",
          "chunks": [
            6,
            7
          ],
          "element_start": 18874368,
          "element_stop": 25165824,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 6,
              "contributors": [
                3
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                3
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r3:local",
              "receiver": "r4:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 18874368,
              "element_stop": 25165824,
              "path": [
                "rank3.tx",
                "local.3->4",
                "rank4.rx"
              ]
            }
          ]
        },
        {
          "sender": 4,
          "receiver": 5,
          "operation": "reduce",
          "chunks": [
            8,
            9
          ],
          "element_start": 25165824,
          "element_stop": 31457280,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 8,
              "contributors": [
                4
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                4
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r4:local",
              "receiver": "r5:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 25165824,
              "element_stop": 31457280,
              "path": [
                "rank4.tx",
                "local.4->5",
                "rank5.rx"
              ]
            }
          ]
        },
        {
          "sender": 5,
          "receiver": 6,
          "operation": "reduce",
          "chunks": [
            10,
            11
          ],
          "element_start": 31457280,
          "element_stop": 37748736,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 10,
              "contributors": [
                5
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                5
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r5:local",
              "receiver": "r6:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 31457280,
              "element_stop": 37748736,
              "path": [
                "rank5.tx",
                "local.5->6",
                "rank6.rx"
              ]
            }
          ]
        },
        {
          "sender": 6,
          "receiver": 7,
          "operation": "reduce",
          "chunks": [
            12,
            13
          ],
          "element_start": 37748736,
          "element_stop": 44040192,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 12,
              "contributors": [
                6
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                6
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r6:local",
              "receiver": "r7:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 37748736,
              "element_stop": 44040192,
              "path": [
                "rank6.tx",
                "local.6->7",
                "rank7.rx"
              ]
            }
          ]
        },
        {
          "sender": 7,
          "receiver": 0,
          "operation": "reduce",
          "chunks": [
            14,
            15
          ],
          "element_start": 44040192,
          "element_stop": 50331648,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 14,
              "contributors": [
                7
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                7
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r7:local",
              "receiver": "r0:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 44040192,
              "element_stop": 50331648,
              "path": [
                "rank7.tx",
                "local.7->0",
                "rank0.rx"
              ]
            }
          ]
        },
        {
          "sender": 8,
          "receiver": 9,
          "operation": "reduce",
          "chunks": [
            0,
            1
          ],
          "element_start": 0,
          "element_stop": 6291456,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 0,
              "contributors": [
                8
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                8
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r8:local",
              "receiver": "r9:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 0,
              "element_stop": 6291456,
              "path": [
                "rank8.tx",
                "local.8->9",
                "rank9.rx"
              ]
            }
          ]
        },
        {
          "sender": 9,
          "receiver": 10,
          "operation": "reduce",
          "chunks": [
            2,
            3
          ],
          "element_start": 6291456,
          "element_stop": 12582912,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 2,
              "contributors": [
                9
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                9
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r9:local",
              "receiver": "r10:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 6291456,
              "element_stop": 12582912,
              "path": [
                "rank9.tx",
                "local.9->10",
                "rank10.rx"
              ]
            }
          ]
        },
        {
          "sender": 10,
          "receiver": 11,
          "operation": "reduce",
          "chunks": [
            4,
            5
          ],
          "element_start": 12582912,
          "element_stop": 18874368,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 4,
              "contributors": [
                10
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                10
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r10:local",
              "receiver": "r11:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 12582912,
              "element_stop": 18874368,
              "path": [
                "rank10.tx",
                "local.10->11",
                "rank11.rx"
              ]
            }
          ]
        },
        {
          "sender": 11,
          "receiver": 12,
          "operation": "reduce",
          "chunks": [
            6,
            7
          ],
          "element_start": 18874368,
          "element_stop": 25165824,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 6,
              "contributors": [
                11
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                11
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r11:local",
              "receiver": "r12:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 18874368,
              "element_stop": 25165824,
              "path": [
                "rank11.tx",
                "local.11->12",
                "rank12.rx"
              ]
            }
          ]
        },
        {
          "sender": 12,
          "receiver": 13,
          "operation": "reduce",
          "chunks": [
            8,
            9
          ],
          "element_start": 25165824,
          "element_stop": 31457280,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 8,
              "contributors": [
                12
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                12
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r12:local",
              "receiver": "r13:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 25165824,
              "element_stop": 31457280,
              "path": [
                "rank12.tx",
                "local.12->13",
                "rank13.rx"
              ]
            }
          ]
        },
        {
          "sender": 13,
          "receiver": 14,
          "operation": "reduce",
          "chunks": [
            10,
            11
          ],
          "element_start": 31457280,
          "element_stop": 37748736,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 10,
              "contributors": [
                13
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                13
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r13:local",
              "receiver": "r14:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 31457280,
              "element_stop": 37748736,
              "path": [
                "rank13.tx",
                "local.13->14",
                "rank14.rx"
              ]
            }
          ]
        },
        {
          "sender": 14,
          "receiver": 15,
          "operation": "reduce",
          "chunks": [
            12,
            13
          ],
          "element_start": 37748736,
          "element_stop": 44040192,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 12,
              "contributors": [
                14
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                14
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r14:local",
              "receiver": "r15:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 37748736,
              "element_stop": 44040192,
              "path": [
                "rank14.tx",
                "local.14->15",
                "rank15.rx"
              ]
            }
          ]
        },
        {
          "sender": 15,
          "receiver": 8,
          "operation": "reduce",
          "chunks": [
            14,
            15
          ],
          "element_start": 44040192,
          "element_stop": 50331648,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 14,
              "contributors": [
                15
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r15:local",
              "receiver": "r8:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 44040192,
              "element_stop": 50331648,
              "path": [
                "rank15.tx",
                "local.15->8",
                "rank8.rx"
              ]
            }
          ]
        }
      ],
      "edges": [
        {
          "sender": "r0:local",
          "receiver": "r1:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 0,
          "element_stop": 6291456,
          "path": [
            "rank0.tx",
            "local.0->1",
            "rank1.rx"
          ]
        },
        {
          "sender": "r1:local",
          "receiver": "r2:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 6291456,
          "element_stop": 12582912,
          "path": [
            "rank1.tx",
            "local.1->2",
            "rank2.rx"
          ]
        },
        {
          "sender": "r2:local",
          "receiver": "r3:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 12582912,
          "element_stop": 18874368,
          "path": [
            "rank2.tx",
            "local.2->3",
            "rank3.rx"
          ]
        },
        {
          "sender": "r3:local",
          "receiver": "r4:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 18874368,
          "element_stop": 25165824,
          "path": [
            "rank3.tx",
            "local.3->4",
            "rank4.rx"
          ]
        },
        {
          "sender": "r4:local",
          "receiver": "r5:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 25165824,
          "element_stop": 31457280,
          "path": [
            "rank4.tx",
            "local.4->5",
            "rank5.rx"
          ]
        },
        {
          "sender": "r5:local",
          "receiver": "r6:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 31457280,
          "element_stop": 37748736,
          "path": [
            "rank5.tx",
            "local.5->6",
            "rank6.rx"
          ]
        },
        {
          "sender": "r6:local",
          "receiver": "r7:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 37748736,
          "element_stop": 44040192,
          "path": [
            "rank6.tx",
            "local.6->7",
            "rank7.rx"
          ]
        },
        {
          "sender": "r7:local",
          "receiver": "r0:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 44040192,
          "element_stop": 50331648,
          "path": [
            "rank7.tx",
            "local.7->0",
            "rank0.rx"
          ]
        },
        {
          "sender": "r8:local",
          "receiver": "r9:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 0,
          "element_stop": 6291456,
          "path": [
            "rank8.tx",
            "local.8->9",
            "rank9.rx"
          ]
        },
        {
          "sender": "r9:local",
          "receiver": "r10:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 6291456,
          "element_stop": 12582912,
          "path": [
            "rank9.tx",
            "local.9->10",
            "rank10.rx"
          ]
        },
        {
          "sender": "r10:local",
          "receiver": "r11:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 12582912,
          "element_stop": 18874368,
          "path": [
            "rank10.tx",
            "local.10->11",
            "rank11.rx"
          ]
        },
        {
          "sender": "r11:local",
          "receiver": "r12:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 18874368,
          "element_stop": 25165824,
          "path": [
            "rank11.tx",
            "local.11->12",
            "rank12.rx"
          ]
        },
        {
          "sender": "r12:local",
          "receiver": "r13:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 25165824,
          "element_stop": 31457280,
          "path": [
            "rank12.tx",
            "local.12->13",
            "rank13.rx"
          ]
        },
        {
          "sender": "r13:local",
          "receiver": "r14:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 31457280,
          "element_stop": 37748736,
          "path": [
            "rank13.tx",
            "local.13->14",
            "rank14.rx"
          ]
        },
        {
          "sender": "r14:local",
          "receiver": "r15:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 37748736,
          "element_stop": 44040192,
          "path": [
            "rank14.tx",
            "local.14->15",
            "rank15.rx"
          ]
        },
        {
          "sender": "r15:local",
          "receiver": "r8:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 44040192,
          "element_stop": 50331648,
          "path": [
            "rank15.tx",
            "local.15->8",
            "rank8.rx"
          ]
        }
      ],
      "resource_bytes": {
        "rank0.tx": 12582912,
        "local.0->1": 12582912,
        "rank1.rx": 12582912,
        "rank1.tx": 12582912,
        "local.1->2": 12582912,
        "rank2.rx": 12582912,
        "rank2.tx": 12582912,
        "local.2->3": 12582912,
        "rank3.rx": 12582912,
        "rank3.tx": 12582912,
        "local.3->4": 12582912,
        "rank4.rx": 12582912,
        "rank4.tx": 12582912,
        "local.4->5": 12582912,
        "rank5.rx": 12582912,
        "rank5.tx": 12582912,
        "local.5->6": 12582912,
        "rank6.rx": 12582912,
        "rank6.tx": 12582912,
        "local.6->7": 12582912,
        "rank7.rx": 12582912,
        "rank7.tx": 12582912,
        "local.7->0": 12582912,
        "rank0.rx": 12582912,
        "rank8.tx": 12582912,
        "local.8->9": 12582912,
        "rank9.rx": 12582912,
        "rank9.tx": 12582912,
        "local.9->10": 12582912,
        "rank10.rx": 12582912,
        "rank10.tx": 12582912,
        "local.10->11": 12582912,
        "rank11.rx": 12582912,
        "rank11.tx": 12582912,
        "local.11->12": 12582912,
        "rank12.rx": 12582912,
        "rank12.tx": 12582912,
        "local.12->13": 12582912,
        "rank13.rx": 12582912,
        "rank13.tx": 12582912,
        "local.13->14": 12582912,
        "rank14.rx": 12582912,
        "rank14.tx": 12582912,
        "local.14->15": 12582912,
        "rank15.rx": 12582912,
        "rank15.tx": 12582912,
        "local.15->8": 12582912,
        "rank8.rx": 12582912
      },
      "resource_lower_seconds_exact": "4096/146484375",
      "barrier_lower_seconds_exact": "2159627/75000000000",
      "barrier_start_seconds_exact": "0",
      "barrier_finish_seconds_exact": "2159627/75000000000"
    },
    {
      "round": 1,
      "stage": "local_reduce_scatter",
      "phase": "reduce_scatter",
      "step": 1,
      "messages": [
        {
          "sender": 0,
          "receiver": 1,
          "operation": "reduce",
          "chunks": [
            14,
            15
          ],
          "element_start": 44040192,
          "element_stop": 50331648,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 14,
              "contributors": [
                0,
                7
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                0,
                7
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r0:local",
              "receiver": "r1:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 44040192,
              "element_stop": 50331648,
              "path": [
                "rank0.tx",
                "local.0->1",
                "rank1.rx"
              ]
            }
          ]
        },
        {
          "sender": 1,
          "receiver": 2,
          "operation": "reduce",
          "chunks": [
            0,
            1
          ],
          "element_start": 0,
          "element_stop": 6291456,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 0,
              "contributors": [
                0,
                1
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                0,
                1
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r1:local",
              "receiver": "r2:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 0,
              "element_stop": 6291456,
              "path": [
                "rank1.tx",
                "local.1->2",
                "rank2.rx"
              ]
            }
          ]
        },
        {
          "sender": 2,
          "receiver": 3,
          "operation": "reduce",
          "chunks": [
            2,
            3
          ],
          "element_start": 6291456,
          "element_stop": 12582912,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 2,
              "contributors": [
                1,
                2
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                1,
                2
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r2:local",
              "receiver": "r3:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 6291456,
              "element_stop": 12582912,
              "path": [
                "rank2.tx",
                "local.2->3",
                "rank3.rx"
              ]
            }
          ]
        },
        {
          "sender": 3,
          "receiver": 4,
          "operation": "reduce",
          "chunks": [
            4,
            5
          ],
          "element_start": 12582912,
          "element_stop": 18874368,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 4,
              "contributors": [
                2,
                3
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                2,
                3
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r3:local",
              "receiver": "r4:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 12582912,
              "element_stop": 18874368,
              "path": [
                "rank3.tx",
                "local.3->4",
                "rank4.rx"
              ]
            }
          ]
        },
        {
          "sender": 4,
          "receiver": 5,
          "operation": "reduce",
          "chunks": [
            6,
            7
          ],
          "element_start": 18874368,
          "element_stop": 25165824,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 6,
              "contributors": [
                3,
                4
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                3,
                4
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r4:local",
              "receiver": "r5:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 18874368,
              "element_stop": 25165824,
              "path": [
                "rank4.tx",
                "local.4->5",
                "rank5.rx"
              ]
            }
          ]
        },
        {
          "sender": 5,
          "receiver": 6,
          "operation": "reduce",
          "chunks": [
            8,
            9
          ],
          "element_start": 25165824,
          "element_stop": 31457280,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 8,
              "contributors": [
                4,
                5
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                4,
                5
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r5:local",
              "receiver": "r6:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 25165824,
              "element_stop": 31457280,
              "path": [
                "rank5.tx",
                "local.5->6",
                "rank6.rx"
              ]
            }
          ]
        },
        {
          "sender": 6,
          "receiver": 7,
          "operation": "reduce",
          "chunks": [
            10,
            11
          ],
          "element_start": 31457280,
          "element_stop": 37748736,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 10,
              "contributors": [
                5,
                6
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                5,
                6
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r6:local",
              "receiver": "r7:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 31457280,
              "element_stop": 37748736,
              "path": [
                "rank6.tx",
                "local.6->7",
                "rank7.rx"
              ]
            }
          ]
        },
        {
          "sender": 7,
          "receiver": 0,
          "operation": "reduce",
          "chunks": [
            12,
            13
          ],
          "element_start": 37748736,
          "element_stop": 44040192,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 12,
              "contributors": [
                6,
                7
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                6,
                7
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r7:local",
              "receiver": "r0:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 37748736,
              "element_stop": 44040192,
              "path": [
                "rank7.tx",
                "local.7->0",
                "rank0.rx"
              ]
            }
          ]
        },
        {
          "sender": 8,
          "receiver": 9,
          "operation": "reduce",
          "chunks": [
            14,
            15
          ],
          "element_start": 44040192,
          "element_stop": 50331648,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 14,
              "contributors": [
                8,
                15
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                8,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r8:local",
              "receiver": "r9:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 44040192,
              "element_stop": 50331648,
              "path": [
                "rank8.tx",
                "local.8->9",
                "rank9.rx"
              ]
            }
          ]
        },
        {
          "sender": 9,
          "receiver": 10,
          "operation": "reduce",
          "chunks": [
            0,
            1
          ],
          "element_start": 0,
          "element_stop": 6291456,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 0,
              "contributors": [
                8,
                9
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                8,
                9
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r9:local",
              "receiver": "r10:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 0,
              "element_stop": 6291456,
              "path": [
                "rank9.tx",
                "local.9->10",
                "rank10.rx"
              ]
            }
          ]
        },
        {
          "sender": 10,
          "receiver": 11,
          "operation": "reduce",
          "chunks": [
            2,
            3
          ],
          "element_start": 6291456,
          "element_stop": 12582912,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 2,
              "contributors": [
                9,
                10
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                9,
                10
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r10:local",
              "receiver": "r11:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 6291456,
              "element_stop": 12582912,
              "path": [
                "rank10.tx",
                "local.10->11",
                "rank11.rx"
              ]
            }
          ]
        },
        {
          "sender": 11,
          "receiver": 12,
          "operation": "reduce",
          "chunks": [
            4,
            5
          ],
          "element_start": 12582912,
          "element_stop": 18874368,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 4,
              "contributors": [
                10,
                11
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                10,
                11
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r11:local",
              "receiver": "r12:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 12582912,
              "element_stop": 18874368,
              "path": [
                "rank11.tx",
                "local.11->12",
                "rank12.rx"
              ]
            }
          ]
        },
        {
          "sender": 12,
          "receiver": 13,
          "operation": "reduce",
          "chunks": [
            6,
            7
          ],
          "element_start": 18874368,
          "element_stop": 25165824,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 6,
              "contributors": [
                11,
                12
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                11,
                12
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r12:local",
              "receiver": "r13:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 18874368,
              "element_stop": 25165824,
              "path": [
                "rank12.tx",
                "local.12->13",
                "rank13.rx"
              ]
            }
          ]
        },
        {
          "sender": 13,
          "receiver": 14,
          "operation": "reduce",
          "chunks": [
            8,
            9
          ],
          "element_start": 25165824,
          "element_stop": 31457280,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 8,
              "contributors": [
                12,
                13
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                12,
                13
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r13:local",
              "receiver": "r14:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 25165824,
              "element_stop": 31457280,
              "path": [
                "rank13.tx",
                "local.13->14",
                "rank14.rx"
              ]
            }
          ]
        },
        {
          "sender": 14,
          "receiver": 15,
          "operation": "reduce",
          "chunks": [
            10,
            11
          ],
          "element_start": 31457280,
          "element_stop": 37748736,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 10,
              "contributors": [
                13,
                14
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                13,
                14
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r14:local",
              "receiver": "r15:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 31457280,
              "element_stop": 37748736,
              "path": [
                "rank14.tx",
                "local.14->15",
                "rank15.rx"
              ]
            }
          ]
        },
        {
          "sender": 15,
          "receiver": 8,
          "operation": "reduce",
          "chunks": [
            12,
            13
          ],
          "element_start": 37748736,
          "element_stop": 44040192,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 12,
              "contributors": [
                14,
                15
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r15:local",
              "receiver": "r8:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 37748736,
              "element_stop": 44040192,
              "path": [
                "rank15.tx",
                "local.15->8",
                "rank8.rx"
              ]
            }
          ]
        }
      ],
      "edges": [
        {
          "sender": "r0:local",
          "receiver": "r1:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 44040192,
          "element_stop": 50331648,
          "path": [
            "rank0.tx",
            "local.0->1",
            "rank1.rx"
          ]
        },
        {
          "sender": "r1:local",
          "receiver": "r2:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 0,
          "element_stop": 6291456,
          "path": [
            "rank1.tx",
            "local.1->2",
            "rank2.rx"
          ]
        },
        {
          "sender": "r2:local",
          "receiver": "r3:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 6291456,
          "element_stop": 12582912,
          "path": [
            "rank2.tx",
            "local.2->3",
            "rank3.rx"
          ]
        },
        {
          "sender": "r3:local",
          "receiver": "r4:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 12582912,
          "element_stop": 18874368,
          "path": [
            "rank3.tx",
            "local.3->4",
            "rank4.rx"
          ]
        },
        {
          "sender": "r4:local",
          "receiver": "r5:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 18874368,
          "element_stop": 25165824,
          "path": [
            "rank4.tx",
            "local.4->5",
            "rank5.rx"
          ]
        },
        {
          "sender": "r5:local",
          "receiver": "r6:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 25165824,
          "element_stop": 31457280,
          "path": [
            "rank5.tx",
            "local.5->6",
            "rank6.rx"
          ]
        },
        {
          "sender": "r6:local",
          "receiver": "r7:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 31457280,
          "element_stop": 37748736,
          "path": [
            "rank6.tx",
            "local.6->7",
            "rank7.rx"
          ]
        },
        {
          "sender": "r7:local",
          "receiver": "r0:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 37748736,
          "element_stop": 44040192,
          "path": [
            "rank7.tx",
            "local.7->0",
            "rank0.rx"
          ]
        },
        {
          "sender": "r8:local",
          "receiver": "r9:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 44040192,
          "element_stop": 50331648,
          "path": [
            "rank8.tx",
            "local.8->9",
            "rank9.rx"
          ]
        },
        {
          "sender": "r9:local",
          "receiver": "r10:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 0,
          "element_stop": 6291456,
          "path": [
            "rank9.tx",
            "local.9->10",
            "rank10.rx"
          ]
        },
        {
          "sender": "r10:local",
          "receiver": "r11:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 6291456,
          "element_stop": 12582912,
          "path": [
            "rank10.tx",
            "local.10->11",
            "rank11.rx"
          ]
        },
        {
          "sender": "r11:local",
          "receiver": "r12:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 12582912,
          "element_stop": 18874368,
          "path": [
            "rank11.tx",
            "local.11->12",
            "rank12.rx"
          ]
        },
        {
          "sender": "r12:local",
          "receiver": "r13:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 18874368,
          "element_stop": 25165824,
          "path": [
            "rank12.tx",
            "local.12->13",
            "rank13.rx"
          ]
        },
        {
          "sender": "r13:local",
          "receiver": "r14:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 25165824,
          "element_stop": 31457280,
          "path": [
            "rank13.tx",
            "local.13->14",
            "rank14.rx"
          ]
        },
        {
          "sender": "r14:local",
          "receiver": "r15:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 31457280,
          "element_stop": 37748736,
          "path": [
            "rank14.tx",
            "local.14->15",
            "rank15.rx"
          ]
        },
        {
          "sender": "r15:local",
          "receiver": "r8:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 37748736,
          "element_stop": 44040192,
          "path": [
            "rank15.tx",
            "local.15->8",
            "rank8.rx"
          ]
        }
      ],
      "resource_bytes": {
        "rank0.tx": 12582912,
        "local.0->1": 12582912,
        "rank1.rx": 12582912,
        "rank1.tx": 12582912,
        "local.1->2": 12582912,
        "rank2.rx": 12582912,
        "rank2.tx": 12582912,
        "local.2->3": 12582912,
        "rank3.rx": 12582912,
        "rank3.tx": 12582912,
        "local.3->4": 12582912,
        "rank4.rx": 12582912,
        "rank4.tx": 12582912,
        "local.4->5": 12582912,
        "rank5.rx": 12582912,
        "rank5.tx": 12582912,
        "local.5->6": 12582912,
        "rank6.rx": 12582912,
        "rank6.tx": 12582912,
        "local.6->7": 12582912,
        "rank7.rx": 12582912,
        "rank7.tx": 12582912,
        "local.7->0": 12582912,
        "rank0.rx": 12582912,
        "rank8.tx": 12582912,
        "local.8->9": 12582912,
        "rank9.rx": 12582912,
        "rank9.tx": 12582912,
        "local.9->10": 12582912,
        "rank10.rx": 12582912,
        "rank10.tx": 12582912,
        "local.10->11": 12582912,
        "rank11.rx": 12582912,
        "rank11.tx": 12582912,
        "local.11->12": 12582912,
        "rank12.rx": 12582912,
        "rank12.tx": 12582912,
        "local.12->13": 12582912,
        "rank13.rx": 12582912,
        "rank13.tx": 12582912,
        "local.13->14": 12582912,
        "rank14.rx": 12582912,
        "rank14.tx": 12582912,
        "local.14->15": 12582912,
        "rank15.rx": 12582912,
        "rank15.tx": 12582912,
        "local.15->8": 12582912,
        "rank8.rx": 12582912
      },
      "resource_lower_seconds_exact": "4096/146484375",
      "barrier_lower_seconds_exact": "2159627/75000000000",
      "barrier_start_seconds_exact": "2159627/75000000000",
      "barrier_finish_seconds_exact": "2159627/37500000000"
    },
    {
      "round": 2,
      "stage": "local_reduce_scatter",
      "phase": "reduce_scatter",
      "step": 2,
      "messages": [
        {
          "sender": 0,
          "receiver": 1,
          "operation": "reduce",
          "chunks": [
            12,
            13
          ],
          "element_start": 37748736,
          "element_stop": 44040192,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 12,
              "contributors": [
                0,
                6,
                7
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                0,
                6,
                7
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r0:local",
              "receiver": "r1:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 37748736,
              "element_stop": 44040192,
              "path": [
                "rank0.tx",
                "local.0->1",
                "rank1.rx"
              ]
            }
          ]
        },
        {
          "sender": 1,
          "receiver": 2,
          "operation": "reduce",
          "chunks": [
            14,
            15
          ],
          "element_start": 44040192,
          "element_stop": 50331648,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 14,
              "contributors": [
                0,
                1,
                7
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                0,
                1,
                7
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r1:local",
              "receiver": "r2:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 44040192,
              "element_stop": 50331648,
              "path": [
                "rank1.tx",
                "local.1->2",
                "rank2.rx"
              ]
            }
          ]
        },
        {
          "sender": 2,
          "receiver": 3,
          "operation": "reduce",
          "chunks": [
            0,
            1
          ],
          "element_start": 0,
          "element_stop": 6291456,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 0,
              "contributors": [
                0,
                1,
                2
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                0,
                1,
                2
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r2:local",
              "receiver": "r3:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 0,
              "element_stop": 6291456,
              "path": [
                "rank2.tx",
                "local.2->3",
                "rank3.rx"
              ]
            }
          ]
        },
        {
          "sender": 3,
          "receiver": 4,
          "operation": "reduce",
          "chunks": [
            2,
            3
          ],
          "element_start": 6291456,
          "element_stop": 12582912,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 2,
              "contributors": [
                1,
                2,
                3
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                1,
                2,
                3
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r3:local",
              "receiver": "r4:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 6291456,
              "element_stop": 12582912,
              "path": [
                "rank3.tx",
                "local.3->4",
                "rank4.rx"
              ]
            }
          ]
        },
        {
          "sender": 4,
          "receiver": 5,
          "operation": "reduce",
          "chunks": [
            4,
            5
          ],
          "element_start": 12582912,
          "element_stop": 18874368,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 4,
              "contributors": [
                2,
                3,
                4
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                2,
                3,
                4
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r4:local",
              "receiver": "r5:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 12582912,
              "element_stop": 18874368,
              "path": [
                "rank4.tx",
                "local.4->5",
                "rank5.rx"
              ]
            }
          ]
        },
        {
          "sender": 5,
          "receiver": 6,
          "operation": "reduce",
          "chunks": [
            6,
            7
          ],
          "element_start": 18874368,
          "element_stop": 25165824,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 6,
              "contributors": [
                3,
                4,
                5
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                3,
                4,
                5
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r5:local",
              "receiver": "r6:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 18874368,
              "element_stop": 25165824,
              "path": [
                "rank5.tx",
                "local.5->6",
                "rank6.rx"
              ]
            }
          ]
        },
        {
          "sender": 6,
          "receiver": 7,
          "operation": "reduce",
          "chunks": [
            8,
            9
          ],
          "element_start": 25165824,
          "element_stop": 31457280,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 8,
              "contributors": [
                4,
                5,
                6
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                4,
                5,
                6
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r6:local",
              "receiver": "r7:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 25165824,
              "element_stop": 31457280,
              "path": [
                "rank6.tx",
                "local.6->7",
                "rank7.rx"
              ]
            }
          ]
        },
        {
          "sender": 7,
          "receiver": 0,
          "operation": "reduce",
          "chunks": [
            10,
            11
          ],
          "element_start": 31457280,
          "element_stop": 37748736,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 10,
              "contributors": [
                5,
                6,
                7
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                5,
                6,
                7
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r7:local",
              "receiver": "r0:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 31457280,
              "element_stop": 37748736,
              "path": [
                "rank7.tx",
                "local.7->0",
                "rank0.rx"
              ]
            }
          ]
        },
        {
          "sender": 8,
          "receiver": 9,
          "operation": "reduce",
          "chunks": [
            12,
            13
          ],
          "element_start": 37748736,
          "element_stop": 44040192,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 12,
              "contributors": [
                8,
                14,
                15
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                8,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r8:local",
              "receiver": "r9:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 37748736,
              "element_stop": 44040192,
              "path": [
                "rank8.tx",
                "local.8->9",
                "rank9.rx"
              ]
            }
          ]
        },
        {
          "sender": 9,
          "receiver": 10,
          "operation": "reduce",
          "chunks": [
            14,
            15
          ],
          "element_start": 44040192,
          "element_stop": 50331648,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 14,
              "contributors": [
                8,
                9,
                15
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                8,
                9,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r9:local",
              "receiver": "r10:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 44040192,
              "element_stop": 50331648,
              "path": [
                "rank9.tx",
                "local.9->10",
                "rank10.rx"
              ]
            }
          ]
        },
        {
          "sender": 10,
          "receiver": 11,
          "operation": "reduce",
          "chunks": [
            0,
            1
          ],
          "element_start": 0,
          "element_stop": 6291456,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 0,
              "contributors": [
                8,
                9,
                10
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                8,
                9,
                10
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r10:local",
              "receiver": "r11:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 0,
              "element_stop": 6291456,
              "path": [
                "rank10.tx",
                "local.10->11",
                "rank11.rx"
              ]
            }
          ]
        },
        {
          "sender": 11,
          "receiver": 12,
          "operation": "reduce",
          "chunks": [
            2,
            3
          ],
          "element_start": 6291456,
          "element_stop": 12582912,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 2,
              "contributors": [
                9,
                10,
                11
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                9,
                10,
                11
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r11:local",
              "receiver": "r12:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 6291456,
              "element_stop": 12582912,
              "path": [
                "rank11.tx",
                "local.11->12",
                "rank12.rx"
              ]
            }
          ]
        },
        {
          "sender": 12,
          "receiver": 13,
          "operation": "reduce",
          "chunks": [
            4,
            5
          ],
          "element_start": 12582912,
          "element_stop": 18874368,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 4,
              "contributors": [
                10,
                11,
                12
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                10,
                11,
                12
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r12:local",
              "receiver": "r13:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 12582912,
              "element_stop": 18874368,
              "path": [
                "rank12.tx",
                "local.12->13",
                "rank13.rx"
              ]
            }
          ]
        },
        {
          "sender": 13,
          "receiver": 14,
          "operation": "reduce",
          "chunks": [
            6,
            7
          ],
          "element_start": 18874368,
          "element_stop": 25165824,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 6,
              "contributors": [
                11,
                12,
                13
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                11,
                12,
                13
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r13:local",
              "receiver": "r14:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 18874368,
              "element_stop": 25165824,
              "path": [
                "rank13.tx",
                "local.13->14",
                "rank14.rx"
              ]
            }
          ]
        },
        {
          "sender": 14,
          "receiver": 15,
          "operation": "reduce",
          "chunks": [
            8,
            9
          ],
          "element_start": 25165824,
          "element_stop": 31457280,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 8,
              "contributors": [
                12,
                13,
                14
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                12,
                13,
                14
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r14:local",
              "receiver": "r15:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 25165824,
              "element_stop": 31457280,
              "path": [
                "rank14.tx",
                "local.14->15",
                "rank15.rx"
              ]
            }
          ]
        },
        {
          "sender": 15,
          "receiver": 8,
          "operation": "reduce",
          "chunks": [
            10,
            11
          ],
          "element_start": 31457280,
          "element_stop": 37748736,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 10,
              "contributors": [
                13,
                14,
                15
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r15:local",
              "receiver": "r8:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 31457280,
              "element_stop": 37748736,
              "path": [
                "rank15.tx",
                "local.15->8",
                "rank8.rx"
              ]
            }
          ]
        }
      ],
      "edges": [
        {
          "sender": "r0:local",
          "receiver": "r1:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 37748736,
          "element_stop": 44040192,
          "path": [
            "rank0.tx",
            "local.0->1",
            "rank1.rx"
          ]
        },
        {
          "sender": "r1:local",
          "receiver": "r2:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 44040192,
          "element_stop": 50331648,
          "path": [
            "rank1.tx",
            "local.1->2",
            "rank2.rx"
          ]
        },
        {
          "sender": "r2:local",
          "receiver": "r3:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 0,
          "element_stop": 6291456,
          "path": [
            "rank2.tx",
            "local.2->3",
            "rank3.rx"
          ]
        },
        {
          "sender": "r3:local",
          "receiver": "r4:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 6291456,
          "element_stop": 12582912,
          "path": [
            "rank3.tx",
            "local.3->4",
            "rank4.rx"
          ]
        },
        {
          "sender": "r4:local",
          "receiver": "r5:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 12582912,
          "element_stop": 18874368,
          "path": [
            "rank4.tx",
            "local.4->5",
            "rank5.rx"
          ]
        },
        {
          "sender": "r5:local",
          "receiver": "r6:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 18874368,
          "element_stop": 25165824,
          "path": [
            "rank5.tx",
            "local.5->6",
            "rank6.rx"
          ]
        },
        {
          "sender": "r6:local",
          "receiver": "r7:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 25165824,
          "element_stop": 31457280,
          "path": [
            "rank6.tx",
            "local.6->7",
            "rank7.rx"
          ]
        },
        {
          "sender": "r7:local",
          "receiver": "r0:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 31457280,
          "element_stop": 37748736,
          "path": [
            "rank7.tx",
            "local.7->0",
            "rank0.rx"
          ]
        },
        {
          "sender": "r8:local",
          "receiver": "r9:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 37748736,
          "element_stop": 44040192,
          "path": [
            "rank8.tx",
            "local.8->9",
            "rank9.rx"
          ]
        },
        {
          "sender": "r9:local",
          "receiver": "r10:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 44040192,
          "element_stop": 50331648,
          "path": [
            "rank9.tx",
            "local.9->10",
            "rank10.rx"
          ]
        },
        {
          "sender": "r10:local",
          "receiver": "r11:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 0,
          "element_stop": 6291456,
          "path": [
            "rank10.tx",
            "local.10->11",
            "rank11.rx"
          ]
        },
        {
          "sender": "r11:local",
          "receiver": "r12:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 6291456,
          "element_stop": 12582912,
          "path": [
            "rank11.tx",
            "local.11->12",
            "rank12.rx"
          ]
        },
        {
          "sender": "r12:local",
          "receiver": "r13:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 12582912,
          "element_stop": 18874368,
          "path": [
            "rank12.tx",
            "local.12->13",
            "rank13.rx"
          ]
        },
        {
          "sender": "r13:local",
          "receiver": "r14:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 18874368,
          "element_stop": 25165824,
          "path": [
            "rank13.tx",
            "local.13->14",
            "rank14.rx"
          ]
        },
        {
          "sender": "r14:local",
          "receiver": "r15:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 25165824,
          "element_stop": 31457280,
          "path": [
            "rank14.tx",
            "local.14->15",
            "rank15.rx"
          ]
        },
        {
          "sender": "r15:local",
          "receiver": "r8:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 31457280,
          "element_stop": 37748736,
          "path": [
            "rank15.tx",
            "local.15->8",
            "rank8.rx"
          ]
        }
      ],
      "resource_bytes": {
        "rank0.tx": 12582912,
        "local.0->1": 12582912,
        "rank1.rx": 12582912,
        "rank1.tx": 12582912,
        "local.1->2": 12582912,
        "rank2.rx": 12582912,
        "rank2.tx": 12582912,
        "local.2->3": 12582912,
        "rank3.rx": 12582912,
        "rank3.tx": 12582912,
        "local.3->4": 12582912,
        "rank4.rx": 12582912,
        "rank4.tx": 12582912,
        "local.4->5": 12582912,
        "rank5.rx": 12582912,
        "rank5.tx": 12582912,
        "local.5->6": 12582912,
        "rank6.rx": 12582912,
        "rank6.tx": 12582912,
        "local.6->7": 12582912,
        "rank7.rx": 12582912,
        "rank7.tx": 12582912,
        "local.7->0": 12582912,
        "rank0.rx": 12582912,
        "rank8.tx": 12582912,
        "local.8->9": 12582912,
        "rank9.rx": 12582912,
        "rank9.tx": 12582912,
        "local.9->10": 12582912,
        "rank10.rx": 12582912,
        "rank10.tx": 12582912,
        "local.10->11": 12582912,
        "rank11.rx": 12582912,
        "rank11.tx": 12582912,
        "local.11->12": 12582912,
        "rank12.rx": 12582912,
        "rank12.tx": 12582912,
        "local.12->13": 12582912,
        "rank13.rx": 12582912,
        "rank13.tx": 12582912,
        "local.13->14": 12582912,
        "rank14.rx": 12582912,
        "rank14.tx": 12582912,
        "local.14->15": 12582912,
        "rank15.rx": 12582912,
        "rank15.tx": 12582912,
        "local.15->8": 12582912,
        "rank8.rx": 12582912
      },
      "resource_lower_seconds_exact": "4096/146484375",
      "barrier_lower_seconds_exact": "2159627/75000000000",
      "barrier_start_seconds_exact": "2159627/37500000000",
      "barrier_finish_seconds_exact": "2159627/25000000000"
    },
    {
      "round": 3,
      "stage": "local_reduce_scatter",
      "phase": "reduce_scatter",
      "step": 3,
      "messages": [
        {
          "sender": 0,
          "receiver": 1,
          "operation": "reduce",
          "chunks": [
            10,
            11
          ],
          "element_start": 31457280,
          "element_stop": 37748736,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 10,
              "contributors": [
                0,
                5,
                6,
                7
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                0,
                5,
                6,
                7
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r0:local",
              "receiver": "r1:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 31457280,
              "element_stop": 37748736,
              "path": [
                "rank0.tx",
                "local.0->1",
                "rank1.rx"
              ]
            }
          ]
        },
        {
          "sender": 1,
          "receiver": 2,
          "operation": "reduce",
          "chunks": [
            12,
            13
          ],
          "element_start": 37748736,
          "element_stop": 44040192,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 12,
              "contributors": [
                0,
                1,
                6,
                7
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                0,
                1,
                6,
                7
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r1:local",
              "receiver": "r2:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 37748736,
              "element_stop": 44040192,
              "path": [
                "rank1.tx",
                "local.1->2",
                "rank2.rx"
              ]
            }
          ]
        },
        {
          "sender": 2,
          "receiver": 3,
          "operation": "reduce",
          "chunks": [
            14,
            15
          ],
          "element_start": 44040192,
          "element_stop": 50331648,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 14,
              "contributors": [
                0,
                1,
                2,
                7
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                0,
                1,
                2,
                7
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r2:local",
              "receiver": "r3:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 44040192,
              "element_stop": 50331648,
              "path": [
                "rank2.tx",
                "local.2->3",
                "rank3.rx"
              ]
            }
          ]
        },
        {
          "sender": 3,
          "receiver": 4,
          "operation": "reduce",
          "chunks": [
            0,
            1
          ],
          "element_start": 0,
          "element_stop": 6291456,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 0,
              "contributors": [
                0,
                1,
                2,
                3
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                0,
                1,
                2,
                3
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r3:local",
              "receiver": "r4:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 0,
              "element_stop": 6291456,
              "path": [
                "rank3.tx",
                "local.3->4",
                "rank4.rx"
              ]
            }
          ]
        },
        {
          "sender": 4,
          "receiver": 5,
          "operation": "reduce",
          "chunks": [
            2,
            3
          ],
          "element_start": 6291456,
          "element_stop": 12582912,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 2,
              "contributors": [
                1,
                2,
                3,
                4
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                1,
                2,
                3,
                4
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r4:local",
              "receiver": "r5:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 6291456,
              "element_stop": 12582912,
              "path": [
                "rank4.tx",
                "local.4->5",
                "rank5.rx"
              ]
            }
          ]
        },
        {
          "sender": 5,
          "receiver": 6,
          "operation": "reduce",
          "chunks": [
            4,
            5
          ],
          "element_start": 12582912,
          "element_stop": 18874368,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 4,
              "contributors": [
                2,
                3,
                4,
                5
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                2,
                3,
                4,
                5
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r5:local",
              "receiver": "r6:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 12582912,
              "element_stop": 18874368,
              "path": [
                "rank5.tx",
                "local.5->6",
                "rank6.rx"
              ]
            }
          ]
        },
        {
          "sender": 6,
          "receiver": 7,
          "operation": "reduce",
          "chunks": [
            6,
            7
          ],
          "element_start": 18874368,
          "element_stop": 25165824,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 6,
              "contributors": [
                3,
                4,
                5,
                6
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                3,
                4,
                5,
                6
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r6:local",
              "receiver": "r7:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 18874368,
              "element_stop": 25165824,
              "path": [
                "rank6.tx",
                "local.6->7",
                "rank7.rx"
              ]
            }
          ]
        },
        {
          "sender": 7,
          "receiver": 0,
          "operation": "reduce",
          "chunks": [
            8,
            9
          ],
          "element_start": 25165824,
          "element_stop": 31457280,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 8,
              "contributors": [
                4,
                5,
                6,
                7
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                4,
                5,
                6,
                7
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r7:local",
              "receiver": "r0:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 25165824,
              "element_stop": 31457280,
              "path": [
                "rank7.tx",
                "local.7->0",
                "rank0.rx"
              ]
            }
          ]
        },
        {
          "sender": 8,
          "receiver": 9,
          "operation": "reduce",
          "chunks": [
            10,
            11
          ],
          "element_start": 31457280,
          "element_stop": 37748736,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 10,
              "contributors": [
                8,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                8,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r8:local",
              "receiver": "r9:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 31457280,
              "element_stop": 37748736,
              "path": [
                "rank8.tx",
                "local.8->9",
                "rank9.rx"
              ]
            }
          ]
        },
        {
          "sender": 9,
          "receiver": 10,
          "operation": "reduce",
          "chunks": [
            12,
            13
          ],
          "element_start": 37748736,
          "element_stop": 44040192,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 12,
              "contributors": [
                8,
                9,
                14,
                15
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                8,
                9,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r9:local",
              "receiver": "r10:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 37748736,
              "element_stop": 44040192,
              "path": [
                "rank9.tx",
                "local.9->10",
                "rank10.rx"
              ]
            }
          ]
        },
        {
          "sender": 10,
          "receiver": 11,
          "operation": "reduce",
          "chunks": [
            14,
            15
          ],
          "element_start": 44040192,
          "element_stop": 50331648,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 14,
              "contributors": [
                8,
                9,
                10,
                15
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                8,
                9,
                10,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r10:local",
              "receiver": "r11:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 44040192,
              "element_stop": 50331648,
              "path": [
                "rank10.tx",
                "local.10->11",
                "rank11.rx"
              ]
            }
          ]
        },
        {
          "sender": 11,
          "receiver": 12,
          "operation": "reduce",
          "chunks": [
            0,
            1
          ],
          "element_start": 0,
          "element_stop": 6291456,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 0,
              "contributors": [
                8,
                9,
                10,
                11
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                8,
                9,
                10,
                11
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r11:local",
              "receiver": "r12:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 0,
              "element_stop": 6291456,
              "path": [
                "rank11.tx",
                "local.11->12",
                "rank12.rx"
              ]
            }
          ]
        },
        {
          "sender": 12,
          "receiver": 13,
          "operation": "reduce",
          "chunks": [
            2,
            3
          ],
          "element_start": 6291456,
          "element_stop": 12582912,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 2,
              "contributors": [
                9,
                10,
                11,
                12
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                9,
                10,
                11,
                12
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r12:local",
              "receiver": "r13:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 6291456,
              "element_stop": 12582912,
              "path": [
                "rank12.tx",
                "local.12->13",
                "rank13.rx"
              ]
            }
          ]
        },
        {
          "sender": 13,
          "receiver": 14,
          "operation": "reduce",
          "chunks": [
            4,
            5
          ],
          "element_start": 12582912,
          "element_stop": 18874368,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 4,
              "contributors": [
                10,
                11,
                12,
                13
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                10,
                11,
                12,
                13
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r13:local",
              "receiver": "r14:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 12582912,
              "element_stop": 18874368,
              "path": [
                "rank13.tx",
                "local.13->14",
                "rank14.rx"
              ]
            }
          ]
        },
        {
          "sender": 14,
          "receiver": 15,
          "operation": "reduce",
          "chunks": [
            6,
            7
          ],
          "element_start": 18874368,
          "element_stop": 25165824,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 6,
              "contributors": [
                11,
                12,
                13,
                14
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                11,
                12,
                13,
                14
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r14:local",
              "receiver": "r15:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 18874368,
              "element_stop": 25165824,
              "path": [
                "rank14.tx",
                "local.14->15",
                "rank15.rx"
              ]
            }
          ]
        },
        {
          "sender": 15,
          "receiver": 8,
          "operation": "reduce",
          "chunks": [
            8,
            9
          ],
          "element_start": 25165824,
          "element_stop": 31457280,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 8,
              "contributors": [
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r15:local",
              "receiver": "r8:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 25165824,
              "element_stop": 31457280,
              "path": [
                "rank15.tx",
                "local.15->8",
                "rank8.rx"
              ]
            }
          ]
        }
      ],
      "edges": [
        {
          "sender": "r0:local",
          "receiver": "r1:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 31457280,
          "element_stop": 37748736,
          "path": [
            "rank0.tx",
            "local.0->1",
            "rank1.rx"
          ]
        },
        {
          "sender": "r1:local",
          "receiver": "r2:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 37748736,
          "element_stop": 44040192,
          "path": [
            "rank1.tx",
            "local.1->2",
            "rank2.rx"
          ]
        },
        {
          "sender": "r2:local",
          "receiver": "r3:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 44040192,
          "element_stop": 50331648,
          "path": [
            "rank2.tx",
            "local.2->3",
            "rank3.rx"
          ]
        },
        {
          "sender": "r3:local",
          "receiver": "r4:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 0,
          "element_stop": 6291456,
          "path": [
            "rank3.tx",
            "local.3->4",
            "rank4.rx"
          ]
        },
        {
          "sender": "r4:local",
          "receiver": "r5:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 6291456,
          "element_stop": 12582912,
          "path": [
            "rank4.tx",
            "local.4->5",
            "rank5.rx"
          ]
        },
        {
          "sender": "r5:local",
          "receiver": "r6:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 12582912,
          "element_stop": 18874368,
          "path": [
            "rank5.tx",
            "local.5->6",
            "rank6.rx"
          ]
        },
        {
          "sender": "r6:local",
          "receiver": "r7:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 18874368,
          "element_stop": 25165824,
          "path": [
            "rank6.tx",
            "local.6->7",
            "rank7.rx"
          ]
        },
        {
          "sender": "r7:local",
          "receiver": "r0:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 25165824,
          "element_stop": 31457280,
          "path": [
            "rank7.tx",
            "local.7->0",
            "rank0.rx"
          ]
        },
        {
          "sender": "r8:local",
          "receiver": "r9:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 31457280,
          "element_stop": 37748736,
          "path": [
            "rank8.tx",
            "local.8->9",
            "rank9.rx"
          ]
        },
        {
          "sender": "r9:local",
          "receiver": "r10:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 37748736,
          "element_stop": 44040192,
          "path": [
            "rank9.tx",
            "local.9->10",
            "rank10.rx"
          ]
        },
        {
          "sender": "r10:local",
          "receiver": "r11:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 44040192,
          "element_stop": 50331648,
          "path": [
            "rank10.tx",
            "local.10->11",
            "rank11.rx"
          ]
        },
        {
          "sender": "r11:local",
          "receiver": "r12:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 0,
          "element_stop": 6291456,
          "path": [
            "rank11.tx",
            "local.11->12",
            "rank12.rx"
          ]
        },
        {
          "sender": "r12:local",
          "receiver": "r13:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 6291456,
          "element_stop": 12582912,
          "path": [
            "rank12.tx",
            "local.12->13",
            "rank13.rx"
          ]
        },
        {
          "sender": "r13:local",
          "receiver": "r14:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 12582912,
          "element_stop": 18874368,
          "path": [
            "rank13.tx",
            "local.13->14",
            "rank14.rx"
          ]
        },
        {
          "sender": "r14:local",
          "receiver": "r15:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 18874368,
          "element_stop": 25165824,
          "path": [
            "rank14.tx",
            "local.14->15",
            "rank15.rx"
          ]
        },
        {
          "sender": "r15:local",
          "receiver": "r8:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 25165824,
          "element_stop": 31457280,
          "path": [
            "rank15.tx",
            "local.15->8",
            "rank8.rx"
          ]
        }
      ],
      "resource_bytes": {
        "rank0.tx": 12582912,
        "local.0->1": 12582912,
        "rank1.rx": 12582912,
        "rank1.tx": 12582912,
        "local.1->2": 12582912,
        "rank2.rx": 12582912,
        "rank2.tx": 12582912,
        "local.2->3": 12582912,
        "rank3.rx": 12582912,
        "rank3.tx": 12582912,
        "local.3->4": 12582912,
        "rank4.rx": 12582912,
        "rank4.tx": 12582912,
        "local.4->5": 12582912,
        "rank5.rx": 12582912,
        "rank5.tx": 12582912,
        "local.5->6": 12582912,
        "rank6.rx": 12582912,
        "rank6.tx": 12582912,
        "local.6->7": 12582912,
        "rank7.rx": 12582912,
        "rank7.tx": 12582912,
        "local.7->0": 12582912,
        "rank0.rx": 12582912,
        "rank8.tx": 12582912,
        "local.8->9": 12582912,
        "rank9.rx": 12582912,
        "rank9.tx": 12582912,
        "local.9->10": 12582912,
        "rank10.rx": 12582912,
        "rank10.tx": 12582912,
        "local.10->11": 12582912,
        "rank11.rx": 12582912,
        "rank11.tx": 12582912,
        "local.11->12": 12582912,
        "rank12.rx": 12582912,
        "rank12.tx": 12582912,
        "local.12->13": 12582912,
        "rank13.rx": 12582912,
        "rank13.tx": 12582912,
        "local.13->14": 12582912,
        "rank14.rx": 12582912,
        "rank14.tx": 12582912,
        "local.14->15": 12582912,
        "rank15.rx": 12582912,
        "rank15.tx": 12582912,
        "local.15->8": 12582912,
        "rank8.rx": 12582912
      },
      "resource_lower_seconds_exact": "4096/146484375",
      "barrier_lower_seconds_exact": "2159627/75000000000",
      "barrier_start_seconds_exact": "2159627/25000000000",
      "barrier_finish_seconds_exact": "2159627/18750000000"
    },
    {
      "round": 4,
      "stage": "local_reduce_scatter",
      "phase": "reduce_scatter",
      "step": 4,
      "messages": [
        {
          "sender": 0,
          "receiver": 1,
          "operation": "reduce",
          "chunks": [
            8,
            9
          ],
          "element_start": 25165824,
          "element_stop": 31457280,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 8,
              "contributors": [
                0,
                4,
                5,
                6,
                7
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                0,
                4,
                5,
                6,
                7
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r0:local",
              "receiver": "r1:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 25165824,
              "element_stop": 31457280,
              "path": [
                "rank0.tx",
                "local.0->1",
                "rank1.rx"
              ]
            }
          ]
        },
        {
          "sender": 1,
          "receiver": 2,
          "operation": "reduce",
          "chunks": [
            10,
            11
          ],
          "element_start": 31457280,
          "element_stop": 37748736,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 10,
              "contributors": [
                0,
                1,
                5,
                6,
                7
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                0,
                1,
                5,
                6,
                7
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r1:local",
              "receiver": "r2:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 31457280,
              "element_stop": 37748736,
              "path": [
                "rank1.tx",
                "local.1->2",
                "rank2.rx"
              ]
            }
          ]
        },
        {
          "sender": 2,
          "receiver": 3,
          "operation": "reduce",
          "chunks": [
            12,
            13
          ],
          "element_start": 37748736,
          "element_stop": 44040192,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 12,
              "contributors": [
                0,
                1,
                2,
                6,
                7
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                0,
                1,
                2,
                6,
                7
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r2:local",
              "receiver": "r3:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 37748736,
              "element_stop": 44040192,
              "path": [
                "rank2.tx",
                "local.2->3",
                "rank3.rx"
              ]
            }
          ]
        },
        {
          "sender": 3,
          "receiver": 4,
          "operation": "reduce",
          "chunks": [
            14,
            15
          ],
          "element_start": 44040192,
          "element_stop": 50331648,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 14,
              "contributors": [
                0,
                1,
                2,
                3,
                7
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                0,
                1,
                2,
                3,
                7
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r3:local",
              "receiver": "r4:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 44040192,
              "element_stop": 50331648,
              "path": [
                "rank3.tx",
                "local.3->4",
                "rank4.rx"
              ]
            }
          ]
        },
        {
          "sender": 4,
          "receiver": 5,
          "operation": "reduce",
          "chunks": [
            0,
            1
          ],
          "element_start": 0,
          "element_stop": 6291456,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 0,
              "contributors": [
                0,
                1,
                2,
                3,
                4
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                0,
                1,
                2,
                3,
                4
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r4:local",
              "receiver": "r5:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 0,
              "element_stop": 6291456,
              "path": [
                "rank4.tx",
                "local.4->5",
                "rank5.rx"
              ]
            }
          ]
        },
        {
          "sender": 5,
          "receiver": 6,
          "operation": "reduce",
          "chunks": [
            2,
            3
          ],
          "element_start": 6291456,
          "element_stop": 12582912,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 2,
              "contributors": [
                1,
                2,
                3,
                4,
                5
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                1,
                2,
                3,
                4,
                5
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r5:local",
              "receiver": "r6:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 6291456,
              "element_stop": 12582912,
              "path": [
                "rank5.tx",
                "local.5->6",
                "rank6.rx"
              ]
            }
          ]
        },
        {
          "sender": 6,
          "receiver": 7,
          "operation": "reduce",
          "chunks": [
            4,
            5
          ],
          "element_start": 12582912,
          "element_stop": 18874368,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 4,
              "contributors": [
                2,
                3,
                4,
                5,
                6
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                2,
                3,
                4,
                5,
                6
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r6:local",
              "receiver": "r7:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 12582912,
              "element_stop": 18874368,
              "path": [
                "rank6.tx",
                "local.6->7",
                "rank7.rx"
              ]
            }
          ]
        },
        {
          "sender": 7,
          "receiver": 0,
          "operation": "reduce",
          "chunks": [
            6,
            7
          ],
          "element_start": 18874368,
          "element_stop": 25165824,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 6,
              "contributors": [
                3,
                4,
                5,
                6,
                7
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                3,
                4,
                5,
                6,
                7
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r7:local",
              "receiver": "r0:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 18874368,
              "element_stop": 25165824,
              "path": [
                "rank7.tx",
                "local.7->0",
                "rank0.rx"
              ]
            }
          ]
        },
        {
          "sender": 8,
          "receiver": 9,
          "operation": "reduce",
          "chunks": [
            8,
            9
          ],
          "element_start": 25165824,
          "element_stop": 31457280,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 8,
              "contributors": [
                8,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                8,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r8:local",
              "receiver": "r9:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 25165824,
              "element_stop": 31457280,
              "path": [
                "rank8.tx",
                "local.8->9",
                "rank9.rx"
              ]
            }
          ]
        },
        {
          "sender": 9,
          "receiver": 10,
          "operation": "reduce",
          "chunks": [
            10,
            11
          ],
          "element_start": 31457280,
          "element_stop": 37748736,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 10,
              "contributors": [
                8,
                9,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                8,
                9,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r9:local",
              "receiver": "r10:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 31457280,
              "element_stop": 37748736,
              "path": [
                "rank9.tx",
                "local.9->10",
                "rank10.rx"
              ]
            }
          ]
        },
        {
          "sender": 10,
          "receiver": 11,
          "operation": "reduce",
          "chunks": [
            12,
            13
          ],
          "element_start": 37748736,
          "element_stop": 44040192,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 12,
              "contributors": [
                8,
                9,
                10,
                14,
                15
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                8,
                9,
                10,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r10:local",
              "receiver": "r11:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 37748736,
              "element_stop": 44040192,
              "path": [
                "rank10.tx",
                "local.10->11",
                "rank11.rx"
              ]
            }
          ]
        },
        {
          "sender": 11,
          "receiver": 12,
          "operation": "reduce",
          "chunks": [
            14,
            15
          ],
          "element_start": 44040192,
          "element_stop": 50331648,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 14,
              "contributors": [
                8,
                9,
                10,
                11,
                15
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                8,
                9,
                10,
                11,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r11:local",
              "receiver": "r12:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 44040192,
              "element_stop": 50331648,
              "path": [
                "rank11.tx",
                "local.11->12",
                "rank12.rx"
              ]
            }
          ]
        },
        {
          "sender": 12,
          "receiver": 13,
          "operation": "reduce",
          "chunks": [
            0,
            1
          ],
          "element_start": 0,
          "element_stop": 6291456,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 0,
              "contributors": [
                8,
                9,
                10,
                11,
                12
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                8,
                9,
                10,
                11,
                12
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r12:local",
              "receiver": "r13:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 0,
              "element_stop": 6291456,
              "path": [
                "rank12.tx",
                "local.12->13",
                "rank13.rx"
              ]
            }
          ]
        },
        {
          "sender": 13,
          "receiver": 14,
          "operation": "reduce",
          "chunks": [
            2,
            3
          ],
          "element_start": 6291456,
          "element_stop": 12582912,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 2,
              "contributors": [
                9,
                10,
                11,
                12,
                13
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                9,
                10,
                11,
                12,
                13
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r13:local",
              "receiver": "r14:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 6291456,
              "element_stop": 12582912,
              "path": [
                "rank13.tx",
                "local.13->14",
                "rank14.rx"
              ]
            }
          ]
        },
        {
          "sender": 14,
          "receiver": 15,
          "operation": "reduce",
          "chunks": [
            4,
            5
          ],
          "element_start": 12582912,
          "element_stop": 18874368,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 4,
              "contributors": [
                10,
                11,
                12,
                13,
                14
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                10,
                11,
                12,
                13,
                14
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r14:local",
              "receiver": "r15:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 12582912,
              "element_stop": 18874368,
              "path": [
                "rank14.tx",
                "local.14->15",
                "rank15.rx"
              ]
            }
          ]
        },
        {
          "sender": 15,
          "receiver": 8,
          "operation": "reduce",
          "chunks": [
            6,
            7
          ],
          "element_start": 18874368,
          "element_stop": 25165824,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 6,
              "contributors": [
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r15:local",
              "receiver": "r8:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 18874368,
              "element_stop": 25165824,
              "path": [
                "rank15.tx",
                "local.15->8",
                "rank8.rx"
              ]
            }
          ]
        }
      ],
      "edges": [
        {
          "sender": "r0:local",
          "receiver": "r1:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 25165824,
          "element_stop": 31457280,
          "path": [
            "rank0.tx",
            "local.0->1",
            "rank1.rx"
          ]
        },
        {
          "sender": "r1:local",
          "receiver": "r2:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 31457280,
          "element_stop": 37748736,
          "path": [
            "rank1.tx",
            "local.1->2",
            "rank2.rx"
          ]
        },
        {
          "sender": "r2:local",
          "receiver": "r3:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 37748736,
          "element_stop": 44040192,
          "path": [
            "rank2.tx",
            "local.2->3",
            "rank3.rx"
          ]
        },
        {
          "sender": "r3:local",
          "receiver": "r4:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 44040192,
          "element_stop": 50331648,
          "path": [
            "rank3.tx",
            "local.3->4",
            "rank4.rx"
          ]
        },
        {
          "sender": "r4:local",
          "receiver": "r5:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 0,
          "element_stop": 6291456,
          "path": [
            "rank4.tx",
            "local.4->5",
            "rank5.rx"
          ]
        },
        {
          "sender": "r5:local",
          "receiver": "r6:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 6291456,
          "element_stop": 12582912,
          "path": [
            "rank5.tx",
            "local.5->6",
            "rank6.rx"
          ]
        },
        {
          "sender": "r6:local",
          "receiver": "r7:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 12582912,
          "element_stop": 18874368,
          "path": [
            "rank6.tx",
            "local.6->7",
            "rank7.rx"
          ]
        },
        {
          "sender": "r7:local",
          "receiver": "r0:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 18874368,
          "element_stop": 25165824,
          "path": [
            "rank7.tx",
            "local.7->0",
            "rank0.rx"
          ]
        },
        {
          "sender": "r8:local",
          "receiver": "r9:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 25165824,
          "element_stop": 31457280,
          "path": [
            "rank8.tx",
            "local.8->9",
            "rank9.rx"
          ]
        },
        {
          "sender": "r9:local",
          "receiver": "r10:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 31457280,
          "element_stop": 37748736,
          "path": [
            "rank9.tx",
            "local.9->10",
            "rank10.rx"
          ]
        },
        {
          "sender": "r10:local",
          "receiver": "r11:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 37748736,
          "element_stop": 44040192,
          "path": [
            "rank10.tx",
            "local.10->11",
            "rank11.rx"
          ]
        },
        {
          "sender": "r11:local",
          "receiver": "r12:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 44040192,
          "element_stop": 50331648,
          "path": [
            "rank11.tx",
            "local.11->12",
            "rank12.rx"
          ]
        },
        {
          "sender": "r12:local",
          "receiver": "r13:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 0,
          "element_stop": 6291456,
          "path": [
            "rank12.tx",
            "local.12->13",
            "rank13.rx"
          ]
        },
        {
          "sender": "r13:local",
          "receiver": "r14:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 6291456,
          "element_stop": 12582912,
          "path": [
            "rank13.tx",
            "local.13->14",
            "rank14.rx"
          ]
        },
        {
          "sender": "r14:local",
          "receiver": "r15:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 12582912,
          "element_stop": 18874368,
          "path": [
            "rank14.tx",
            "local.14->15",
            "rank15.rx"
          ]
        },
        {
          "sender": "r15:local",
          "receiver": "r8:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 18874368,
          "element_stop": 25165824,
          "path": [
            "rank15.tx",
            "local.15->8",
            "rank8.rx"
          ]
        }
      ],
      "resource_bytes": {
        "rank0.tx": 12582912,
        "local.0->1": 12582912,
        "rank1.rx": 12582912,
        "rank1.tx": 12582912,
        "local.1->2": 12582912,
        "rank2.rx": 12582912,
        "rank2.tx": 12582912,
        "local.2->3": 12582912,
        "rank3.rx": 12582912,
        "rank3.tx": 12582912,
        "local.3->4": 12582912,
        "rank4.rx": 12582912,
        "rank4.tx": 12582912,
        "local.4->5": 12582912,
        "rank5.rx": 12582912,
        "rank5.tx": 12582912,
        "local.5->6": 12582912,
        "rank6.rx": 12582912,
        "rank6.tx": 12582912,
        "local.6->7": 12582912,
        "rank7.rx": 12582912,
        "rank7.tx": 12582912,
        "local.7->0": 12582912,
        "rank0.rx": 12582912,
        "rank8.tx": 12582912,
        "local.8->9": 12582912,
        "rank9.rx": 12582912,
        "rank9.tx": 12582912,
        "local.9->10": 12582912,
        "rank10.rx": 12582912,
        "rank10.tx": 12582912,
        "local.10->11": 12582912,
        "rank11.rx": 12582912,
        "rank11.tx": 12582912,
        "local.11->12": 12582912,
        "rank12.rx": 12582912,
        "rank12.tx": 12582912,
        "local.12->13": 12582912,
        "rank13.rx": 12582912,
        "rank13.tx": 12582912,
        "local.13->14": 12582912,
        "rank14.rx": 12582912,
        "rank14.tx": 12582912,
        "local.14->15": 12582912,
        "rank15.rx": 12582912,
        "rank15.tx": 12582912,
        "local.15->8": 12582912,
        "rank8.rx": 12582912
      },
      "resource_lower_seconds_exact": "4096/146484375",
      "barrier_lower_seconds_exact": "2159627/75000000000",
      "barrier_start_seconds_exact": "2159627/18750000000",
      "barrier_finish_seconds_exact": "2159627/15000000000"
    },
    {
      "round": 5,
      "stage": "local_reduce_scatter",
      "phase": "reduce_scatter",
      "step": 5,
      "messages": [
        {
          "sender": 0,
          "receiver": 1,
          "operation": "reduce",
          "chunks": [
            6,
            7
          ],
          "element_start": 18874368,
          "element_stop": 25165824,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 6,
              "contributors": [
                0,
                3,
                4,
                5,
                6,
                7
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                0,
                3,
                4,
                5,
                6,
                7
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r0:local",
              "receiver": "r1:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 18874368,
              "element_stop": 25165824,
              "path": [
                "rank0.tx",
                "local.0->1",
                "rank1.rx"
              ]
            }
          ]
        },
        {
          "sender": 1,
          "receiver": 2,
          "operation": "reduce",
          "chunks": [
            8,
            9
          ],
          "element_start": 25165824,
          "element_stop": 31457280,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 8,
              "contributors": [
                0,
                1,
                4,
                5,
                6,
                7
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                0,
                1,
                4,
                5,
                6,
                7
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r1:local",
              "receiver": "r2:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 25165824,
              "element_stop": 31457280,
              "path": [
                "rank1.tx",
                "local.1->2",
                "rank2.rx"
              ]
            }
          ]
        },
        {
          "sender": 2,
          "receiver": 3,
          "operation": "reduce",
          "chunks": [
            10,
            11
          ],
          "element_start": 31457280,
          "element_stop": 37748736,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 10,
              "contributors": [
                0,
                1,
                2,
                5,
                6,
                7
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                0,
                1,
                2,
                5,
                6,
                7
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r2:local",
              "receiver": "r3:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 31457280,
              "element_stop": 37748736,
              "path": [
                "rank2.tx",
                "local.2->3",
                "rank3.rx"
              ]
            }
          ]
        },
        {
          "sender": 3,
          "receiver": 4,
          "operation": "reduce",
          "chunks": [
            12,
            13
          ],
          "element_start": 37748736,
          "element_stop": 44040192,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 12,
              "contributors": [
                0,
                1,
                2,
                3,
                6,
                7
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                0,
                1,
                2,
                3,
                6,
                7
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r3:local",
              "receiver": "r4:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 37748736,
              "element_stop": 44040192,
              "path": [
                "rank3.tx",
                "local.3->4",
                "rank4.rx"
              ]
            }
          ]
        },
        {
          "sender": 4,
          "receiver": 5,
          "operation": "reduce",
          "chunks": [
            14,
            15
          ],
          "element_start": 44040192,
          "element_stop": 50331648,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 14,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                7
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                7
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r4:local",
              "receiver": "r5:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 44040192,
              "element_stop": 50331648,
              "path": [
                "rank4.tx",
                "local.4->5",
                "rank5.rx"
              ]
            }
          ]
        },
        {
          "sender": 5,
          "receiver": 6,
          "operation": "reduce",
          "chunks": [
            0,
            1
          ],
          "element_start": 0,
          "element_stop": 6291456,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 0,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r5:local",
              "receiver": "r6:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 0,
              "element_stop": 6291456,
              "path": [
                "rank5.tx",
                "local.5->6",
                "rank6.rx"
              ]
            }
          ]
        },
        {
          "sender": 6,
          "receiver": 7,
          "operation": "reduce",
          "chunks": [
            2,
            3
          ],
          "element_start": 6291456,
          "element_stop": 12582912,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 2,
              "contributors": [
                1,
                2,
                3,
                4,
                5,
                6
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                1,
                2,
                3,
                4,
                5,
                6
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r6:local",
              "receiver": "r7:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 6291456,
              "element_stop": 12582912,
              "path": [
                "rank6.tx",
                "local.6->7",
                "rank7.rx"
              ]
            }
          ]
        },
        {
          "sender": 7,
          "receiver": 0,
          "operation": "reduce",
          "chunks": [
            4,
            5
          ],
          "element_start": 12582912,
          "element_stop": 18874368,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 4,
              "contributors": [
                2,
                3,
                4,
                5,
                6,
                7
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                2,
                3,
                4,
                5,
                6,
                7
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r7:local",
              "receiver": "r0:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 12582912,
              "element_stop": 18874368,
              "path": [
                "rank7.tx",
                "local.7->0",
                "rank0.rx"
              ]
            }
          ]
        },
        {
          "sender": 8,
          "receiver": 9,
          "operation": "reduce",
          "chunks": [
            6,
            7
          ],
          "element_start": 18874368,
          "element_stop": 25165824,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 6,
              "contributors": [
                8,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                8,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r8:local",
              "receiver": "r9:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 18874368,
              "element_stop": 25165824,
              "path": [
                "rank8.tx",
                "local.8->9",
                "rank9.rx"
              ]
            }
          ]
        },
        {
          "sender": 9,
          "receiver": 10,
          "operation": "reduce",
          "chunks": [
            8,
            9
          ],
          "element_start": 25165824,
          "element_stop": 31457280,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 8,
              "contributors": [
                8,
                9,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                8,
                9,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r9:local",
              "receiver": "r10:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 25165824,
              "element_stop": 31457280,
              "path": [
                "rank9.tx",
                "local.9->10",
                "rank10.rx"
              ]
            }
          ]
        },
        {
          "sender": 10,
          "receiver": 11,
          "operation": "reduce",
          "chunks": [
            10,
            11
          ],
          "element_start": 31457280,
          "element_stop": 37748736,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 10,
              "contributors": [
                8,
                9,
                10,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                8,
                9,
                10,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r10:local",
              "receiver": "r11:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 31457280,
              "element_stop": 37748736,
              "path": [
                "rank10.tx",
                "local.10->11",
                "rank11.rx"
              ]
            }
          ]
        },
        {
          "sender": 11,
          "receiver": 12,
          "operation": "reduce",
          "chunks": [
            12,
            13
          ],
          "element_start": 37748736,
          "element_stop": 44040192,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 12,
              "contributors": [
                8,
                9,
                10,
                11,
                14,
                15
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                8,
                9,
                10,
                11,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r11:local",
              "receiver": "r12:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 37748736,
              "element_stop": 44040192,
              "path": [
                "rank11.tx",
                "local.11->12",
                "rank12.rx"
              ]
            }
          ]
        },
        {
          "sender": 12,
          "receiver": 13,
          "operation": "reduce",
          "chunks": [
            14,
            15
          ],
          "element_start": 44040192,
          "element_stop": 50331648,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 14,
              "contributors": [
                8,
                9,
                10,
                11,
                12,
                15
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                8,
                9,
                10,
                11,
                12,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r12:local",
              "receiver": "r13:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 44040192,
              "element_stop": 50331648,
              "path": [
                "rank12.tx",
                "local.12->13",
                "rank13.rx"
              ]
            }
          ]
        },
        {
          "sender": 13,
          "receiver": 14,
          "operation": "reduce",
          "chunks": [
            0,
            1
          ],
          "element_start": 0,
          "element_stop": 6291456,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 0,
              "contributors": [
                8,
                9,
                10,
                11,
                12,
                13
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                8,
                9,
                10,
                11,
                12,
                13
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r13:local",
              "receiver": "r14:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 0,
              "element_stop": 6291456,
              "path": [
                "rank13.tx",
                "local.13->14",
                "rank14.rx"
              ]
            }
          ]
        },
        {
          "sender": 14,
          "receiver": 15,
          "operation": "reduce",
          "chunks": [
            2,
            3
          ],
          "element_start": 6291456,
          "element_stop": 12582912,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 2,
              "contributors": [
                9,
                10,
                11,
                12,
                13,
                14
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                9,
                10,
                11,
                12,
                13,
                14
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r14:local",
              "receiver": "r15:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 6291456,
              "element_stop": 12582912,
              "path": [
                "rank14.tx",
                "local.14->15",
                "rank15.rx"
              ]
            }
          ]
        },
        {
          "sender": 15,
          "receiver": 8,
          "operation": "reduce",
          "chunks": [
            4,
            5
          ],
          "element_start": 12582912,
          "element_stop": 18874368,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 4,
              "contributors": [
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r15:local",
              "receiver": "r8:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 12582912,
              "element_stop": 18874368,
              "path": [
                "rank15.tx",
                "local.15->8",
                "rank8.rx"
              ]
            }
          ]
        }
      ],
      "edges": [
        {
          "sender": "r0:local",
          "receiver": "r1:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 18874368,
          "element_stop": 25165824,
          "path": [
            "rank0.tx",
            "local.0->1",
            "rank1.rx"
          ]
        },
        {
          "sender": "r1:local",
          "receiver": "r2:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 25165824,
          "element_stop": 31457280,
          "path": [
            "rank1.tx",
            "local.1->2",
            "rank2.rx"
          ]
        },
        {
          "sender": "r2:local",
          "receiver": "r3:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 31457280,
          "element_stop": 37748736,
          "path": [
            "rank2.tx",
            "local.2->3",
            "rank3.rx"
          ]
        },
        {
          "sender": "r3:local",
          "receiver": "r4:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 37748736,
          "element_stop": 44040192,
          "path": [
            "rank3.tx",
            "local.3->4",
            "rank4.rx"
          ]
        },
        {
          "sender": "r4:local",
          "receiver": "r5:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 44040192,
          "element_stop": 50331648,
          "path": [
            "rank4.tx",
            "local.4->5",
            "rank5.rx"
          ]
        },
        {
          "sender": "r5:local",
          "receiver": "r6:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 0,
          "element_stop": 6291456,
          "path": [
            "rank5.tx",
            "local.5->6",
            "rank6.rx"
          ]
        },
        {
          "sender": "r6:local",
          "receiver": "r7:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 6291456,
          "element_stop": 12582912,
          "path": [
            "rank6.tx",
            "local.6->7",
            "rank7.rx"
          ]
        },
        {
          "sender": "r7:local",
          "receiver": "r0:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 12582912,
          "element_stop": 18874368,
          "path": [
            "rank7.tx",
            "local.7->0",
            "rank0.rx"
          ]
        },
        {
          "sender": "r8:local",
          "receiver": "r9:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 18874368,
          "element_stop": 25165824,
          "path": [
            "rank8.tx",
            "local.8->9",
            "rank9.rx"
          ]
        },
        {
          "sender": "r9:local",
          "receiver": "r10:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 25165824,
          "element_stop": 31457280,
          "path": [
            "rank9.tx",
            "local.9->10",
            "rank10.rx"
          ]
        },
        {
          "sender": "r10:local",
          "receiver": "r11:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 31457280,
          "element_stop": 37748736,
          "path": [
            "rank10.tx",
            "local.10->11",
            "rank11.rx"
          ]
        },
        {
          "sender": "r11:local",
          "receiver": "r12:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 37748736,
          "element_stop": 44040192,
          "path": [
            "rank11.tx",
            "local.11->12",
            "rank12.rx"
          ]
        },
        {
          "sender": "r12:local",
          "receiver": "r13:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 44040192,
          "element_stop": 50331648,
          "path": [
            "rank12.tx",
            "local.12->13",
            "rank13.rx"
          ]
        },
        {
          "sender": "r13:local",
          "receiver": "r14:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 0,
          "element_stop": 6291456,
          "path": [
            "rank13.tx",
            "local.13->14",
            "rank14.rx"
          ]
        },
        {
          "sender": "r14:local",
          "receiver": "r15:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 6291456,
          "element_stop": 12582912,
          "path": [
            "rank14.tx",
            "local.14->15",
            "rank15.rx"
          ]
        },
        {
          "sender": "r15:local",
          "receiver": "r8:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 12582912,
          "element_stop": 18874368,
          "path": [
            "rank15.tx",
            "local.15->8",
            "rank8.rx"
          ]
        }
      ],
      "resource_bytes": {
        "rank0.tx": 12582912,
        "local.0->1": 12582912,
        "rank1.rx": 12582912,
        "rank1.tx": 12582912,
        "local.1->2": 12582912,
        "rank2.rx": 12582912,
        "rank2.tx": 12582912,
        "local.2->3": 12582912,
        "rank3.rx": 12582912,
        "rank3.tx": 12582912,
        "local.3->4": 12582912,
        "rank4.rx": 12582912,
        "rank4.tx": 12582912,
        "local.4->5": 12582912,
        "rank5.rx": 12582912,
        "rank5.tx": 12582912,
        "local.5->6": 12582912,
        "rank6.rx": 12582912,
        "rank6.tx": 12582912,
        "local.6->7": 12582912,
        "rank7.rx": 12582912,
        "rank7.tx": 12582912,
        "local.7->0": 12582912,
        "rank0.rx": 12582912,
        "rank8.tx": 12582912,
        "local.8->9": 12582912,
        "rank9.rx": 12582912,
        "rank9.tx": 12582912,
        "local.9->10": 12582912,
        "rank10.rx": 12582912,
        "rank10.tx": 12582912,
        "local.10->11": 12582912,
        "rank11.rx": 12582912,
        "rank11.tx": 12582912,
        "local.11->12": 12582912,
        "rank12.rx": 12582912,
        "rank12.tx": 12582912,
        "local.12->13": 12582912,
        "rank13.rx": 12582912,
        "rank13.tx": 12582912,
        "local.13->14": 12582912,
        "rank14.rx": 12582912,
        "rank14.tx": 12582912,
        "local.14->15": 12582912,
        "rank15.rx": 12582912,
        "rank15.tx": 12582912,
        "local.15->8": 12582912,
        "rank8.rx": 12582912
      },
      "resource_lower_seconds_exact": "4096/146484375",
      "barrier_lower_seconds_exact": "2159627/75000000000",
      "barrier_start_seconds_exact": "2159627/15000000000",
      "barrier_finish_seconds_exact": "2159627/12500000000"
    },
    {
      "round": 6,
      "stage": "local_reduce_scatter",
      "phase": "reduce_scatter",
      "step": 6,
      "messages": [
        {
          "sender": 0,
          "receiver": 1,
          "operation": "reduce",
          "chunks": [
            4,
            5
          ],
          "element_start": 12582912,
          "element_stop": 18874368,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 4,
              "contributors": [
                0,
                2,
                3,
                4,
                5,
                6,
                7
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                0,
                2,
                3,
                4,
                5,
                6,
                7
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r0:local",
              "receiver": "r1:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 12582912,
              "element_stop": 18874368,
              "path": [
                "rank0.tx",
                "local.0->1",
                "rank1.rx"
              ]
            }
          ]
        },
        {
          "sender": 1,
          "receiver": 2,
          "operation": "reduce",
          "chunks": [
            6,
            7
          ],
          "element_start": 18874368,
          "element_stop": 25165824,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 6,
              "contributors": [
                0,
                1,
                3,
                4,
                5,
                6,
                7
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                0,
                1,
                3,
                4,
                5,
                6,
                7
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r1:local",
              "receiver": "r2:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 18874368,
              "element_stop": 25165824,
              "path": [
                "rank1.tx",
                "local.1->2",
                "rank2.rx"
              ]
            }
          ]
        },
        {
          "sender": 2,
          "receiver": 3,
          "operation": "reduce",
          "chunks": [
            8,
            9
          ],
          "element_start": 25165824,
          "element_stop": 31457280,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 8,
              "contributors": [
                0,
                1,
                2,
                4,
                5,
                6,
                7
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                0,
                1,
                2,
                4,
                5,
                6,
                7
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r2:local",
              "receiver": "r3:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 25165824,
              "element_stop": 31457280,
              "path": [
                "rank2.tx",
                "local.2->3",
                "rank3.rx"
              ]
            }
          ]
        },
        {
          "sender": 3,
          "receiver": 4,
          "operation": "reduce",
          "chunks": [
            10,
            11
          ],
          "element_start": 31457280,
          "element_stop": 37748736,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 10,
              "contributors": [
                0,
                1,
                2,
                3,
                5,
                6,
                7
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                0,
                1,
                2,
                3,
                5,
                6,
                7
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r3:local",
              "receiver": "r4:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 31457280,
              "element_stop": 37748736,
              "path": [
                "rank3.tx",
                "local.3->4",
                "rank4.rx"
              ]
            }
          ]
        },
        {
          "sender": 4,
          "receiver": 5,
          "operation": "reduce",
          "chunks": [
            12,
            13
          ],
          "element_start": 37748736,
          "element_stop": 44040192,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 12,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                6,
                7
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                6,
                7
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r4:local",
              "receiver": "r5:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 37748736,
              "element_stop": 44040192,
              "path": [
                "rank4.tx",
                "local.4->5",
                "rank5.rx"
              ]
            }
          ]
        },
        {
          "sender": 5,
          "receiver": 6,
          "operation": "reduce",
          "chunks": [
            14,
            15
          ],
          "element_start": 44040192,
          "element_stop": 50331648,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 14,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                7
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                7
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r5:local",
              "receiver": "r6:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 44040192,
              "element_stop": 50331648,
              "path": [
                "rank5.tx",
                "local.5->6",
                "rank6.rx"
              ]
            }
          ]
        },
        {
          "sender": 6,
          "receiver": 7,
          "operation": "reduce",
          "chunks": [
            0,
            1
          ],
          "element_start": 0,
          "element_stop": 6291456,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 0,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r6:local",
              "receiver": "r7:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 0,
              "element_stop": 6291456,
              "path": [
                "rank6.tx",
                "local.6->7",
                "rank7.rx"
              ]
            }
          ]
        },
        {
          "sender": 7,
          "receiver": 0,
          "operation": "reduce",
          "chunks": [
            2,
            3
          ],
          "element_start": 6291456,
          "element_stop": 12582912,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 2,
              "contributors": [
                1,
                2,
                3,
                4,
                5,
                6,
                7
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                1,
                2,
                3,
                4,
                5,
                6,
                7
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r7:local",
              "receiver": "r0:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 6291456,
              "element_stop": 12582912,
              "path": [
                "rank7.tx",
                "local.7->0",
                "rank0.rx"
              ]
            }
          ]
        },
        {
          "sender": 8,
          "receiver": 9,
          "operation": "reduce",
          "chunks": [
            4,
            5
          ],
          "element_start": 12582912,
          "element_stop": 18874368,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 4,
              "contributors": [
                8,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                8,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r8:local",
              "receiver": "r9:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 12582912,
              "element_stop": 18874368,
              "path": [
                "rank8.tx",
                "local.8->9",
                "rank9.rx"
              ]
            }
          ]
        },
        {
          "sender": 9,
          "receiver": 10,
          "operation": "reduce",
          "chunks": [
            6,
            7
          ],
          "element_start": 18874368,
          "element_stop": 25165824,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 6,
              "contributors": [
                8,
                9,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                8,
                9,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r9:local",
              "receiver": "r10:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 18874368,
              "element_stop": 25165824,
              "path": [
                "rank9.tx",
                "local.9->10",
                "rank10.rx"
              ]
            }
          ]
        },
        {
          "sender": 10,
          "receiver": 11,
          "operation": "reduce",
          "chunks": [
            8,
            9
          ],
          "element_start": 25165824,
          "element_stop": 31457280,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 8,
              "contributors": [
                8,
                9,
                10,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                8,
                9,
                10,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r10:local",
              "receiver": "r11:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 25165824,
              "element_stop": 31457280,
              "path": [
                "rank10.tx",
                "local.10->11",
                "rank11.rx"
              ]
            }
          ]
        },
        {
          "sender": 11,
          "receiver": 12,
          "operation": "reduce",
          "chunks": [
            10,
            11
          ],
          "element_start": 31457280,
          "element_stop": 37748736,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 10,
              "contributors": [
                8,
                9,
                10,
                11,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                8,
                9,
                10,
                11,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r11:local",
              "receiver": "r12:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 31457280,
              "element_stop": 37748736,
              "path": [
                "rank11.tx",
                "local.11->12",
                "rank12.rx"
              ]
            }
          ]
        },
        {
          "sender": 12,
          "receiver": 13,
          "operation": "reduce",
          "chunks": [
            12,
            13
          ],
          "element_start": 37748736,
          "element_stop": 44040192,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 12,
              "contributors": [
                8,
                9,
                10,
                11,
                12,
                14,
                15
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                8,
                9,
                10,
                11,
                12,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r12:local",
              "receiver": "r13:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 37748736,
              "element_stop": 44040192,
              "path": [
                "rank12.tx",
                "local.12->13",
                "rank13.rx"
              ]
            }
          ]
        },
        {
          "sender": 13,
          "receiver": 14,
          "operation": "reduce",
          "chunks": [
            14,
            15
          ],
          "element_start": 44040192,
          "element_stop": 50331648,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 14,
              "contributors": [
                8,
                9,
                10,
                11,
                12,
                13,
                15
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                8,
                9,
                10,
                11,
                12,
                13,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r13:local",
              "receiver": "r14:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 44040192,
              "element_stop": 50331648,
              "path": [
                "rank13.tx",
                "local.13->14",
                "rank14.rx"
              ]
            }
          ]
        },
        {
          "sender": 14,
          "receiver": 15,
          "operation": "reduce",
          "chunks": [
            0,
            1
          ],
          "element_start": 0,
          "element_stop": 6291456,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 0,
              "contributors": [
                8,
                9,
                10,
                11,
                12,
                13,
                14
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                8,
                9,
                10,
                11,
                12,
                13,
                14
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r14:local",
              "receiver": "r15:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 0,
              "element_stop": 6291456,
              "path": [
                "rank14.tx",
                "local.14->15",
                "rank15.rx"
              ]
            }
          ]
        },
        {
          "sender": 15,
          "receiver": 8,
          "operation": "reduce",
          "chunks": [
            2,
            3
          ],
          "element_start": 6291456,
          "element_stop": 12582912,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 2,
              "contributors": [
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r15:local",
              "receiver": "r8:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 6291456,
              "element_stop": 12582912,
              "path": [
                "rank15.tx",
                "local.15->8",
                "rank8.rx"
              ]
            }
          ]
        }
      ],
      "edges": [
        {
          "sender": "r0:local",
          "receiver": "r1:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 12582912,
          "element_stop": 18874368,
          "path": [
            "rank0.tx",
            "local.0->1",
            "rank1.rx"
          ]
        },
        {
          "sender": "r1:local",
          "receiver": "r2:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 18874368,
          "element_stop": 25165824,
          "path": [
            "rank1.tx",
            "local.1->2",
            "rank2.rx"
          ]
        },
        {
          "sender": "r2:local",
          "receiver": "r3:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 25165824,
          "element_stop": 31457280,
          "path": [
            "rank2.tx",
            "local.2->3",
            "rank3.rx"
          ]
        },
        {
          "sender": "r3:local",
          "receiver": "r4:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 31457280,
          "element_stop": 37748736,
          "path": [
            "rank3.tx",
            "local.3->4",
            "rank4.rx"
          ]
        },
        {
          "sender": "r4:local",
          "receiver": "r5:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 37748736,
          "element_stop": 44040192,
          "path": [
            "rank4.tx",
            "local.4->5",
            "rank5.rx"
          ]
        },
        {
          "sender": "r5:local",
          "receiver": "r6:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 44040192,
          "element_stop": 50331648,
          "path": [
            "rank5.tx",
            "local.5->6",
            "rank6.rx"
          ]
        },
        {
          "sender": "r6:local",
          "receiver": "r7:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 0,
          "element_stop": 6291456,
          "path": [
            "rank6.tx",
            "local.6->7",
            "rank7.rx"
          ]
        },
        {
          "sender": "r7:local",
          "receiver": "r0:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 6291456,
          "element_stop": 12582912,
          "path": [
            "rank7.tx",
            "local.7->0",
            "rank0.rx"
          ]
        },
        {
          "sender": "r8:local",
          "receiver": "r9:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 12582912,
          "element_stop": 18874368,
          "path": [
            "rank8.tx",
            "local.8->9",
            "rank9.rx"
          ]
        },
        {
          "sender": "r9:local",
          "receiver": "r10:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 18874368,
          "element_stop": 25165824,
          "path": [
            "rank9.tx",
            "local.9->10",
            "rank10.rx"
          ]
        },
        {
          "sender": "r10:local",
          "receiver": "r11:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 25165824,
          "element_stop": 31457280,
          "path": [
            "rank10.tx",
            "local.10->11",
            "rank11.rx"
          ]
        },
        {
          "sender": "r11:local",
          "receiver": "r12:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 31457280,
          "element_stop": 37748736,
          "path": [
            "rank11.tx",
            "local.11->12",
            "rank12.rx"
          ]
        },
        {
          "sender": "r12:local",
          "receiver": "r13:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 37748736,
          "element_stop": 44040192,
          "path": [
            "rank12.tx",
            "local.12->13",
            "rank13.rx"
          ]
        },
        {
          "sender": "r13:local",
          "receiver": "r14:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 44040192,
          "element_stop": 50331648,
          "path": [
            "rank13.tx",
            "local.13->14",
            "rank14.rx"
          ]
        },
        {
          "sender": "r14:local",
          "receiver": "r15:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 0,
          "element_stop": 6291456,
          "path": [
            "rank14.tx",
            "local.14->15",
            "rank15.rx"
          ]
        },
        {
          "sender": "r15:local",
          "receiver": "r8:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 6291456,
          "element_stop": 12582912,
          "path": [
            "rank15.tx",
            "local.15->8",
            "rank8.rx"
          ]
        }
      ],
      "resource_bytes": {
        "rank0.tx": 12582912,
        "local.0->1": 12582912,
        "rank1.rx": 12582912,
        "rank1.tx": 12582912,
        "local.1->2": 12582912,
        "rank2.rx": 12582912,
        "rank2.tx": 12582912,
        "local.2->3": 12582912,
        "rank3.rx": 12582912,
        "rank3.tx": 12582912,
        "local.3->4": 12582912,
        "rank4.rx": 12582912,
        "rank4.tx": 12582912,
        "local.4->5": 12582912,
        "rank5.rx": 12582912,
        "rank5.tx": 12582912,
        "local.5->6": 12582912,
        "rank6.rx": 12582912,
        "rank6.tx": 12582912,
        "local.6->7": 12582912,
        "rank7.rx": 12582912,
        "rank7.tx": 12582912,
        "local.7->0": 12582912,
        "rank0.rx": 12582912,
        "rank8.tx": 12582912,
        "local.8->9": 12582912,
        "rank9.rx": 12582912,
        "rank9.tx": 12582912,
        "local.9->10": 12582912,
        "rank10.rx": 12582912,
        "rank10.tx": 12582912,
        "local.10->11": 12582912,
        "rank11.rx": 12582912,
        "rank11.tx": 12582912,
        "local.11->12": 12582912,
        "rank12.rx": 12582912,
        "rank12.tx": 12582912,
        "local.12->13": 12582912,
        "rank13.rx": 12582912,
        "rank13.tx": 12582912,
        "local.13->14": 12582912,
        "rank14.rx": 12582912,
        "rank14.tx": 12582912,
        "local.14->15": 12582912,
        "rank15.rx": 12582912,
        "rank15.tx": 12582912,
        "local.15->8": 12582912,
        "rank8.rx": 12582912
      },
      "resource_lower_seconds_exact": "4096/146484375",
      "barrier_lower_seconds_exact": "2159627/75000000000",
      "barrier_start_seconds_exact": "2159627/12500000000",
      "barrier_finish_seconds_exact": "15117389/75000000000"
    },
    {
      "round": 7,
      "stage": "cross_server_allreduce",
      "phase": "reduce_scatter",
      "step": 0,
      "messages": [
        {
          "sender": 7,
          "receiver": 15,
          "operation": "reduce",
          "chunks": [
            0
          ],
          "element_start": 0,
          "element_stop": 3145728,
          "bytes": 6291456,
          "contributions": [
            {
              "chunk": 0,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7
              ]
            }
          ],
          "remote": true,
          "stripes": [
            {
              "sender": "r7:nic7",
              "receiver": "r15:nic7",
              "bytes": 6291456,
              "nic": 7,
              "element_start": 0,
              "element_stop": 3145728,
              "path": [
                "rank7.tx",
                "server0.nic7.tx",
                "cut.0->1",
                "shared_cut.bidirectional",
                "server1.nic7.rx",
                "rank15.rx"
              ]
            }
          ]
        },
        {
          "sender": 15,
          "receiver": 7,
          "operation": "reduce",
          "chunks": [
            1
          ],
          "element_start": 3145728,
          "element_stop": 6291456,
          "bytes": 6291456,
          "contributions": [
            {
              "chunk": 1,
              "contributors": [
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": true,
          "stripes": [
            {
              "sender": "r15:nic7",
              "receiver": "r7:nic7",
              "bytes": 6291456,
              "nic": 7,
              "element_start": 3145728,
              "element_stop": 6291456,
              "path": [
                "rank15.tx",
                "server1.nic7.tx",
                "cut.1->0",
                "shared_cut.bidirectional",
                "server0.nic7.rx",
                "rank7.rx"
              ]
            }
          ]
        },
        {
          "sender": 0,
          "receiver": 8,
          "operation": "reduce",
          "chunks": [
            2
          ],
          "element_start": 6291456,
          "element_stop": 9437184,
          "bytes": 6291456,
          "contributions": [
            {
              "chunk": 2,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7
              ]
            }
          ],
          "remote": true,
          "stripes": [
            {
              "sender": "r0:nic0",
              "receiver": "r8:nic0",
              "bytes": 6291456,
              "nic": 0,
              "element_start": 6291456,
              "element_stop": 9437184,
              "path": [
                "rank0.tx",
                "server0.nic0.tx",
                "cut.0->1",
                "shared_cut.bidirectional",
                "server1.nic0.rx",
                "rank8.rx"
              ]
            }
          ]
        },
        {
          "sender": 8,
          "receiver": 0,
          "operation": "reduce",
          "chunks": [
            3
          ],
          "element_start": 9437184,
          "element_stop": 12582912,
          "bytes": 6291456,
          "contributions": [
            {
              "chunk": 3,
              "contributors": [
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": true,
          "stripes": [
            {
              "sender": "r8:nic0",
              "receiver": "r0:nic0",
              "bytes": 6291456,
              "nic": 0,
              "element_start": 9437184,
              "element_stop": 12582912,
              "path": [
                "rank8.tx",
                "server1.nic0.tx",
                "cut.1->0",
                "shared_cut.bidirectional",
                "server0.nic0.rx",
                "rank0.rx"
              ]
            }
          ]
        },
        {
          "sender": 1,
          "receiver": 9,
          "operation": "reduce",
          "chunks": [
            4
          ],
          "element_start": 12582912,
          "element_stop": 15728640,
          "bytes": 6291456,
          "contributions": [
            {
              "chunk": 4,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7
              ]
            }
          ],
          "remote": true,
          "stripes": [
            {
              "sender": "r1:nic1",
              "receiver": "r9:nic1",
              "bytes": 6291456,
              "nic": 1,
              "element_start": 12582912,
              "element_stop": 15728640,
              "path": [
                "rank1.tx",
                "server0.nic1.tx",
                "cut.0->1",
                "shared_cut.bidirectional",
                "server1.nic1.rx",
                "rank9.rx"
              ]
            }
          ]
        },
        {
          "sender": 9,
          "receiver": 1,
          "operation": "reduce",
          "chunks": [
            5
          ],
          "element_start": 15728640,
          "element_stop": 18874368,
          "bytes": 6291456,
          "contributions": [
            {
              "chunk": 5,
              "contributors": [
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": true,
          "stripes": [
            {
              "sender": "r9:nic1",
              "receiver": "r1:nic1",
              "bytes": 6291456,
              "nic": 1,
              "element_start": 15728640,
              "element_stop": 18874368,
              "path": [
                "rank9.tx",
                "server1.nic1.tx",
                "cut.1->0",
                "shared_cut.bidirectional",
                "server0.nic1.rx",
                "rank1.rx"
              ]
            }
          ]
        },
        {
          "sender": 2,
          "receiver": 10,
          "operation": "reduce",
          "chunks": [
            6
          ],
          "element_start": 18874368,
          "element_stop": 22020096,
          "bytes": 6291456,
          "contributions": [
            {
              "chunk": 6,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7
              ]
            }
          ],
          "remote": true,
          "stripes": [
            {
              "sender": "r2:nic2",
              "receiver": "r10:nic2",
              "bytes": 6291456,
              "nic": 2,
              "element_start": 18874368,
              "element_stop": 22020096,
              "path": [
                "rank2.tx",
                "server0.nic2.tx",
                "cut.0->1",
                "shared_cut.bidirectional",
                "server1.nic2.rx",
                "rank10.rx"
              ]
            }
          ]
        },
        {
          "sender": 10,
          "receiver": 2,
          "operation": "reduce",
          "chunks": [
            7
          ],
          "element_start": 22020096,
          "element_stop": 25165824,
          "bytes": 6291456,
          "contributions": [
            {
              "chunk": 7,
              "contributors": [
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": true,
          "stripes": [
            {
              "sender": "r10:nic2",
              "receiver": "r2:nic2",
              "bytes": 6291456,
              "nic": 2,
              "element_start": 22020096,
              "element_stop": 25165824,
              "path": [
                "rank10.tx",
                "server1.nic2.tx",
                "cut.1->0",
                "shared_cut.bidirectional",
                "server0.nic2.rx",
                "rank2.rx"
              ]
            }
          ]
        },
        {
          "sender": 3,
          "receiver": 11,
          "operation": "reduce",
          "chunks": [
            8
          ],
          "element_start": 25165824,
          "element_stop": 28311552,
          "bytes": 6291456,
          "contributions": [
            {
              "chunk": 8,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7
              ]
            }
          ],
          "remote": true,
          "stripes": [
            {
              "sender": "r3:nic3",
              "receiver": "r11:nic3",
              "bytes": 6291456,
              "nic": 3,
              "element_start": 25165824,
              "element_stop": 28311552,
              "path": [
                "rank3.tx",
                "server0.nic3.tx",
                "cut.0->1",
                "shared_cut.bidirectional",
                "server1.nic3.rx",
                "rank11.rx"
              ]
            }
          ]
        },
        {
          "sender": 11,
          "receiver": 3,
          "operation": "reduce",
          "chunks": [
            9
          ],
          "element_start": 28311552,
          "element_stop": 31457280,
          "bytes": 6291456,
          "contributions": [
            {
              "chunk": 9,
              "contributors": [
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": true,
          "stripes": [
            {
              "sender": "r11:nic3",
              "receiver": "r3:nic3",
              "bytes": 6291456,
              "nic": 3,
              "element_start": 28311552,
              "element_stop": 31457280,
              "path": [
                "rank11.tx",
                "server1.nic3.tx",
                "cut.1->0",
                "shared_cut.bidirectional",
                "server0.nic3.rx",
                "rank3.rx"
              ]
            }
          ]
        },
        {
          "sender": 4,
          "receiver": 12,
          "operation": "reduce",
          "chunks": [
            10
          ],
          "element_start": 31457280,
          "element_stop": 34603008,
          "bytes": 6291456,
          "contributions": [
            {
              "chunk": 10,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7
              ]
            }
          ],
          "remote": true,
          "stripes": [
            {
              "sender": "r4:nic4",
              "receiver": "r12:nic4",
              "bytes": 6291456,
              "nic": 4,
              "element_start": 31457280,
              "element_stop": 34603008,
              "path": [
                "rank4.tx",
                "server0.nic4.tx",
                "cut.0->1",
                "shared_cut.bidirectional",
                "server1.nic4.rx",
                "rank12.rx"
              ]
            }
          ]
        },
        {
          "sender": 12,
          "receiver": 4,
          "operation": "reduce",
          "chunks": [
            11
          ],
          "element_start": 34603008,
          "element_stop": 37748736,
          "bytes": 6291456,
          "contributions": [
            {
              "chunk": 11,
              "contributors": [
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": true,
          "stripes": [
            {
              "sender": "r12:nic4",
              "receiver": "r4:nic4",
              "bytes": 6291456,
              "nic": 4,
              "element_start": 34603008,
              "element_stop": 37748736,
              "path": [
                "rank12.tx",
                "server1.nic4.tx",
                "cut.1->0",
                "shared_cut.bidirectional",
                "server0.nic4.rx",
                "rank4.rx"
              ]
            }
          ]
        },
        {
          "sender": 5,
          "receiver": 13,
          "operation": "reduce",
          "chunks": [
            12
          ],
          "element_start": 37748736,
          "element_stop": 40894464,
          "bytes": 6291456,
          "contributions": [
            {
              "chunk": 12,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7
              ]
            }
          ],
          "remote": true,
          "stripes": [
            {
              "sender": "r5:nic5",
              "receiver": "r13:nic5",
              "bytes": 6291456,
              "nic": 5,
              "element_start": 37748736,
              "element_stop": 40894464,
              "path": [
                "rank5.tx",
                "server0.nic5.tx",
                "cut.0->1",
                "shared_cut.bidirectional",
                "server1.nic5.rx",
                "rank13.rx"
              ]
            }
          ]
        },
        {
          "sender": 13,
          "receiver": 5,
          "operation": "reduce",
          "chunks": [
            13
          ],
          "element_start": 40894464,
          "element_stop": 44040192,
          "bytes": 6291456,
          "contributions": [
            {
              "chunk": 13,
              "contributors": [
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": true,
          "stripes": [
            {
              "sender": "r13:nic5",
              "receiver": "r5:nic5",
              "bytes": 6291456,
              "nic": 5,
              "element_start": 40894464,
              "element_stop": 44040192,
              "path": [
                "rank13.tx",
                "server1.nic5.tx",
                "cut.1->0",
                "shared_cut.bidirectional",
                "server0.nic5.rx",
                "rank5.rx"
              ]
            }
          ]
        },
        {
          "sender": 6,
          "receiver": 14,
          "operation": "reduce",
          "chunks": [
            14
          ],
          "element_start": 44040192,
          "element_stop": 47185920,
          "bytes": 6291456,
          "contributions": [
            {
              "chunk": 14,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7
              ]
            }
          ],
          "remote": true,
          "stripes": [
            {
              "sender": "r6:nic6",
              "receiver": "r14:nic6",
              "bytes": 6291456,
              "nic": 6,
              "element_start": 44040192,
              "element_stop": 47185920,
              "path": [
                "rank6.tx",
                "server0.nic6.tx",
                "cut.0->1",
                "shared_cut.bidirectional",
                "server1.nic6.rx",
                "rank14.rx"
              ]
            }
          ]
        },
        {
          "sender": 14,
          "receiver": 6,
          "operation": "reduce",
          "chunks": [
            15
          ],
          "element_start": 47185920,
          "element_stop": 50331648,
          "bytes": 6291456,
          "contributions": [
            {
              "chunk": 15,
              "contributors": [
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": true,
          "stripes": [
            {
              "sender": "r14:nic6",
              "receiver": "r6:nic6",
              "bytes": 6291456,
              "nic": 6,
              "element_start": 47185920,
              "element_stop": 50331648,
              "path": [
                "rank14.tx",
                "server1.nic6.tx",
                "cut.1->0",
                "shared_cut.bidirectional",
                "server0.nic6.rx",
                "rank6.rx"
              ]
            }
          ]
        }
      ],
      "edges": [
        {
          "sender": "r7:nic7",
          "receiver": "r15:nic7",
          "bytes": 6291456,
          "nic": 7,
          "element_start": 0,
          "element_stop": 3145728,
          "path": [
            "rank7.tx",
            "server0.nic7.tx",
            "cut.0->1",
            "shared_cut.bidirectional",
            "server1.nic7.rx",
            "rank15.rx"
          ]
        },
        {
          "sender": "r15:nic7",
          "receiver": "r7:nic7",
          "bytes": 6291456,
          "nic": 7,
          "element_start": 3145728,
          "element_stop": 6291456,
          "path": [
            "rank15.tx",
            "server1.nic7.tx",
            "cut.1->0",
            "shared_cut.bidirectional",
            "server0.nic7.rx",
            "rank7.rx"
          ]
        },
        {
          "sender": "r0:nic0",
          "receiver": "r8:nic0",
          "bytes": 6291456,
          "nic": 0,
          "element_start": 6291456,
          "element_stop": 9437184,
          "path": [
            "rank0.tx",
            "server0.nic0.tx",
            "cut.0->1",
            "shared_cut.bidirectional",
            "server1.nic0.rx",
            "rank8.rx"
          ]
        },
        {
          "sender": "r8:nic0",
          "receiver": "r0:nic0",
          "bytes": 6291456,
          "nic": 0,
          "element_start": 9437184,
          "element_stop": 12582912,
          "path": [
            "rank8.tx",
            "server1.nic0.tx",
            "cut.1->0",
            "shared_cut.bidirectional",
            "server0.nic0.rx",
            "rank0.rx"
          ]
        },
        {
          "sender": "r1:nic1",
          "receiver": "r9:nic1",
          "bytes": 6291456,
          "nic": 1,
          "element_start": 12582912,
          "element_stop": 15728640,
          "path": [
            "rank1.tx",
            "server0.nic1.tx",
            "cut.0->1",
            "shared_cut.bidirectional",
            "server1.nic1.rx",
            "rank9.rx"
          ]
        },
        {
          "sender": "r9:nic1",
          "receiver": "r1:nic1",
          "bytes": 6291456,
          "nic": 1,
          "element_start": 15728640,
          "element_stop": 18874368,
          "path": [
            "rank9.tx",
            "server1.nic1.tx",
            "cut.1->0",
            "shared_cut.bidirectional",
            "server0.nic1.rx",
            "rank1.rx"
          ]
        },
        {
          "sender": "r2:nic2",
          "receiver": "r10:nic2",
          "bytes": 6291456,
          "nic": 2,
          "element_start": 18874368,
          "element_stop": 22020096,
          "path": [
            "rank2.tx",
            "server0.nic2.tx",
            "cut.0->1",
            "shared_cut.bidirectional",
            "server1.nic2.rx",
            "rank10.rx"
          ]
        },
        {
          "sender": "r10:nic2",
          "receiver": "r2:nic2",
          "bytes": 6291456,
          "nic": 2,
          "element_start": 22020096,
          "element_stop": 25165824,
          "path": [
            "rank10.tx",
            "server1.nic2.tx",
            "cut.1->0",
            "shared_cut.bidirectional",
            "server0.nic2.rx",
            "rank2.rx"
          ]
        },
        {
          "sender": "r3:nic3",
          "receiver": "r11:nic3",
          "bytes": 6291456,
          "nic": 3,
          "element_start": 25165824,
          "element_stop": 28311552,
          "path": [
            "rank3.tx",
            "server0.nic3.tx",
            "cut.0->1",
            "shared_cut.bidirectional",
            "server1.nic3.rx",
            "rank11.rx"
          ]
        },
        {
          "sender": "r11:nic3",
          "receiver": "r3:nic3",
          "bytes": 6291456,
          "nic": 3,
          "element_start": 28311552,
          "element_stop": 31457280,
          "path": [
            "rank11.tx",
            "server1.nic3.tx",
            "cut.1->0",
            "shared_cut.bidirectional",
            "server0.nic3.rx",
            "rank3.rx"
          ]
        },
        {
          "sender": "r4:nic4",
          "receiver": "r12:nic4",
          "bytes": 6291456,
          "nic": 4,
          "element_start": 31457280,
          "element_stop": 34603008,
          "path": [
            "rank4.tx",
            "server0.nic4.tx",
            "cut.0->1",
            "shared_cut.bidirectional",
            "server1.nic4.rx",
            "rank12.rx"
          ]
        },
        {
          "sender": "r12:nic4",
          "receiver": "r4:nic4",
          "bytes": 6291456,
          "nic": 4,
          "element_start": 34603008,
          "element_stop": 37748736,
          "path": [
            "rank12.tx",
            "server1.nic4.tx",
            "cut.1->0",
            "shared_cut.bidirectional",
            "server0.nic4.rx",
            "rank4.rx"
          ]
        },
        {
          "sender": "r5:nic5",
          "receiver": "r13:nic5",
          "bytes": 6291456,
          "nic": 5,
          "element_start": 37748736,
          "element_stop": 40894464,
          "path": [
            "rank5.tx",
            "server0.nic5.tx",
            "cut.0->1",
            "shared_cut.bidirectional",
            "server1.nic5.rx",
            "rank13.rx"
          ]
        },
        {
          "sender": "r13:nic5",
          "receiver": "r5:nic5",
          "bytes": 6291456,
          "nic": 5,
          "element_start": 40894464,
          "element_stop": 44040192,
          "path": [
            "rank13.tx",
            "server1.nic5.tx",
            "cut.1->0",
            "shared_cut.bidirectional",
            "server0.nic5.rx",
            "rank5.rx"
          ]
        },
        {
          "sender": "r6:nic6",
          "receiver": "r14:nic6",
          "bytes": 6291456,
          "nic": 6,
          "element_start": 44040192,
          "element_stop": 47185920,
          "path": [
            "rank6.tx",
            "server0.nic6.tx",
            "cut.0->1",
            "shared_cut.bidirectional",
            "server1.nic6.rx",
            "rank14.rx"
          ]
        },
        {
          "sender": "r14:nic6",
          "receiver": "r6:nic6",
          "bytes": 6291456,
          "nic": 6,
          "element_start": 47185920,
          "element_stop": 50331648,
          "path": [
            "rank14.tx",
            "server1.nic6.tx",
            "cut.1->0",
            "shared_cut.bidirectional",
            "server0.nic6.rx",
            "rank6.rx"
          ]
        }
      ],
      "resource_bytes": {
        "rank7.tx": 6291456,
        "server0.nic7.tx": 6291456,
        "cut.0->1": 50331648,
        "shared_cut.bidirectional": 100663296,
        "server1.nic7.rx": 6291456,
        "rank15.rx": 6291456,
        "rank15.tx": 6291456,
        "server1.nic7.tx": 6291456,
        "cut.1->0": 50331648,
        "server0.nic7.rx": 6291456,
        "rank7.rx": 6291456,
        "rank0.tx": 6291456,
        "server0.nic0.tx": 6291456,
        "server1.nic0.rx": 6291456,
        "rank8.rx": 6291456,
        "rank8.tx": 6291456,
        "server1.nic0.tx": 6291456,
        "server0.nic0.rx": 6291456,
        "rank0.rx": 6291456,
        "rank1.tx": 6291456,
        "server0.nic1.tx": 6291456,
        "server1.nic1.rx": 6291456,
        "rank9.rx": 6291456,
        "rank9.tx": 6291456,
        "server1.nic1.tx": 6291456,
        "server0.nic1.rx": 6291456,
        "rank1.rx": 6291456,
        "rank2.tx": 6291456,
        "server0.nic2.tx": 6291456,
        "server1.nic2.rx": 6291456,
        "rank10.rx": 6291456,
        "rank10.tx": 6291456,
        "server1.nic2.tx": 6291456,
        "server0.nic2.rx": 6291456,
        "rank2.rx": 6291456,
        "rank3.tx": 6291456,
        "server0.nic3.tx": 6291456,
        "server1.nic3.rx": 6291456,
        "rank11.rx": 6291456,
        "rank11.tx": 6291456,
        "server1.nic3.tx": 6291456,
        "server0.nic3.rx": 6291456,
        "rank3.rx": 6291456,
        "rank4.tx": 6291456,
        "server0.nic4.tx": 6291456,
        "server1.nic4.rx": 6291456,
        "rank12.rx": 6291456,
        "rank12.tx": 6291456,
        "server1.nic4.tx": 6291456,
        "server0.nic4.rx": 6291456,
        "rank4.rx": 6291456,
        "rank5.tx": 6291456,
        "server0.nic5.tx": 6291456,
        "server1.nic5.rx": 6291456,
        "rank13.rx": 6291456,
        "rank13.tx": 6291456,
        "server1.nic5.tx": 6291456,
        "server0.nic5.rx": 6291456,
        "rank5.rx": 6291456,
        "rank6.tx": 6291456,
        "server0.nic6.tx": 6291456,
        "server1.nic6.rx": 6291456,
        "rank14.rx": 6291456,
        "rank14.tx": 6291456,
        "server1.nic6.tx": 6291456,
        "server0.nic6.rx": 6291456,
        "rank6.rx": 6291456
      },
      "resource_lower_seconds_exact": "6144/48828125",
      "barrier_lower_seconds_exact": "3166553/25000000000",
      "barrier_start_seconds_exact": "15117389/75000000000",
      "barrier_finish_seconds_exact": "3077131/9375000000"
    },
    {
      "round": 8,
      "stage": "cross_server_allreduce",
      "phase": "all_gather",
      "step": 0,
      "messages": [
        {
          "sender": 7,
          "receiver": 15,
          "operation": "copy",
          "chunks": [
            1
          ],
          "element_start": 3145728,
          "element_stop": 6291456,
          "bytes": 6291456,
          "contributions": [
            {
              "chunk": 1,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": true,
          "stripes": [
            {
              "sender": "r7:nic7",
              "receiver": "r15:nic7",
              "bytes": 6291456,
              "nic": 7,
              "element_start": 3145728,
              "element_stop": 6291456,
              "path": [
                "rank7.tx",
                "server0.nic7.tx",
                "cut.0->1",
                "shared_cut.bidirectional",
                "server1.nic7.rx",
                "rank15.rx"
              ]
            }
          ]
        },
        {
          "sender": 15,
          "receiver": 7,
          "operation": "copy",
          "chunks": [
            0
          ],
          "element_start": 0,
          "element_stop": 3145728,
          "bytes": 6291456,
          "contributions": [
            {
              "chunk": 0,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": true,
          "stripes": [
            {
              "sender": "r15:nic7",
              "receiver": "r7:nic7",
              "bytes": 6291456,
              "nic": 7,
              "element_start": 0,
              "element_stop": 3145728,
              "path": [
                "rank15.tx",
                "server1.nic7.tx",
                "cut.1->0",
                "shared_cut.bidirectional",
                "server0.nic7.rx",
                "rank7.rx"
              ]
            }
          ]
        },
        {
          "sender": 0,
          "receiver": 8,
          "operation": "copy",
          "chunks": [
            3
          ],
          "element_start": 9437184,
          "element_stop": 12582912,
          "bytes": 6291456,
          "contributions": [
            {
              "chunk": 3,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": true,
          "stripes": [
            {
              "sender": "r0:nic0",
              "receiver": "r8:nic0",
              "bytes": 6291456,
              "nic": 0,
              "element_start": 9437184,
              "element_stop": 12582912,
              "path": [
                "rank0.tx",
                "server0.nic0.tx",
                "cut.0->1",
                "shared_cut.bidirectional",
                "server1.nic0.rx",
                "rank8.rx"
              ]
            }
          ]
        },
        {
          "sender": 8,
          "receiver": 0,
          "operation": "copy",
          "chunks": [
            2
          ],
          "element_start": 6291456,
          "element_stop": 9437184,
          "bytes": 6291456,
          "contributions": [
            {
              "chunk": 2,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": true,
          "stripes": [
            {
              "sender": "r8:nic0",
              "receiver": "r0:nic0",
              "bytes": 6291456,
              "nic": 0,
              "element_start": 6291456,
              "element_stop": 9437184,
              "path": [
                "rank8.tx",
                "server1.nic0.tx",
                "cut.1->0",
                "shared_cut.bidirectional",
                "server0.nic0.rx",
                "rank0.rx"
              ]
            }
          ]
        },
        {
          "sender": 1,
          "receiver": 9,
          "operation": "copy",
          "chunks": [
            5
          ],
          "element_start": 15728640,
          "element_stop": 18874368,
          "bytes": 6291456,
          "contributions": [
            {
              "chunk": 5,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": true,
          "stripes": [
            {
              "sender": "r1:nic1",
              "receiver": "r9:nic1",
              "bytes": 6291456,
              "nic": 1,
              "element_start": 15728640,
              "element_stop": 18874368,
              "path": [
                "rank1.tx",
                "server0.nic1.tx",
                "cut.0->1",
                "shared_cut.bidirectional",
                "server1.nic1.rx",
                "rank9.rx"
              ]
            }
          ]
        },
        {
          "sender": 9,
          "receiver": 1,
          "operation": "copy",
          "chunks": [
            4
          ],
          "element_start": 12582912,
          "element_stop": 15728640,
          "bytes": 6291456,
          "contributions": [
            {
              "chunk": 4,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": true,
          "stripes": [
            {
              "sender": "r9:nic1",
              "receiver": "r1:nic1",
              "bytes": 6291456,
              "nic": 1,
              "element_start": 12582912,
              "element_stop": 15728640,
              "path": [
                "rank9.tx",
                "server1.nic1.tx",
                "cut.1->0",
                "shared_cut.bidirectional",
                "server0.nic1.rx",
                "rank1.rx"
              ]
            }
          ]
        },
        {
          "sender": 2,
          "receiver": 10,
          "operation": "copy",
          "chunks": [
            7
          ],
          "element_start": 22020096,
          "element_stop": 25165824,
          "bytes": 6291456,
          "contributions": [
            {
              "chunk": 7,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": true,
          "stripes": [
            {
              "sender": "r2:nic2",
              "receiver": "r10:nic2",
              "bytes": 6291456,
              "nic": 2,
              "element_start": 22020096,
              "element_stop": 25165824,
              "path": [
                "rank2.tx",
                "server0.nic2.tx",
                "cut.0->1",
                "shared_cut.bidirectional",
                "server1.nic2.rx",
                "rank10.rx"
              ]
            }
          ]
        },
        {
          "sender": 10,
          "receiver": 2,
          "operation": "copy",
          "chunks": [
            6
          ],
          "element_start": 18874368,
          "element_stop": 22020096,
          "bytes": 6291456,
          "contributions": [
            {
              "chunk": 6,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": true,
          "stripes": [
            {
              "sender": "r10:nic2",
              "receiver": "r2:nic2",
              "bytes": 6291456,
              "nic": 2,
              "element_start": 18874368,
              "element_stop": 22020096,
              "path": [
                "rank10.tx",
                "server1.nic2.tx",
                "cut.1->0",
                "shared_cut.bidirectional",
                "server0.nic2.rx",
                "rank2.rx"
              ]
            }
          ]
        },
        {
          "sender": 3,
          "receiver": 11,
          "operation": "copy",
          "chunks": [
            9
          ],
          "element_start": 28311552,
          "element_stop": 31457280,
          "bytes": 6291456,
          "contributions": [
            {
              "chunk": 9,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": true,
          "stripes": [
            {
              "sender": "r3:nic3",
              "receiver": "r11:nic3",
              "bytes": 6291456,
              "nic": 3,
              "element_start": 28311552,
              "element_stop": 31457280,
              "path": [
                "rank3.tx",
                "server0.nic3.tx",
                "cut.0->1",
                "shared_cut.bidirectional",
                "server1.nic3.rx",
                "rank11.rx"
              ]
            }
          ]
        },
        {
          "sender": 11,
          "receiver": 3,
          "operation": "copy",
          "chunks": [
            8
          ],
          "element_start": 25165824,
          "element_stop": 28311552,
          "bytes": 6291456,
          "contributions": [
            {
              "chunk": 8,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": true,
          "stripes": [
            {
              "sender": "r11:nic3",
              "receiver": "r3:nic3",
              "bytes": 6291456,
              "nic": 3,
              "element_start": 25165824,
              "element_stop": 28311552,
              "path": [
                "rank11.tx",
                "server1.nic3.tx",
                "cut.1->0",
                "shared_cut.bidirectional",
                "server0.nic3.rx",
                "rank3.rx"
              ]
            }
          ]
        },
        {
          "sender": 4,
          "receiver": 12,
          "operation": "copy",
          "chunks": [
            11
          ],
          "element_start": 34603008,
          "element_stop": 37748736,
          "bytes": 6291456,
          "contributions": [
            {
              "chunk": 11,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": true,
          "stripes": [
            {
              "sender": "r4:nic4",
              "receiver": "r12:nic4",
              "bytes": 6291456,
              "nic": 4,
              "element_start": 34603008,
              "element_stop": 37748736,
              "path": [
                "rank4.tx",
                "server0.nic4.tx",
                "cut.0->1",
                "shared_cut.bidirectional",
                "server1.nic4.rx",
                "rank12.rx"
              ]
            }
          ]
        },
        {
          "sender": 12,
          "receiver": 4,
          "operation": "copy",
          "chunks": [
            10
          ],
          "element_start": 31457280,
          "element_stop": 34603008,
          "bytes": 6291456,
          "contributions": [
            {
              "chunk": 10,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": true,
          "stripes": [
            {
              "sender": "r12:nic4",
              "receiver": "r4:nic4",
              "bytes": 6291456,
              "nic": 4,
              "element_start": 31457280,
              "element_stop": 34603008,
              "path": [
                "rank12.tx",
                "server1.nic4.tx",
                "cut.1->0",
                "shared_cut.bidirectional",
                "server0.nic4.rx",
                "rank4.rx"
              ]
            }
          ]
        },
        {
          "sender": 5,
          "receiver": 13,
          "operation": "copy",
          "chunks": [
            13
          ],
          "element_start": 40894464,
          "element_stop": 44040192,
          "bytes": 6291456,
          "contributions": [
            {
              "chunk": 13,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": true,
          "stripes": [
            {
              "sender": "r5:nic5",
              "receiver": "r13:nic5",
              "bytes": 6291456,
              "nic": 5,
              "element_start": 40894464,
              "element_stop": 44040192,
              "path": [
                "rank5.tx",
                "server0.nic5.tx",
                "cut.0->1",
                "shared_cut.bidirectional",
                "server1.nic5.rx",
                "rank13.rx"
              ]
            }
          ]
        },
        {
          "sender": 13,
          "receiver": 5,
          "operation": "copy",
          "chunks": [
            12
          ],
          "element_start": 37748736,
          "element_stop": 40894464,
          "bytes": 6291456,
          "contributions": [
            {
              "chunk": 12,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": true,
          "stripes": [
            {
              "sender": "r13:nic5",
              "receiver": "r5:nic5",
              "bytes": 6291456,
              "nic": 5,
              "element_start": 37748736,
              "element_stop": 40894464,
              "path": [
                "rank13.tx",
                "server1.nic5.tx",
                "cut.1->0",
                "shared_cut.bidirectional",
                "server0.nic5.rx",
                "rank5.rx"
              ]
            }
          ]
        },
        {
          "sender": 6,
          "receiver": 14,
          "operation": "copy",
          "chunks": [
            15
          ],
          "element_start": 47185920,
          "element_stop": 50331648,
          "bytes": 6291456,
          "contributions": [
            {
              "chunk": 15,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": true,
          "stripes": [
            {
              "sender": "r6:nic6",
              "receiver": "r14:nic6",
              "bytes": 6291456,
              "nic": 6,
              "element_start": 47185920,
              "element_stop": 50331648,
              "path": [
                "rank6.tx",
                "server0.nic6.tx",
                "cut.0->1",
                "shared_cut.bidirectional",
                "server1.nic6.rx",
                "rank14.rx"
              ]
            }
          ]
        },
        {
          "sender": 14,
          "receiver": 6,
          "operation": "copy",
          "chunks": [
            14
          ],
          "element_start": 44040192,
          "element_stop": 47185920,
          "bytes": 6291456,
          "contributions": [
            {
              "chunk": 14,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": true,
          "stripes": [
            {
              "sender": "r14:nic6",
              "receiver": "r6:nic6",
              "bytes": 6291456,
              "nic": 6,
              "element_start": 44040192,
              "element_stop": 47185920,
              "path": [
                "rank14.tx",
                "server1.nic6.tx",
                "cut.1->0",
                "shared_cut.bidirectional",
                "server0.nic6.rx",
                "rank6.rx"
              ]
            }
          ]
        }
      ],
      "edges": [
        {
          "sender": "r7:nic7",
          "receiver": "r15:nic7",
          "bytes": 6291456,
          "nic": 7,
          "element_start": 3145728,
          "element_stop": 6291456,
          "path": [
            "rank7.tx",
            "server0.nic7.tx",
            "cut.0->1",
            "shared_cut.bidirectional",
            "server1.nic7.rx",
            "rank15.rx"
          ]
        },
        {
          "sender": "r15:nic7",
          "receiver": "r7:nic7",
          "bytes": 6291456,
          "nic": 7,
          "element_start": 0,
          "element_stop": 3145728,
          "path": [
            "rank15.tx",
            "server1.nic7.tx",
            "cut.1->0",
            "shared_cut.bidirectional",
            "server0.nic7.rx",
            "rank7.rx"
          ]
        },
        {
          "sender": "r0:nic0",
          "receiver": "r8:nic0",
          "bytes": 6291456,
          "nic": 0,
          "element_start": 9437184,
          "element_stop": 12582912,
          "path": [
            "rank0.tx",
            "server0.nic0.tx",
            "cut.0->1",
            "shared_cut.bidirectional",
            "server1.nic0.rx",
            "rank8.rx"
          ]
        },
        {
          "sender": "r8:nic0",
          "receiver": "r0:nic0",
          "bytes": 6291456,
          "nic": 0,
          "element_start": 6291456,
          "element_stop": 9437184,
          "path": [
            "rank8.tx",
            "server1.nic0.tx",
            "cut.1->0",
            "shared_cut.bidirectional",
            "server0.nic0.rx",
            "rank0.rx"
          ]
        },
        {
          "sender": "r1:nic1",
          "receiver": "r9:nic1",
          "bytes": 6291456,
          "nic": 1,
          "element_start": 15728640,
          "element_stop": 18874368,
          "path": [
            "rank1.tx",
            "server0.nic1.tx",
            "cut.0->1",
            "shared_cut.bidirectional",
            "server1.nic1.rx",
            "rank9.rx"
          ]
        },
        {
          "sender": "r9:nic1",
          "receiver": "r1:nic1",
          "bytes": 6291456,
          "nic": 1,
          "element_start": 12582912,
          "element_stop": 15728640,
          "path": [
            "rank9.tx",
            "server1.nic1.tx",
            "cut.1->0",
            "shared_cut.bidirectional",
            "server0.nic1.rx",
            "rank1.rx"
          ]
        },
        {
          "sender": "r2:nic2",
          "receiver": "r10:nic2",
          "bytes": 6291456,
          "nic": 2,
          "element_start": 22020096,
          "element_stop": 25165824,
          "path": [
            "rank2.tx",
            "server0.nic2.tx",
            "cut.0->1",
            "shared_cut.bidirectional",
            "server1.nic2.rx",
            "rank10.rx"
          ]
        },
        {
          "sender": "r10:nic2",
          "receiver": "r2:nic2",
          "bytes": 6291456,
          "nic": 2,
          "element_start": 18874368,
          "element_stop": 22020096,
          "path": [
            "rank10.tx",
            "server1.nic2.tx",
            "cut.1->0",
            "shared_cut.bidirectional",
            "server0.nic2.rx",
            "rank2.rx"
          ]
        },
        {
          "sender": "r3:nic3",
          "receiver": "r11:nic3",
          "bytes": 6291456,
          "nic": 3,
          "element_start": 28311552,
          "element_stop": 31457280,
          "path": [
            "rank3.tx",
            "server0.nic3.tx",
            "cut.0->1",
            "shared_cut.bidirectional",
            "server1.nic3.rx",
            "rank11.rx"
          ]
        },
        {
          "sender": "r11:nic3",
          "receiver": "r3:nic3",
          "bytes": 6291456,
          "nic": 3,
          "element_start": 25165824,
          "element_stop": 28311552,
          "path": [
            "rank11.tx",
            "server1.nic3.tx",
            "cut.1->0",
            "shared_cut.bidirectional",
            "server0.nic3.rx",
            "rank3.rx"
          ]
        },
        {
          "sender": "r4:nic4",
          "receiver": "r12:nic4",
          "bytes": 6291456,
          "nic": 4,
          "element_start": 34603008,
          "element_stop": 37748736,
          "path": [
            "rank4.tx",
            "server0.nic4.tx",
            "cut.0->1",
            "shared_cut.bidirectional",
            "server1.nic4.rx",
            "rank12.rx"
          ]
        },
        {
          "sender": "r12:nic4",
          "receiver": "r4:nic4",
          "bytes": 6291456,
          "nic": 4,
          "element_start": 31457280,
          "element_stop": 34603008,
          "path": [
            "rank12.tx",
            "server1.nic4.tx",
            "cut.1->0",
            "shared_cut.bidirectional",
            "server0.nic4.rx",
            "rank4.rx"
          ]
        },
        {
          "sender": "r5:nic5",
          "receiver": "r13:nic5",
          "bytes": 6291456,
          "nic": 5,
          "element_start": 40894464,
          "element_stop": 44040192,
          "path": [
            "rank5.tx",
            "server0.nic5.tx",
            "cut.0->1",
            "shared_cut.bidirectional",
            "server1.nic5.rx",
            "rank13.rx"
          ]
        },
        {
          "sender": "r13:nic5",
          "receiver": "r5:nic5",
          "bytes": 6291456,
          "nic": 5,
          "element_start": 37748736,
          "element_stop": 40894464,
          "path": [
            "rank13.tx",
            "server1.nic5.tx",
            "cut.1->0",
            "shared_cut.bidirectional",
            "server0.nic5.rx",
            "rank5.rx"
          ]
        },
        {
          "sender": "r6:nic6",
          "receiver": "r14:nic6",
          "bytes": 6291456,
          "nic": 6,
          "element_start": 47185920,
          "element_stop": 50331648,
          "path": [
            "rank6.tx",
            "server0.nic6.tx",
            "cut.0->1",
            "shared_cut.bidirectional",
            "server1.nic6.rx",
            "rank14.rx"
          ]
        },
        {
          "sender": "r14:nic6",
          "receiver": "r6:nic6",
          "bytes": 6291456,
          "nic": 6,
          "element_start": 44040192,
          "element_stop": 47185920,
          "path": [
            "rank14.tx",
            "server1.nic6.tx",
            "cut.1->0",
            "shared_cut.bidirectional",
            "server0.nic6.rx",
            "rank6.rx"
          ]
        }
      ],
      "resource_bytes": {
        "rank7.tx": 6291456,
        "server0.nic7.tx": 6291456,
        "cut.0->1": 50331648,
        "shared_cut.bidirectional": 100663296,
        "server1.nic7.rx": 6291456,
        "rank15.rx": 6291456,
        "rank15.tx": 6291456,
        "server1.nic7.tx": 6291456,
        "cut.1->0": 50331648,
        "server0.nic7.rx": 6291456,
        "rank7.rx": 6291456,
        "rank0.tx": 6291456,
        "server0.nic0.tx": 6291456,
        "server1.nic0.rx": 6291456,
        "rank8.rx": 6291456,
        "rank8.tx": 6291456,
        "server1.nic0.tx": 6291456,
        "server0.nic0.rx": 6291456,
        "rank0.rx": 6291456,
        "rank1.tx": 6291456,
        "server0.nic1.tx": 6291456,
        "server1.nic1.rx": 6291456,
        "rank9.rx": 6291456,
        "rank9.tx": 6291456,
        "server1.nic1.tx": 6291456,
        "server0.nic1.rx": 6291456,
        "rank1.rx": 6291456,
        "rank2.tx": 6291456,
        "server0.nic2.tx": 6291456,
        "server1.nic2.rx": 6291456,
        "rank10.rx": 6291456,
        "rank10.tx": 6291456,
        "server1.nic2.tx": 6291456,
        "server0.nic2.rx": 6291456,
        "rank2.rx": 6291456,
        "rank3.tx": 6291456,
        "server0.nic3.tx": 6291456,
        "server1.nic3.rx": 6291456,
        "rank11.rx": 6291456,
        "rank11.tx": 6291456,
        "server1.nic3.tx": 6291456,
        "server0.nic3.rx": 6291456,
        "rank3.rx": 6291456,
        "rank4.tx": 6291456,
        "server0.nic4.tx": 6291456,
        "server1.nic4.rx": 6291456,
        "rank12.rx": 6291456,
        "rank12.tx": 6291456,
        "server1.nic4.tx": 6291456,
        "server0.nic4.rx": 6291456,
        "rank4.rx": 6291456,
        "rank5.tx": 6291456,
        "server0.nic5.tx": 6291456,
        "server1.nic5.rx": 6291456,
        "rank13.rx": 6291456,
        "rank13.tx": 6291456,
        "server1.nic5.tx": 6291456,
        "server0.nic5.rx": 6291456,
        "rank5.rx": 6291456,
        "rank6.tx": 6291456,
        "server0.nic6.tx": 6291456,
        "server1.nic6.rx": 6291456,
        "rank14.rx": 6291456,
        "rank14.tx": 6291456,
        "server1.nic6.tx": 6291456,
        "server0.nic6.rx": 6291456,
        "rank6.rx": 6291456
      },
      "resource_lower_seconds_exact": "6144/48828125",
      "barrier_lower_seconds_exact": "3166553/25000000000",
      "barrier_start_seconds_exact": "3077131/9375000000",
      "barrier_finish_seconds_exact": "34116707/75000000000"
    },
    {
      "round": 9,
      "stage": "local_all_gather",
      "phase": "all_gather",
      "step": 0,
      "messages": [
        {
          "sender": 0,
          "receiver": 1,
          "operation": "copy",
          "chunks": [
            2,
            3
          ],
          "element_start": 6291456,
          "element_stop": 12582912,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 2,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r0:local",
              "receiver": "r1:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 6291456,
              "element_stop": 12582912,
              "path": [
                "rank0.tx",
                "local.0->1",
                "rank1.rx"
              ]
            }
          ]
        },
        {
          "sender": 1,
          "receiver": 2,
          "operation": "copy",
          "chunks": [
            4,
            5
          ],
          "element_start": 12582912,
          "element_stop": 18874368,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 4,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r1:local",
              "receiver": "r2:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 12582912,
              "element_stop": 18874368,
              "path": [
                "rank1.tx",
                "local.1->2",
                "rank2.rx"
              ]
            }
          ]
        },
        {
          "sender": 2,
          "receiver": 3,
          "operation": "copy",
          "chunks": [
            6,
            7
          ],
          "element_start": 18874368,
          "element_stop": 25165824,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 6,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r2:local",
              "receiver": "r3:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 18874368,
              "element_stop": 25165824,
              "path": [
                "rank2.tx",
                "local.2->3",
                "rank3.rx"
              ]
            }
          ]
        },
        {
          "sender": 3,
          "receiver": 4,
          "operation": "copy",
          "chunks": [
            8,
            9
          ],
          "element_start": 25165824,
          "element_stop": 31457280,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 8,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r3:local",
              "receiver": "r4:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 25165824,
              "element_stop": 31457280,
              "path": [
                "rank3.tx",
                "local.3->4",
                "rank4.rx"
              ]
            }
          ]
        },
        {
          "sender": 4,
          "receiver": 5,
          "operation": "copy",
          "chunks": [
            10,
            11
          ],
          "element_start": 31457280,
          "element_stop": 37748736,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 10,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r4:local",
              "receiver": "r5:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 31457280,
              "element_stop": 37748736,
              "path": [
                "rank4.tx",
                "local.4->5",
                "rank5.rx"
              ]
            }
          ]
        },
        {
          "sender": 5,
          "receiver": 6,
          "operation": "copy",
          "chunks": [
            12,
            13
          ],
          "element_start": 37748736,
          "element_stop": 44040192,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 12,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r5:local",
              "receiver": "r6:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 37748736,
              "element_stop": 44040192,
              "path": [
                "rank5.tx",
                "local.5->6",
                "rank6.rx"
              ]
            }
          ]
        },
        {
          "sender": 6,
          "receiver": 7,
          "operation": "copy",
          "chunks": [
            14,
            15
          ],
          "element_start": 44040192,
          "element_stop": 50331648,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 14,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r6:local",
              "receiver": "r7:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 44040192,
              "element_stop": 50331648,
              "path": [
                "rank6.tx",
                "local.6->7",
                "rank7.rx"
              ]
            }
          ]
        },
        {
          "sender": 7,
          "receiver": 0,
          "operation": "copy",
          "chunks": [
            0,
            1
          ],
          "element_start": 0,
          "element_stop": 6291456,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 0,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r7:local",
              "receiver": "r0:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 0,
              "element_stop": 6291456,
              "path": [
                "rank7.tx",
                "local.7->0",
                "rank0.rx"
              ]
            }
          ]
        },
        {
          "sender": 8,
          "receiver": 9,
          "operation": "copy",
          "chunks": [
            2,
            3
          ],
          "element_start": 6291456,
          "element_stop": 12582912,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 2,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r8:local",
              "receiver": "r9:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 6291456,
              "element_stop": 12582912,
              "path": [
                "rank8.tx",
                "local.8->9",
                "rank9.rx"
              ]
            }
          ]
        },
        {
          "sender": 9,
          "receiver": 10,
          "operation": "copy",
          "chunks": [
            4,
            5
          ],
          "element_start": 12582912,
          "element_stop": 18874368,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 4,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r9:local",
              "receiver": "r10:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 12582912,
              "element_stop": 18874368,
              "path": [
                "rank9.tx",
                "local.9->10",
                "rank10.rx"
              ]
            }
          ]
        },
        {
          "sender": 10,
          "receiver": 11,
          "operation": "copy",
          "chunks": [
            6,
            7
          ],
          "element_start": 18874368,
          "element_stop": 25165824,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 6,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r10:local",
              "receiver": "r11:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 18874368,
              "element_stop": 25165824,
              "path": [
                "rank10.tx",
                "local.10->11",
                "rank11.rx"
              ]
            }
          ]
        },
        {
          "sender": 11,
          "receiver": 12,
          "operation": "copy",
          "chunks": [
            8,
            9
          ],
          "element_start": 25165824,
          "element_stop": 31457280,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 8,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r11:local",
              "receiver": "r12:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 25165824,
              "element_stop": 31457280,
              "path": [
                "rank11.tx",
                "local.11->12",
                "rank12.rx"
              ]
            }
          ]
        },
        {
          "sender": 12,
          "receiver": 13,
          "operation": "copy",
          "chunks": [
            10,
            11
          ],
          "element_start": 31457280,
          "element_stop": 37748736,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 10,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r12:local",
              "receiver": "r13:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 31457280,
              "element_stop": 37748736,
              "path": [
                "rank12.tx",
                "local.12->13",
                "rank13.rx"
              ]
            }
          ]
        },
        {
          "sender": 13,
          "receiver": 14,
          "operation": "copy",
          "chunks": [
            12,
            13
          ],
          "element_start": 37748736,
          "element_stop": 44040192,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 12,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r13:local",
              "receiver": "r14:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 37748736,
              "element_stop": 44040192,
              "path": [
                "rank13.tx",
                "local.13->14",
                "rank14.rx"
              ]
            }
          ]
        },
        {
          "sender": 14,
          "receiver": 15,
          "operation": "copy",
          "chunks": [
            14,
            15
          ],
          "element_start": 44040192,
          "element_stop": 50331648,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 14,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r14:local",
              "receiver": "r15:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 44040192,
              "element_stop": 50331648,
              "path": [
                "rank14.tx",
                "local.14->15",
                "rank15.rx"
              ]
            }
          ]
        },
        {
          "sender": 15,
          "receiver": 8,
          "operation": "copy",
          "chunks": [
            0,
            1
          ],
          "element_start": 0,
          "element_stop": 6291456,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 0,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r15:local",
              "receiver": "r8:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 0,
              "element_stop": 6291456,
              "path": [
                "rank15.tx",
                "local.15->8",
                "rank8.rx"
              ]
            }
          ]
        }
      ],
      "edges": [
        {
          "sender": "r0:local",
          "receiver": "r1:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 6291456,
          "element_stop": 12582912,
          "path": [
            "rank0.tx",
            "local.0->1",
            "rank1.rx"
          ]
        },
        {
          "sender": "r1:local",
          "receiver": "r2:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 12582912,
          "element_stop": 18874368,
          "path": [
            "rank1.tx",
            "local.1->2",
            "rank2.rx"
          ]
        },
        {
          "sender": "r2:local",
          "receiver": "r3:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 18874368,
          "element_stop": 25165824,
          "path": [
            "rank2.tx",
            "local.2->3",
            "rank3.rx"
          ]
        },
        {
          "sender": "r3:local",
          "receiver": "r4:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 25165824,
          "element_stop": 31457280,
          "path": [
            "rank3.tx",
            "local.3->4",
            "rank4.rx"
          ]
        },
        {
          "sender": "r4:local",
          "receiver": "r5:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 31457280,
          "element_stop": 37748736,
          "path": [
            "rank4.tx",
            "local.4->5",
            "rank5.rx"
          ]
        },
        {
          "sender": "r5:local",
          "receiver": "r6:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 37748736,
          "element_stop": 44040192,
          "path": [
            "rank5.tx",
            "local.5->6",
            "rank6.rx"
          ]
        },
        {
          "sender": "r6:local",
          "receiver": "r7:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 44040192,
          "element_stop": 50331648,
          "path": [
            "rank6.tx",
            "local.6->7",
            "rank7.rx"
          ]
        },
        {
          "sender": "r7:local",
          "receiver": "r0:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 0,
          "element_stop": 6291456,
          "path": [
            "rank7.tx",
            "local.7->0",
            "rank0.rx"
          ]
        },
        {
          "sender": "r8:local",
          "receiver": "r9:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 6291456,
          "element_stop": 12582912,
          "path": [
            "rank8.tx",
            "local.8->9",
            "rank9.rx"
          ]
        },
        {
          "sender": "r9:local",
          "receiver": "r10:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 12582912,
          "element_stop": 18874368,
          "path": [
            "rank9.tx",
            "local.9->10",
            "rank10.rx"
          ]
        },
        {
          "sender": "r10:local",
          "receiver": "r11:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 18874368,
          "element_stop": 25165824,
          "path": [
            "rank10.tx",
            "local.10->11",
            "rank11.rx"
          ]
        },
        {
          "sender": "r11:local",
          "receiver": "r12:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 25165824,
          "element_stop": 31457280,
          "path": [
            "rank11.tx",
            "local.11->12",
            "rank12.rx"
          ]
        },
        {
          "sender": "r12:local",
          "receiver": "r13:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 31457280,
          "element_stop": 37748736,
          "path": [
            "rank12.tx",
            "local.12->13",
            "rank13.rx"
          ]
        },
        {
          "sender": "r13:local",
          "receiver": "r14:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 37748736,
          "element_stop": 44040192,
          "path": [
            "rank13.tx",
            "local.13->14",
            "rank14.rx"
          ]
        },
        {
          "sender": "r14:local",
          "receiver": "r15:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 44040192,
          "element_stop": 50331648,
          "path": [
            "rank14.tx",
            "local.14->15",
            "rank15.rx"
          ]
        },
        {
          "sender": "r15:local",
          "receiver": "r8:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 0,
          "element_stop": 6291456,
          "path": [
            "rank15.tx",
            "local.15->8",
            "rank8.rx"
          ]
        }
      ],
      "resource_bytes": {
        "rank0.tx": 12582912,
        "local.0->1": 12582912,
        "rank1.rx": 12582912,
        "rank1.tx": 12582912,
        "local.1->2": 12582912,
        "rank2.rx": 12582912,
        "rank2.tx": 12582912,
        "local.2->3": 12582912,
        "rank3.rx": 12582912,
        "rank3.tx": 12582912,
        "local.3->4": 12582912,
        "rank4.rx": 12582912,
        "rank4.tx": 12582912,
        "local.4->5": 12582912,
        "rank5.rx": 12582912,
        "rank5.tx": 12582912,
        "local.5->6": 12582912,
        "rank6.rx": 12582912,
        "rank6.tx": 12582912,
        "local.6->7": 12582912,
        "rank7.rx": 12582912,
        "rank7.tx": 12582912,
        "local.7->0": 12582912,
        "rank0.rx": 12582912,
        "rank8.tx": 12582912,
        "local.8->9": 12582912,
        "rank9.rx": 12582912,
        "rank9.tx": 12582912,
        "local.9->10": 12582912,
        "rank10.rx": 12582912,
        "rank10.tx": 12582912,
        "local.10->11": 12582912,
        "rank11.rx": 12582912,
        "rank11.tx": 12582912,
        "local.11->12": 12582912,
        "rank12.rx": 12582912,
        "rank12.tx": 12582912,
        "local.12->13": 12582912,
        "rank13.rx": 12582912,
        "rank13.tx": 12582912,
        "local.13->14": 12582912,
        "rank14.rx": 12582912,
        "rank14.tx": 12582912,
        "local.14->15": 12582912,
        "rank15.rx": 12582912,
        "rank15.tx": 12582912,
        "local.15->8": 12582912,
        "rank8.rx": 12582912
      },
      "resource_lower_seconds_exact": "4096/146484375",
      "barrier_lower_seconds_exact": "2159627/75000000000",
      "barrier_start_seconds_exact": "34116707/75000000000",
      "barrier_finish_seconds_exact": "18138167/37500000000"
    },
    {
      "round": 10,
      "stage": "local_all_gather",
      "phase": "all_gather",
      "step": 1,
      "messages": [
        {
          "sender": 0,
          "receiver": 1,
          "operation": "copy",
          "chunks": [
            0,
            1
          ],
          "element_start": 0,
          "element_stop": 6291456,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 0,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r0:local",
              "receiver": "r1:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 0,
              "element_stop": 6291456,
              "path": [
                "rank0.tx",
                "local.0->1",
                "rank1.rx"
              ]
            }
          ]
        },
        {
          "sender": 1,
          "receiver": 2,
          "operation": "copy",
          "chunks": [
            2,
            3
          ],
          "element_start": 6291456,
          "element_stop": 12582912,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 2,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r1:local",
              "receiver": "r2:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 6291456,
              "element_stop": 12582912,
              "path": [
                "rank1.tx",
                "local.1->2",
                "rank2.rx"
              ]
            }
          ]
        },
        {
          "sender": 2,
          "receiver": 3,
          "operation": "copy",
          "chunks": [
            4,
            5
          ],
          "element_start": 12582912,
          "element_stop": 18874368,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 4,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r2:local",
              "receiver": "r3:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 12582912,
              "element_stop": 18874368,
              "path": [
                "rank2.tx",
                "local.2->3",
                "rank3.rx"
              ]
            }
          ]
        },
        {
          "sender": 3,
          "receiver": 4,
          "operation": "copy",
          "chunks": [
            6,
            7
          ],
          "element_start": 18874368,
          "element_stop": 25165824,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 6,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r3:local",
              "receiver": "r4:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 18874368,
              "element_stop": 25165824,
              "path": [
                "rank3.tx",
                "local.3->4",
                "rank4.rx"
              ]
            }
          ]
        },
        {
          "sender": 4,
          "receiver": 5,
          "operation": "copy",
          "chunks": [
            8,
            9
          ],
          "element_start": 25165824,
          "element_stop": 31457280,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 8,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r4:local",
              "receiver": "r5:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 25165824,
              "element_stop": 31457280,
              "path": [
                "rank4.tx",
                "local.4->5",
                "rank5.rx"
              ]
            }
          ]
        },
        {
          "sender": 5,
          "receiver": 6,
          "operation": "copy",
          "chunks": [
            10,
            11
          ],
          "element_start": 31457280,
          "element_stop": 37748736,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 10,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r5:local",
              "receiver": "r6:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 31457280,
              "element_stop": 37748736,
              "path": [
                "rank5.tx",
                "local.5->6",
                "rank6.rx"
              ]
            }
          ]
        },
        {
          "sender": 6,
          "receiver": 7,
          "operation": "copy",
          "chunks": [
            12,
            13
          ],
          "element_start": 37748736,
          "element_stop": 44040192,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 12,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r6:local",
              "receiver": "r7:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 37748736,
              "element_stop": 44040192,
              "path": [
                "rank6.tx",
                "local.6->7",
                "rank7.rx"
              ]
            }
          ]
        },
        {
          "sender": 7,
          "receiver": 0,
          "operation": "copy",
          "chunks": [
            14,
            15
          ],
          "element_start": 44040192,
          "element_stop": 50331648,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 14,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r7:local",
              "receiver": "r0:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 44040192,
              "element_stop": 50331648,
              "path": [
                "rank7.tx",
                "local.7->0",
                "rank0.rx"
              ]
            }
          ]
        },
        {
          "sender": 8,
          "receiver": 9,
          "operation": "copy",
          "chunks": [
            0,
            1
          ],
          "element_start": 0,
          "element_stop": 6291456,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 0,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r8:local",
              "receiver": "r9:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 0,
              "element_stop": 6291456,
              "path": [
                "rank8.tx",
                "local.8->9",
                "rank9.rx"
              ]
            }
          ]
        },
        {
          "sender": 9,
          "receiver": 10,
          "operation": "copy",
          "chunks": [
            2,
            3
          ],
          "element_start": 6291456,
          "element_stop": 12582912,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 2,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r9:local",
              "receiver": "r10:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 6291456,
              "element_stop": 12582912,
              "path": [
                "rank9.tx",
                "local.9->10",
                "rank10.rx"
              ]
            }
          ]
        },
        {
          "sender": 10,
          "receiver": 11,
          "operation": "copy",
          "chunks": [
            4,
            5
          ],
          "element_start": 12582912,
          "element_stop": 18874368,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 4,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r10:local",
              "receiver": "r11:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 12582912,
              "element_stop": 18874368,
              "path": [
                "rank10.tx",
                "local.10->11",
                "rank11.rx"
              ]
            }
          ]
        },
        {
          "sender": 11,
          "receiver": 12,
          "operation": "copy",
          "chunks": [
            6,
            7
          ],
          "element_start": 18874368,
          "element_stop": 25165824,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 6,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r11:local",
              "receiver": "r12:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 18874368,
              "element_stop": 25165824,
              "path": [
                "rank11.tx",
                "local.11->12",
                "rank12.rx"
              ]
            }
          ]
        },
        {
          "sender": 12,
          "receiver": 13,
          "operation": "copy",
          "chunks": [
            8,
            9
          ],
          "element_start": 25165824,
          "element_stop": 31457280,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 8,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r12:local",
              "receiver": "r13:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 25165824,
              "element_stop": 31457280,
              "path": [
                "rank12.tx",
                "local.12->13",
                "rank13.rx"
              ]
            }
          ]
        },
        {
          "sender": 13,
          "receiver": 14,
          "operation": "copy",
          "chunks": [
            10,
            11
          ],
          "element_start": 31457280,
          "element_stop": 37748736,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 10,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r13:local",
              "receiver": "r14:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 31457280,
              "element_stop": 37748736,
              "path": [
                "rank13.tx",
                "local.13->14",
                "rank14.rx"
              ]
            }
          ]
        },
        {
          "sender": 14,
          "receiver": 15,
          "operation": "copy",
          "chunks": [
            12,
            13
          ],
          "element_start": 37748736,
          "element_stop": 44040192,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 12,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r14:local",
              "receiver": "r15:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 37748736,
              "element_stop": 44040192,
              "path": [
                "rank14.tx",
                "local.14->15",
                "rank15.rx"
              ]
            }
          ]
        },
        {
          "sender": 15,
          "receiver": 8,
          "operation": "copy",
          "chunks": [
            14,
            15
          ],
          "element_start": 44040192,
          "element_stop": 50331648,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 14,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r15:local",
              "receiver": "r8:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 44040192,
              "element_stop": 50331648,
              "path": [
                "rank15.tx",
                "local.15->8",
                "rank8.rx"
              ]
            }
          ]
        }
      ],
      "edges": [
        {
          "sender": "r0:local",
          "receiver": "r1:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 0,
          "element_stop": 6291456,
          "path": [
            "rank0.tx",
            "local.0->1",
            "rank1.rx"
          ]
        },
        {
          "sender": "r1:local",
          "receiver": "r2:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 6291456,
          "element_stop": 12582912,
          "path": [
            "rank1.tx",
            "local.1->2",
            "rank2.rx"
          ]
        },
        {
          "sender": "r2:local",
          "receiver": "r3:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 12582912,
          "element_stop": 18874368,
          "path": [
            "rank2.tx",
            "local.2->3",
            "rank3.rx"
          ]
        },
        {
          "sender": "r3:local",
          "receiver": "r4:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 18874368,
          "element_stop": 25165824,
          "path": [
            "rank3.tx",
            "local.3->4",
            "rank4.rx"
          ]
        },
        {
          "sender": "r4:local",
          "receiver": "r5:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 25165824,
          "element_stop": 31457280,
          "path": [
            "rank4.tx",
            "local.4->5",
            "rank5.rx"
          ]
        },
        {
          "sender": "r5:local",
          "receiver": "r6:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 31457280,
          "element_stop": 37748736,
          "path": [
            "rank5.tx",
            "local.5->6",
            "rank6.rx"
          ]
        },
        {
          "sender": "r6:local",
          "receiver": "r7:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 37748736,
          "element_stop": 44040192,
          "path": [
            "rank6.tx",
            "local.6->7",
            "rank7.rx"
          ]
        },
        {
          "sender": "r7:local",
          "receiver": "r0:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 44040192,
          "element_stop": 50331648,
          "path": [
            "rank7.tx",
            "local.7->0",
            "rank0.rx"
          ]
        },
        {
          "sender": "r8:local",
          "receiver": "r9:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 0,
          "element_stop": 6291456,
          "path": [
            "rank8.tx",
            "local.8->9",
            "rank9.rx"
          ]
        },
        {
          "sender": "r9:local",
          "receiver": "r10:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 6291456,
          "element_stop": 12582912,
          "path": [
            "rank9.tx",
            "local.9->10",
            "rank10.rx"
          ]
        },
        {
          "sender": "r10:local",
          "receiver": "r11:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 12582912,
          "element_stop": 18874368,
          "path": [
            "rank10.tx",
            "local.10->11",
            "rank11.rx"
          ]
        },
        {
          "sender": "r11:local",
          "receiver": "r12:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 18874368,
          "element_stop": 25165824,
          "path": [
            "rank11.tx",
            "local.11->12",
            "rank12.rx"
          ]
        },
        {
          "sender": "r12:local",
          "receiver": "r13:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 25165824,
          "element_stop": 31457280,
          "path": [
            "rank12.tx",
            "local.12->13",
            "rank13.rx"
          ]
        },
        {
          "sender": "r13:local",
          "receiver": "r14:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 31457280,
          "element_stop": 37748736,
          "path": [
            "rank13.tx",
            "local.13->14",
            "rank14.rx"
          ]
        },
        {
          "sender": "r14:local",
          "receiver": "r15:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 37748736,
          "element_stop": 44040192,
          "path": [
            "rank14.tx",
            "local.14->15",
            "rank15.rx"
          ]
        },
        {
          "sender": "r15:local",
          "receiver": "r8:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 44040192,
          "element_stop": 50331648,
          "path": [
            "rank15.tx",
            "local.15->8",
            "rank8.rx"
          ]
        }
      ],
      "resource_bytes": {
        "rank0.tx": 12582912,
        "local.0->1": 12582912,
        "rank1.rx": 12582912,
        "rank1.tx": 12582912,
        "local.1->2": 12582912,
        "rank2.rx": 12582912,
        "rank2.tx": 12582912,
        "local.2->3": 12582912,
        "rank3.rx": 12582912,
        "rank3.tx": 12582912,
        "local.3->4": 12582912,
        "rank4.rx": 12582912,
        "rank4.tx": 12582912,
        "local.4->5": 12582912,
        "rank5.rx": 12582912,
        "rank5.tx": 12582912,
        "local.5->6": 12582912,
        "rank6.rx": 12582912,
        "rank6.tx": 12582912,
        "local.6->7": 12582912,
        "rank7.rx": 12582912,
        "rank7.tx": 12582912,
        "local.7->0": 12582912,
        "rank0.rx": 12582912,
        "rank8.tx": 12582912,
        "local.8->9": 12582912,
        "rank9.rx": 12582912,
        "rank9.tx": 12582912,
        "local.9->10": 12582912,
        "rank10.rx": 12582912,
        "rank10.tx": 12582912,
        "local.10->11": 12582912,
        "rank11.rx": 12582912,
        "rank11.tx": 12582912,
        "local.11->12": 12582912,
        "rank12.rx": 12582912,
        "rank12.tx": 12582912,
        "local.12->13": 12582912,
        "rank13.rx": 12582912,
        "rank13.tx": 12582912,
        "local.13->14": 12582912,
        "rank14.rx": 12582912,
        "rank14.tx": 12582912,
        "local.14->15": 12582912,
        "rank15.rx": 12582912,
        "rank15.tx": 12582912,
        "local.15->8": 12582912,
        "rank8.rx": 12582912
      },
      "resource_lower_seconds_exact": "4096/146484375",
      "barrier_lower_seconds_exact": "2159627/75000000000",
      "barrier_start_seconds_exact": "18138167/37500000000",
      "barrier_finish_seconds_exact": "12811987/25000000000"
    },
    {
      "round": 11,
      "stage": "local_all_gather",
      "phase": "all_gather",
      "step": 2,
      "messages": [
        {
          "sender": 0,
          "receiver": 1,
          "operation": "copy",
          "chunks": [
            14,
            15
          ],
          "element_start": 44040192,
          "element_stop": 50331648,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 14,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r0:local",
              "receiver": "r1:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 44040192,
              "element_stop": 50331648,
              "path": [
                "rank0.tx",
                "local.0->1",
                "rank1.rx"
              ]
            }
          ]
        },
        {
          "sender": 1,
          "receiver": 2,
          "operation": "copy",
          "chunks": [
            0,
            1
          ],
          "element_start": 0,
          "element_stop": 6291456,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 0,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r1:local",
              "receiver": "r2:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 0,
              "element_stop": 6291456,
              "path": [
                "rank1.tx",
                "local.1->2",
                "rank2.rx"
              ]
            }
          ]
        },
        {
          "sender": 2,
          "receiver": 3,
          "operation": "copy",
          "chunks": [
            2,
            3
          ],
          "element_start": 6291456,
          "element_stop": 12582912,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 2,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r2:local",
              "receiver": "r3:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 6291456,
              "element_stop": 12582912,
              "path": [
                "rank2.tx",
                "local.2->3",
                "rank3.rx"
              ]
            }
          ]
        },
        {
          "sender": 3,
          "receiver": 4,
          "operation": "copy",
          "chunks": [
            4,
            5
          ],
          "element_start": 12582912,
          "element_stop": 18874368,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 4,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r3:local",
              "receiver": "r4:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 12582912,
              "element_stop": 18874368,
              "path": [
                "rank3.tx",
                "local.3->4",
                "rank4.rx"
              ]
            }
          ]
        },
        {
          "sender": 4,
          "receiver": 5,
          "operation": "copy",
          "chunks": [
            6,
            7
          ],
          "element_start": 18874368,
          "element_stop": 25165824,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 6,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r4:local",
              "receiver": "r5:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 18874368,
              "element_stop": 25165824,
              "path": [
                "rank4.tx",
                "local.4->5",
                "rank5.rx"
              ]
            }
          ]
        },
        {
          "sender": 5,
          "receiver": 6,
          "operation": "copy",
          "chunks": [
            8,
            9
          ],
          "element_start": 25165824,
          "element_stop": 31457280,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 8,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r5:local",
              "receiver": "r6:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 25165824,
              "element_stop": 31457280,
              "path": [
                "rank5.tx",
                "local.5->6",
                "rank6.rx"
              ]
            }
          ]
        },
        {
          "sender": 6,
          "receiver": 7,
          "operation": "copy",
          "chunks": [
            10,
            11
          ],
          "element_start": 31457280,
          "element_stop": 37748736,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 10,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r6:local",
              "receiver": "r7:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 31457280,
              "element_stop": 37748736,
              "path": [
                "rank6.tx",
                "local.6->7",
                "rank7.rx"
              ]
            }
          ]
        },
        {
          "sender": 7,
          "receiver": 0,
          "operation": "copy",
          "chunks": [
            12,
            13
          ],
          "element_start": 37748736,
          "element_stop": 44040192,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 12,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r7:local",
              "receiver": "r0:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 37748736,
              "element_stop": 44040192,
              "path": [
                "rank7.tx",
                "local.7->0",
                "rank0.rx"
              ]
            }
          ]
        },
        {
          "sender": 8,
          "receiver": 9,
          "operation": "copy",
          "chunks": [
            14,
            15
          ],
          "element_start": 44040192,
          "element_stop": 50331648,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 14,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r8:local",
              "receiver": "r9:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 44040192,
              "element_stop": 50331648,
              "path": [
                "rank8.tx",
                "local.8->9",
                "rank9.rx"
              ]
            }
          ]
        },
        {
          "sender": 9,
          "receiver": 10,
          "operation": "copy",
          "chunks": [
            0,
            1
          ],
          "element_start": 0,
          "element_stop": 6291456,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 0,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r9:local",
              "receiver": "r10:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 0,
              "element_stop": 6291456,
              "path": [
                "rank9.tx",
                "local.9->10",
                "rank10.rx"
              ]
            }
          ]
        },
        {
          "sender": 10,
          "receiver": 11,
          "operation": "copy",
          "chunks": [
            2,
            3
          ],
          "element_start": 6291456,
          "element_stop": 12582912,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 2,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r10:local",
              "receiver": "r11:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 6291456,
              "element_stop": 12582912,
              "path": [
                "rank10.tx",
                "local.10->11",
                "rank11.rx"
              ]
            }
          ]
        },
        {
          "sender": 11,
          "receiver": 12,
          "operation": "copy",
          "chunks": [
            4,
            5
          ],
          "element_start": 12582912,
          "element_stop": 18874368,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 4,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r11:local",
              "receiver": "r12:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 12582912,
              "element_stop": 18874368,
              "path": [
                "rank11.tx",
                "local.11->12",
                "rank12.rx"
              ]
            }
          ]
        },
        {
          "sender": 12,
          "receiver": 13,
          "operation": "copy",
          "chunks": [
            6,
            7
          ],
          "element_start": 18874368,
          "element_stop": 25165824,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 6,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r12:local",
              "receiver": "r13:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 18874368,
              "element_stop": 25165824,
              "path": [
                "rank12.tx",
                "local.12->13",
                "rank13.rx"
              ]
            }
          ]
        },
        {
          "sender": 13,
          "receiver": 14,
          "operation": "copy",
          "chunks": [
            8,
            9
          ],
          "element_start": 25165824,
          "element_stop": 31457280,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 8,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r13:local",
              "receiver": "r14:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 25165824,
              "element_stop": 31457280,
              "path": [
                "rank13.tx",
                "local.13->14",
                "rank14.rx"
              ]
            }
          ]
        },
        {
          "sender": 14,
          "receiver": 15,
          "operation": "copy",
          "chunks": [
            10,
            11
          ],
          "element_start": 31457280,
          "element_stop": 37748736,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 10,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r14:local",
              "receiver": "r15:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 31457280,
              "element_stop": 37748736,
              "path": [
                "rank14.tx",
                "local.14->15",
                "rank15.rx"
              ]
            }
          ]
        },
        {
          "sender": 15,
          "receiver": 8,
          "operation": "copy",
          "chunks": [
            12,
            13
          ],
          "element_start": 37748736,
          "element_stop": 44040192,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 12,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r15:local",
              "receiver": "r8:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 37748736,
              "element_stop": 44040192,
              "path": [
                "rank15.tx",
                "local.15->8",
                "rank8.rx"
              ]
            }
          ]
        }
      ],
      "edges": [
        {
          "sender": "r0:local",
          "receiver": "r1:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 44040192,
          "element_stop": 50331648,
          "path": [
            "rank0.tx",
            "local.0->1",
            "rank1.rx"
          ]
        },
        {
          "sender": "r1:local",
          "receiver": "r2:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 0,
          "element_stop": 6291456,
          "path": [
            "rank1.tx",
            "local.1->2",
            "rank2.rx"
          ]
        },
        {
          "sender": "r2:local",
          "receiver": "r3:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 6291456,
          "element_stop": 12582912,
          "path": [
            "rank2.tx",
            "local.2->3",
            "rank3.rx"
          ]
        },
        {
          "sender": "r3:local",
          "receiver": "r4:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 12582912,
          "element_stop": 18874368,
          "path": [
            "rank3.tx",
            "local.3->4",
            "rank4.rx"
          ]
        },
        {
          "sender": "r4:local",
          "receiver": "r5:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 18874368,
          "element_stop": 25165824,
          "path": [
            "rank4.tx",
            "local.4->5",
            "rank5.rx"
          ]
        },
        {
          "sender": "r5:local",
          "receiver": "r6:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 25165824,
          "element_stop": 31457280,
          "path": [
            "rank5.tx",
            "local.5->6",
            "rank6.rx"
          ]
        },
        {
          "sender": "r6:local",
          "receiver": "r7:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 31457280,
          "element_stop": 37748736,
          "path": [
            "rank6.tx",
            "local.6->7",
            "rank7.rx"
          ]
        },
        {
          "sender": "r7:local",
          "receiver": "r0:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 37748736,
          "element_stop": 44040192,
          "path": [
            "rank7.tx",
            "local.7->0",
            "rank0.rx"
          ]
        },
        {
          "sender": "r8:local",
          "receiver": "r9:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 44040192,
          "element_stop": 50331648,
          "path": [
            "rank8.tx",
            "local.8->9",
            "rank9.rx"
          ]
        },
        {
          "sender": "r9:local",
          "receiver": "r10:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 0,
          "element_stop": 6291456,
          "path": [
            "rank9.tx",
            "local.9->10",
            "rank10.rx"
          ]
        },
        {
          "sender": "r10:local",
          "receiver": "r11:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 6291456,
          "element_stop": 12582912,
          "path": [
            "rank10.tx",
            "local.10->11",
            "rank11.rx"
          ]
        },
        {
          "sender": "r11:local",
          "receiver": "r12:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 12582912,
          "element_stop": 18874368,
          "path": [
            "rank11.tx",
            "local.11->12",
            "rank12.rx"
          ]
        },
        {
          "sender": "r12:local",
          "receiver": "r13:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 18874368,
          "element_stop": 25165824,
          "path": [
            "rank12.tx",
            "local.12->13",
            "rank13.rx"
          ]
        },
        {
          "sender": "r13:local",
          "receiver": "r14:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 25165824,
          "element_stop": 31457280,
          "path": [
            "rank13.tx",
            "local.13->14",
            "rank14.rx"
          ]
        },
        {
          "sender": "r14:local",
          "receiver": "r15:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 31457280,
          "element_stop": 37748736,
          "path": [
            "rank14.tx",
            "local.14->15",
            "rank15.rx"
          ]
        },
        {
          "sender": "r15:local",
          "receiver": "r8:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 37748736,
          "element_stop": 44040192,
          "path": [
            "rank15.tx",
            "local.15->8",
            "rank8.rx"
          ]
        }
      ],
      "resource_bytes": {
        "rank0.tx": 12582912,
        "local.0->1": 12582912,
        "rank1.rx": 12582912,
        "rank1.tx": 12582912,
        "local.1->2": 12582912,
        "rank2.rx": 12582912,
        "rank2.tx": 12582912,
        "local.2->3": 12582912,
        "rank3.rx": 12582912,
        "rank3.tx": 12582912,
        "local.3->4": 12582912,
        "rank4.rx": 12582912,
        "rank4.tx": 12582912,
        "local.4->5": 12582912,
        "rank5.rx": 12582912,
        "rank5.tx": 12582912,
        "local.5->6": 12582912,
        "rank6.rx": 12582912,
        "rank6.tx": 12582912,
        "local.6->7": 12582912,
        "rank7.rx": 12582912,
        "rank7.tx": 12582912,
        "local.7->0": 12582912,
        "rank0.rx": 12582912,
        "rank8.tx": 12582912,
        "local.8->9": 12582912,
        "rank9.rx": 12582912,
        "rank9.tx": 12582912,
        "local.9->10": 12582912,
        "rank10.rx": 12582912,
        "rank10.tx": 12582912,
        "local.10->11": 12582912,
        "rank11.rx": 12582912,
        "rank11.tx": 12582912,
        "local.11->12": 12582912,
        "rank12.rx": 12582912,
        "rank12.tx": 12582912,
        "local.12->13": 12582912,
        "rank13.rx": 12582912,
        "rank13.tx": 12582912,
        "local.13->14": 12582912,
        "rank14.rx": 12582912,
        "rank14.tx": 12582912,
        "local.14->15": 12582912,
        "rank15.rx": 12582912,
        "rank15.tx": 12582912,
        "local.15->8": 12582912,
        "rank8.rx": 12582912
      },
      "resource_lower_seconds_exact": "4096/146484375",
      "barrier_lower_seconds_exact": "2159627/75000000000",
      "barrier_start_seconds_exact": "12811987/25000000000",
      "barrier_finish_seconds_exact": "10148897/18750000000"
    },
    {
      "round": 12,
      "stage": "local_all_gather",
      "phase": "all_gather",
      "step": 3,
      "messages": [
        {
          "sender": 0,
          "receiver": 1,
          "operation": "copy",
          "chunks": [
            12,
            13
          ],
          "element_start": 37748736,
          "element_stop": 44040192,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 12,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r0:local",
              "receiver": "r1:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 37748736,
              "element_stop": 44040192,
              "path": [
                "rank0.tx",
                "local.0->1",
                "rank1.rx"
              ]
            }
          ]
        },
        {
          "sender": 1,
          "receiver": 2,
          "operation": "copy",
          "chunks": [
            14,
            15
          ],
          "element_start": 44040192,
          "element_stop": 50331648,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 14,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r1:local",
              "receiver": "r2:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 44040192,
              "element_stop": 50331648,
              "path": [
                "rank1.tx",
                "local.1->2",
                "rank2.rx"
              ]
            }
          ]
        },
        {
          "sender": 2,
          "receiver": 3,
          "operation": "copy",
          "chunks": [
            0,
            1
          ],
          "element_start": 0,
          "element_stop": 6291456,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 0,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r2:local",
              "receiver": "r3:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 0,
              "element_stop": 6291456,
              "path": [
                "rank2.tx",
                "local.2->3",
                "rank3.rx"
              ]
            }
          ]
        },
        {
          "sender": 3,
          "receiver": 4,
          "operation": "copy",
          "chunks": [
            2,
            3
          ],
          "element_start": 6291456,
          "element_stop": 12582912,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 2,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r3:local",
              "receiver": "r4:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 6291456,
              "element_stop": 12582912,
              "path": [
                "rank3.tx",
                "local.3->4",
                "rank4.rx"
              ]
            }
          ]
        },
        {
          "sender": 4,
          "receiver": 5,
          "operation": "copy",
          "chunks": [
            4,
            5
          ],
          "element_start": 12582912,
          "element_stop": 18874368,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 4,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r4:local",
              "receiver": "r5:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 12582912,
              "element_stop": 18874368,
              "path": [
                "rank4.tx",
                "local.4->5",
                "rank5.rx"
              ]
            }
          ]
        },
        {
          "sender": 5,
          "receiver": 6,
          "operation": "copy",
          "chunks": [
            6,
            7
          ],
          "element_start": 18874368,
          "element_stop": 25165824,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 6,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r5:local",
              "receiver": "r6:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 18874368,
              "element_stop": 25165824,
              "path": [
                "rank5.tx",
                "local.5->6",
                "rank6.rx"
              ]
            }
          ]
        },
        {
          "sender": 6,
          "receiver": 7,
          "operation": "copy",
          "chunks": [
            8,
            9
          ],
          "element_start": 25165824,
          "element_stop": 31457280,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 8,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r6:local",
              "receiver": "r7:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 25165824,
              "element_stop": 31457280,
              "path": [
                "rank6.tx",
                "local.6->7",
                "rank7.rx"
              ]
            }
          ]
        },
        {
          "sender": 7,
          "receiver": 0,
          "operation": "copy",
          "chunks": [
            10,
            11
          ],
          "element_start": 31457280,
          "element_stop": 37748736,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 10,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r7:local",
              "receiver": "r0:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 31457280,
              "element_stop": 37748736,
              "path": [
                "rank7.tx",
                "local.7->0",
                "rank0.rx"
              ]
            }
          ]
        },
        {
          "sender": 8,
          "receiver": 9,
          "operation": "copy",
          "chunks": [
            12,
            13
          ],
          "element_start": 37748736,
          "element_stop": 44040192,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 12,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r8:local",
              "receiver": "r9:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 37748736,
              "element_stop": 44040192,
              "path": [
                "rank8.tx",
                "local.8->9",
                "rank9.rx"
              ]
            }
          ]
        },
        {
          "sender": 9,
          "receiver": 10,
          "operation": "copy",
          "chunks": [
            14,
            15
          ],
          "element_start": 44040192,
          "element_stop": 50331648,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 14,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r9:local",
              "receiver": "r10:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 44040192,
              "element_stop": 50331648,
              "path": [
                "rank9.tx",
                "local.9->10",
                "rank10.rx"
              ]
            }
          ]
        },
        {
          "sender": 10,
          "receiver": 11,
          "operation": "copy",
          "chunks": [
            0,
            1
          ],
          "element_start": 0,
          "element_stop": 6291456,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 0,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r10:local",
              "receiver": "r11:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 0,
              "element_stop": 6291456,
              "path": [
                "rank10.tx",
                "local.10->11",
                "rank11.rx"
              ]
            }
          ]
        },
        {
          "sender": 11,
          "receiver": 12,
          "operation": "copy",
          "chunks": [
            2,
            3
          ],
          "element_start": 6291456,
          "element_stop": 12582912,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 2,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r11:local",
              "receiver": "r12:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 6291456,
              "element_stop": 12582912,
              "path": [
                "rank11.tx",
                "local.11->12",
                "rank12.rx"
              ]
            }
          ]
        },
        {
          "sender": 12,
          "receiver": 13,
          "operation": "copy",
          "chunks": [
            4,
            5
          ],
          "element_start": 12582912,
          "element_stop": 18874368,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 4,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r12:local",
              "receiver": "r13:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 12582912,
              "element_stop": 18874368,
              "path": [
                "rank12.tx",
                "local.12->13",
                "rank13.rx"
              ]
            }
          ]
        },
        {
          "sender": 13,
          "receiver": 14,
          "operation": "copy",
          "chunks": [
            6,
            7
          ],
          "element_start": 18874368,
          "element_stop": 25165824,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 6,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r13:local",
              "receiver": "r14:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 18874368,
              "element_stop": 25165824,
              "path": [
                "rank13.tx",
                "local.13->14",
                "rank14.rx"
              ]
            }
          ]
        },
        {
          "sender": 14,
          "receiver": 15,
          "operation": "copy",
          "chunks": [
            8,
            9
          ],
          "element_start": 25165824,
          "element_stop": 31457280,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 8,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r14:local",
              "receiver": "r15:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 25165824,
              "element_stop": 31457280,
              "path": [
                "rank14.tx",
                "local.14->15",
                "rank15.rx"
              ]
            }
          ]
        },
        {
          "sender": 15,
          "receiver": 8,
          "operation": "copy",
          "chunks": [
            10,
            11
          ],
          "element_start": 31457280,
          "element_stop": 37748736,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 10,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r15:local",
              "receiver": "r8:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 31457280,
              "element_stop": 37748736,
              "path": [
                "rank15.tx",
                "local.15->8",
                "rank8.rx"
              ]
            }
          ]
        }
      ],
      "edges": [
        {
          "sender": "r0:local",
          "receiver": "r1:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 37748736,
          "element_stop": 44040192,
          "path": [
            "rank0.tx",
            "local.0->1",
            "rank1.rx"
          ]
        },
        {
          "sender": "r1:local",
          "receiver": "r2:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 44040192,
          "element_stop": 50331648,
          "path": [
            "rank1.tx",
            "local.1->2",
            "rank2.rx"
          ]
        },
        {
          "sender": "r2:local",
          "receiver": "r3:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 0,
          "element_stop": 6291456,
          "path": [
            "rank2.tx",
            "local.2->3",
            "rank3.rx"
          ]
        },
        {
          "sender": "r3:local",
          "receiver": "r4:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 6291456,
          "element_stop": 12582912,
          "path": [
            "rank3.tx",
            "local.3->4",
            "rank4.rx"
          ]
        },
        {
          "sender": "r4:local",
          "receiver": "r5:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 12582912,
          "element_stop": 18874368,
          "path": [
            "rank4.tx",
            "local.4->5",
            "rank5.rx"
          ]
        },
        {
          "sender": "r5:local",
          "receiver": "r6:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 18874368,
          "element_stop": 25165824,
          "path": [
            "rank5.tx",
            "local.5->6",
            "rank6.rx"
          ]
        },
        {
          "sender": "r6:local",
          "receiver": "r7:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 25165824,
          "element_stop": 31457280,
          "path": [
            "rank6.tx",
            "local.6->7",
            "rank7.rx"
          ]
        },
        {
          "sender": "r7:local",
          "receiver": "r0:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 31457280,
          "element_stop": 37748736,
          "path": [
            "rank7.tx",
            "local.7->0",
            "rank0.rx"
          ]
        },
        {
          "sender": "r8:local",
          "receiver": "r9:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 37748736,
          "element_stop": 44040192,
          "path": [
            "rank8.tx",
            "local.8->9",
            "rank9.rx"
          ]
        },
        {
          "sender": "r9:local",
          "receiver": "r10:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 44040192,
          "element_stop": 50331648,
          "path": [
            "rank9.tx",
            "local.9->10",
            "rank10.rx"
          ]
        },
        {
          "sender": "r10:local",
          "receiver": "r11:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 0,
          "element_stop": 6291456,
          "path": [
            "rank10.tx",
            "local.10->11",
            "rank11.rx"
          ]
        },
        {
          "sender": "r11:local",
          "receiver": "r12:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 6291456,
          "element_stop": 12582912,
          "path": [
            "rank11.tx",
            "local.11->12",
            "rank12.rx"
          ]
        },
        {
          "sender": "r12:local",
          "receiver": "r13:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 12582912,
          "element_stop": 18874368,
          "path": [
            "rank12.tx",
            "local.12->13",
            "rank13.rx"
          ]
        },
        {
          "sender": "r13:local",
          "receiver": "r14:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 18874368,
          "element_stop": 25165824,
          "path": [
            "rank13.tx",
            "local.13->14",
            "rank14.rx"
          ]
        },
        {
          "sender": "r14:local",
          "receiver": "r15:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 25165824,
          "element_stop": 31457280,
          "path": [
            "rank14.tx",
            "local.14->15",
            "rank15.rx"
          ]
        },
        {
          "sender": "r15:local",
          "receiver": "r8:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 31457280,
          "element_stop": 37748736,
          "path": [
            "rank15.tx",
            "local.15->8",
            "rank8.rx"
          ]
        }
      ],
      "resource_bytes": {
        "rank0.tx": 12582912,
        "local.0->1": 12582912,
        "rank1.rx": 12582912,
        "rank1.tx": 12582912,
        "local.1->2": 12582912,
        "rank2.rx": 12582912,
        "rank2.tx": 12582912,
        "local.2->3": 12582912,
        "rank3.rx": 12582912,
        "rank3.tx": 12582912,
        "local.3->4": 12582912,
        "rank4.rx": 12582912,
        "rank4.tx": 12582912,
        "local.4->5": 12582912,
        "rank5.rx": 12582912,
        "rank5.tx": 12582912,
        "local.5->6": 12582912,
        "rank6.rx": 12582912,
        "rank6.tx": 12582912,
        "local.6->7": 12582912,
        "rank7.rx": 12582912,
        "rank7.tx": 12582912,
        "local.7->0": 12582912,
        "rank0.rx": 12582912,
        "rank8.tx": 12582912,
        "local.8->9": 12582912,
        "rank9.rx": 12582912,
        "rank9.tx": 12582912,
        "local.9->10": 12582912,
        "rank10.rx": 12582912,
        "rank10.tx": 12582912,
        "local.10->11": 12582912,
        "rank11.rx": 12582912,
        "rank11.tx": 12582912,
        "local.11->12": 12582912,
        "rank12.rx": 12582912,
        "rank12.tx": 12582912,
        "local.12->13": 12582912,
        "rank13.rx": 12582912,
        "rank13.tx": 12582912,
        "local.13->14": 12582912,
        "rank14.rx": 12582912,
        "rank14.tx": 12582912,
        "local.14->15": 12582912,
        "rank15.rx": 12582912,
        "rank15.tx": 12582912,
        "local.15->8": 12582912,
        "rank8.rx": 12582912
      },
      "resource_lower_seconds_exact": "4096/146484375",
      "barrier_lower_seconds_exact": "2159627/75000000000",
      "barrier_start_seconds_exact": "10148897/18750000000",
      "barrier_finish_seconds_exact": "8551043/15000000000"
    },
    {
      "round": 13,
      "stage": "local_all_gather",
      "phase": "all_gather",
      "step": 4,
      "messages": [
        {
          "sender": 0,
          "receiver": 1,
          "operation": "copy",
          "chunks": [
            10,
            11
          ],
          "element_start": 31457280,
          "element_stop": 37748736,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 10,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r0:local",
              "receiver": "r1:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 31457280,
              "element_stop": 37748736,
              "path": [
                "rank0.tx",
                "local.0->1",
                "rank1.rx"
              ]
            }
          ]
        },
        {
          "sender": 1,
          "receiver": 2,
          "operation": "copy",
          "chunks": [
            12,
            13
          ],
          "element_start": 37748736,
          "element_stop": 44040192,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 12,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r1:local",
              "receiver": "r2:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 37748736,
              "element_stop": 44040192,
              "path": [
                "rank1.tx",
                "local.1->2",
                "rank2.rx"
              ]
            }
          ]
        },
        {
          "sender": 2,
          "receiver": 3,
          "operation": "copy",
          "chunks": [
            14,
            15
          ],
          "element_start": 44040192,
          "element_stop": 50331648,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 14,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r2:local",
              "receiver": "r3:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 44040192,
              "element_stop": 50331648,
              "path": [
                "rank2.tx",
                "local.2->3",
                "rank3.rx"
              ]
            }
          ]
        },
        {
          "sender": 3,
          "receiver": 4,
          "operation": "copy",
          "chunks": [
            0,
            1
          ],
          "element_start": 0,
          "element_stop": 6291456,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 0,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r3:local",
              "receiver": "r4:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 0,
              "element_stop": 6291456,
              "path": [
                "rank3.tx",
                "local.3->4",
                "rank4.rx"
              ]
            }
          ]
        },
        {
          "sender": 4,
          "receiver": 5,
          "operation": "copy",
          "chunks": [
            2,
            3
          ],
          "element_start": 6291456,
          "element_stop": 12582912,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 2,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r4:local",
              "receiver": "r5:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 6291456,
              "element_stop": 12582912,
              "path": [
                "rank4.tx",
                "local.4->5",
                "rank5.rx"
              ]
            }
          ]
        },
        {
          "sender": 5,
          "receiver": 6,
          "operation": "copy",
          "chunks": [
            4,
            5
          ],
          "element_start": 12582912,
          "element_stop": 18874368,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 4,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r5:local",
              "receiver": "r6:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 12582912,
              "element_stop": 18874368,
              "path": [
                "rank5.tx",
                "local.5->6",
                "rank6.rx"
              ]
            }
          ]
        },
        {
          "sender": 6,
          "receiver": 7,
          "operation": "copy",
          "chunks": [
            6,
            7
          ],
          "element_start": 18874368,
          "element_stop": 25165824,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 6,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r6:local",
              "receiver": "r7:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 18874368,
              "element_stop": 25165824,
              "path": [
                "rank6.tx",
                "local.6->7",
                "rank7.rx"
              ]
            }
          ]
        },
        {
          "sender": 7,
          "receiver": 0,
          "operation": "copy",
          "chunks": [
            8,
            9
          ],
          "element_start": 25165824,
          "element_stop": 31457280,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 8,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r7:local",
              "receiver": "r0:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 25165824,
              "element_stop": 31457280,
              "path": [
                "rank7.tx",
                "local.7->0",
                "rank0.rx"
              ]
            }
          ]
        },
        {
          "sender": 8,
          "receiver": 9,
          "operation": "copy",
          "chunks": [
            10,
            11
          ],
          "element_start": 31457280,
          "element_stop": 37748736,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 10,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r8:local",
              "receiver": "r9:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 31457280,
              "element_stop": 37748736,
              "path": [
                "rank8.tx",
                "local.8->9",
                "rank9.rx"
              ]
            }
          ]
        },
        {
          "sender": 9,
          "receiver": 10,
          "operation": "copy",
          "chunks": [
            12,
            13
          ],
          "element_start": 37748736,
          "element_stop": 44040192,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 12,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r9:local",
              "receiver": "r10:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 37748736,
              "element_stop": 44040192,
              "path": [
                "rank9.tx",
                "local.9->10",
                "rank10.rx"
              ]
            }
          ]
        },
        {
          "sender": 10,
          "receiver": 11,
          "operation": "copy",
          "chunks": [
            14,
            15
          ],
          "element_start": 44040192,
          "element_stop": 50331648,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 14,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r10:local",
              "receiver": "r11:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 44040192,
              "element_stop": 50331648,
              "path": [
                "rank10.tx",
                "local.10->11",
                "rank11.rx"
              ]
            }
          ]
        },
        {
          "sender": 11,
          "receiver": 12,
          "operation": "copy",
          "chunks": [
            0,
            1
          ],
          "element_start": 0,
          "element_stop": 6291456,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 0,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r11:local",
              "receiver": "r12:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 0,
              "element_stop": 6291456,
              "path": [
                "rank11.tx",
                "local.11->12",
                "rank12.rx"
              ]
            }
          ]
        },
        {
          "sender": 12,
          "receiver": 13,
          "operation": "copy",
          "chunks": [
            2,
            3
          ],
          "element_start": 6291456,
          "element_stop": 12582912,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 2,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r12:local",
              "receiver": "r13:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 6291456,
              "element_stop": 12582912,
              "path": [
                "rank12.tx",
                "local.12->13",
                "rank13.rx"
              ]
            }
          ]
        },
        {
          "sender": 13,
          "receiver": 14,
          "operation": "copy",
          "chunks": [
            4,
            5
          ],
          "element_start": 12582912,
          "element_stop": 18874368,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 4,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r13:local",
              "receiver": "r14:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 12582912,
              "element_stop": 18874368,
              "path": [
                "rank13.tx",
                "local.13->14",
                "rank14.rx"
              ]
            }
          ]
        },
        {
          "sender": 14,
          "receiver": 15,
          "operation": "copy",
          "chunks": [
            6,
            7
          ],
          "element_start": 18874368,
          "element_stop": 25165824,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 6,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r14:local",
              "receiver": "r15:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 18874368,
              "element_stop": 25165824,
              "path": [
                "rank14.tx",
                "local.14->15",
                "rank15.rx"
              ]
            }
          ]
        },
        {
          "sender": 15,
          "receiver": 8,
          "operation": "copy",
          "chunks": [
            8,
            9
          ],
          "element_start": 25165824,
          "element_stop": 31457280,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 8,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r15:local",
              "receiver": "r8:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 25165824,
              "element_stop": 31457280,
              "path": [
                "rank15.tx",
                "local.15->8",
                "rank8.rx"
              ]
            }
          ]
        }
      ],
      "edges": [
        {
          "sender": "r0:local",
          "receiver": "r1:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 31457280,
          "element_stop": 37748736,
          "path": [
            "rank0.tx",
            "local.0->1",
            "rank1.rx"
          ]
        },
        {
          "sender": "r1:local",
          "receiver": "r2:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 37748736,
          "element_stop": 44040192,
          "path": [
            "rank1.tx",
            "local.1->2",
            "rank2.rx"
          ]
        },
        {
          "sender": "r2:local",
          "receiver": "r3:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 44040192,
          "element_stop": 50331648,
          "path": [
            "rank2.tx",
            "local.2->3",
            "rank3.rx"
          ]
        },
        {
          "sender": "r3:local",
          "receiver": "r4:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 0,
          "element_stop": 6291456,
          "path": [
            "rank3.tx",
            "local.3->4",
            "rank4.rx"
          ]
        },
        {
          "sender": "r4:local",
          "receiver": "r5:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 6291456,
          "element_stop": 12582912,
          "path": [
            "rank4.tx",
            "local.4->5",
            "rank5.rx"
          ]
        },
        {
          "sender": "r5:local",
          "receiver": "r6:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 12582912,
          "element_stop": 18874368,
          "path": [
            "rank5.tx",
            "local.5->6",
            "rank6.rx"
          ]
        },
        {
          "sender": "r6:local",
          "receiver": "r7:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 18874368,
          "element_stop": 25165824,
          "path": [
            "rank6.tx",
            "local.6->7",
            "rank7.rx"
          ]
        },
        {
          "sender": "r7:local",
          "receiver": "r0:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 25165824,
          "element_stop": 31457280,
          "path": [
            "rank7.tx",
            "local.7->0",
            "rank0.rx"
          ]
        },
        {
          "sender": "r8:local",
          "receiver": "r9:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 31457280,
          "element_stop": 37748736,
          "path": [
            "rank8.tx",
            "local.8->9",
            "rank9.rx"
          ]
        },
        {
          "sender": "r9:local",
          "receiver": "r10:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 37748736,
          "element_stop": 44040192,
          "path": [
            "rank9.tx",
            "local.9->10",
            "rank10.rx"
          ]
        },
        {
          "sender": "r10:local",
          "receiver": "r11:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 44040192,
          "element_stop": 50331648,
          "path": [
            "rank10.tx",
            "local.10->11",
            "rank11.rx"
          ]
        },
        {
          "sender": "r11:local",
          "receiver": "r12:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 0,
          "element_stop": 6291456,
          "path": [
            "rank11.tx",
            "local.11->12",
            "rank12.rx"
          ]
        },
        {
          "sender": "r12:local",
          "receiver": "r13:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 6291456,
          "element_stop": 12582912,
          "path": [
            "rank12.tx",
            "local.12->13",
            "rank13.rx"
          ]
        },
        {
          "sender": "r13:local",
          "receiver": "r14:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 12582912,
          "element_stop": 18874368,
          "path": [
            "rank13.tx",
            "local.13->14",
            "rank14.rx"
          ]
        },
        {
          "sender": "r14:local",
          "receiver": "r15:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 18874368,
          "element_stop": 25165824,
          "path": [
            "rank14.tx",
            "local.14->15",
            "rank15.rx"
          ]
        },
        {
          "sender": "r15:local",
          "receiver": "r8:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 25165824,
          "element_stop": 31457280,
          "path": [
            "rank15.tx",
            "local.15->8",
            "rank8.rx"
          ]
        }
      ],
      "resource_bytes": {
        "rank0.tx": 12582912,
        "local.0->1": 12582912,
        "rank1.rx": 12582912,
        "rank1.tx": 12582912,
        "local.1->2": 12582912,
        "rank2.rx": 12582912,
        "rank2.tx": 12582912,
        "local.2->3": 12582912,
        "rank3.rx": 12582912,
        "rank3.tx": 12582912,
        "local.3->4": 12582912,
        "rank4.rx": 12582912,
        "rank4.tx": 12582912,
        "local.4->5": 12582912,
        "rank5.rx": 12582912,
        "rank5.tx": 12582912,
        "local.5->6": 12582912,
        "rank6.rx": 12582912,
        "rank6.tx": 12582912,
        "local.6->7": 12582912,
        "rank7.rx": 12582912,
        "rank7.tx": 12582912,
        "local.7->0": 12582912,
        "rank0.rx": 12582912,
        "rank8.tx": 12582912,
        "local.8->9": 12582912,
        "rank9.rx": 12582912,
        "rank9.tx": 12582912,
        "local.9->10": 12582912,
        "rank10.rx": 12582912,
        "rank10.tx": 12582912,
        "local.10->11": 12582912,
        "rank11.rx": 12582912,
        "rank11.tx": 12582912,
        "local.11->12": 12582912,
        "rank12.rx": 12582912,
        "rank12.tx": 12582912,
        "local.12->13": 12582912,
        "rank13.rx": 12582912,
        "rank13.tx": 12582912,
        "local.13->14": 12582912,
        "rank14.rx": 12582912,
        "rank14.tx": 12582912,
        "local.14->15": 12582912,
        "rank15.rx": 12582912,
        "rank15.tx": 12582912,
        "local.15->8": 12582912,
        "rank8.rx": 12582912
      },
      "resource_lower_seconds_exact": "4096/146484375",
      "barrier_lower_seconds_exact": "2159627/75000000000",
      "barrier_start_seconds_exact": "8551043/15000000000",
      "barrier_finish_seconds_exact": "7485807/12500000000"
    },
    {
      "round": 14,
      "stage": "local_all_gather",
      "phase": "all_gather",
      "step": 5,
      "messages": [
        {
          "sender": 0,
          "receiver": 1,
          "operation": "copy",
          "chunks": [
            8,
            9
          ],
          "element_start": 25165824,
          "element_stop": 31457280,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 8,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r0:local",
              "receiver": "r1:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 25165824,
              "element_stop": 31457280,
              "path": [
                "rank0.tx",
                "local.0->1",
                "rank1.rx"
              ]
            }
          ]
        },
        {
          "sender": 1,
          "receiver": 2,
          "operation": "copy",
          "chunks": [
            10,
            11
          ],
          "element_start": 31457280,
          "element_stop": 37748736,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 10,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r1:local",
              "receiver": "r2:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 31457280,
              "element_stop": 37748736,
              "path": [
                "rank1.tx",
                "local.1->2",
                "rank2.rx"
              ]
            }
          ]
        },
        {
          "sender": 2,
          "receiver": 3,
          "operation": "copy",
          "chunks": [
            12,
            13
          ],
          "element_start": 37748736,
          "element_stop": 44040192,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 12,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r2:local",
              "receiver": "r3:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 37748736,
              "element_stop": 44040192,
              "path": [
                "rank2.tx",
                "local.2->3",
                "rank3.rx"
              ]
            }
          ]
        },
        {
          "sender": 3,
          "receiver": 4,
          "operation": "copy",
          "chunks": [
            14,
            15
          ],
          "element_start": 44040192,
          "element_stop": 50331648,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 14,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r3:local",
              "receiver": "r4:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 44040192,
              "element_stop": 50331648,
              "path": [
                "rank3.tx",
                "local.3->4",
                "rank4.rx"
              ]
            }
          ]
        },
        {
          "sender": 4,
          "receiver": 5,
          "operation": "copy",
          "chunks": [
            0,
            1
          ],
          "element_start": 0,
          "element_stop": 6291456,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 0,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r4:local",
              "receiver": "r5:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 0,
              "element_stop": 6291456,
              "path": [
                "rank4.tx",
                "local.4->5",
                "rank5.rx"
              ]
            }
          ]
        },
        {
          "sender": 5,
          "receiver": 6,
          "operation": "copy",
          "chunks": [
            2,
            3
          ],
          "element_start": 6291456,
          "element_stop": 12582912,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 2,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r5:local",
              "receiver": "r6:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 6291456,
              "element_stop": 12582912,
              "path": [
                "rank5.tx",
                "local.5->6",
                "rank6.rx"
              ]
            }
          ]
        },
        {
          "sender": 6,
          "receiver": 7,
          "operation": "copy",
          "chunks": [
            4,
            5
          ],
          "element_start": 12582912,
          "element_stop": 18874368,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 4,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r6:local",
              "receiver": "r7:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 12582912,
              "element_stop": 18874368,
              "path": [
                "rank6.tx",
                "local.6->7",
                "rank7.rx"
              ]
            }
          ]
        },
        {
          "sender": 7,
          "receiver": 0,
          "operation": "copy",
          "chunks": [
            6,
            7
          ],
          "element_start": 18874368,
          "element_stop": 25165824,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 6,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r7:local",
              "receiver": "r0:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 18874368,
              "element_stop": 25165824,
              "path": [
                "rank7.tx",
                "local.7->0",
                "rank0.rx"
              ]
            }
          ]
        },
        {
          "sender": 8,
          "receiver": 9,
          "operation": "copy",
          "chunks": [
            8,
            9
          ],
          "element_start": 25165824,
          "element_stop": 31457280,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 8,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r8:local",
              "receiver": "r9:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 25165824,
              "element_stop": 31457280,
              "path": [
                "rank8.tx",
                "local.8->9",
                "rank9.rx"
              ]
            }
          ]
        },
        {
          "sender": 9,
          "receiver": 10,
          "operation": "copy",
          "chunks": [
            10,
            11
          ],
          "element_start": 31457280,
          "element_stop": 37748736,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 10,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r9:local",
              "receiver": "r10:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 31457280,
              "element_stop": 37748736,
              "path": [
                "rank9.tx",
                "local.9->10",
                "rank10.rx"
              ]
            }
          ]
        },
        {
          "sender": 10,
          "receiver": 11,
          "operation": "copy",
          "chunks": [
            12,
            13
          ],
          "element_start": 37748736,
          "element_stop": 44040192,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 12,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r10:local",
              "receiver": "r11:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 37748736,
              "element_stop": 44040192,
              "path": [
                "rank10.tx",
                "local.10->11",
                "rank11.rx"
              ]
            }
          ]
        },
        {
          "sender": 11,
          "receiver": 12,
          "operation": "copy",
          "chunks": [
            14,
            15
          ],
          "element_start": 44040192,
          "element_stop": 50331648,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 14,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r11:local",
              "receiver": "r12:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 44040192,
              "element_stop": 50331648,
              "path": [
                "rank11.tx",
                "local.11->12",
                "rank12.rx"
              ]
            }
          ]
        },
        {
          "sender": 12,
          "receiver": 13,
          "operation": "copy",
          "chunks": [
            0,
            1
          ],
          "element_start": 0,
          "element_stop": 6291456,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 0,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r12:local",
              "receiver": "r13:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 0,
              "element_stop": 6291456,
              "path": [
                "rank12.tx",
                "local.12->13",
                "rank13.rx"
              ]
            }
          ]
        },
        {
          "sender": 13,
          "receiver": 14,
          "operation": "copy",
          "chunks": [
            2,
            3
          ],
          "element_start": 6291456,
          "element_stop": 12582912,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 2,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r13:local",
              "receiver": "r14:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 6291456,
              "element_stop": 12582912,
              "path": [
                "rank13.tx",
                "local.13->14",
                "rank14.rx"
              ]
            }
          ]
        },
        {
          "sender": 14,
          "receiver": 15,
          "operation": "copy",
          "chunks": [
            4,
            5
          ],
          "element_start": 12582912,
          "element_stop": 18874368,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 4,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r14:local",
              "receiver": "r15:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 12582912,
              "element_stop": 18874368,
              "path": [
                "rank14.tx",
                "local.14->15",
                "rank15.rx"
              ]
            }
          ]
        },
        {
          "sender": 15,
          "receiver": 8,
          "operation": "copy",
          "chunks": [
            6,
            7
          ],
          "element_start": 18874368,
          "element_stop": 25165824,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 6,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r15:local",
              "receiver": "r8:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 18874368,
              "element_stop": 25165824,
              "path": [
                "rank15.tx",
                "local.15->8",
                "rank8.rx"
              ]
            }
          ]
        }
      ],
      "edges": [
        {
          "sender": "r0:local",
          "receiver": "r1:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 25165824,
          "element_stop": 31457280,
          "path": [
            "rank0.tx",
            "local.0->1",
            "rank1.rx"
          ]
        },
        {
          "sender": "r1:local",
          "receiver": "r2:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 31457280,
          "element_stop": 37748736,
          "path": [
            "rank1.tx",
            "local.1->2",
            "rank2.rx"
          ]
        },
        {
          "sender": "r2:local",
          "receiver": "r3:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 37748736,
          "element_stop": 44040192,
          "path": [
            "rank2.tx",
            "local.2->3",
            "rank3.rx"
          ]
        },
        {
          "sender": "r3:local",
          "receiver": "r4:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 44040192,
          "element_stop": 50331648,
          "path": [
            "rank3.tx",
            "local.3->4",
            "rank4.rx"
          ]
        },
        {
          "sender": "r4:local",
          "receiver": "r5:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 0,
          "element_stop": 6291456,
          "path": [
            "rank4.tx",
            "local.4->5",
            "rank5.rx"
          ]
        },
        {
          "sender": "r5:local",
          "receiver": "r6:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 6291456,
          "element_stop": 12582912,
          "path": [
            "rank5.tx",
            "local.5->6",
            "rank6.rx"
          ]
        },
        {
          "sender": "r6:local",
          "receiver": "r7:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 12582912,
          "element_stop": 18874368,
          "path": [
            "rank6.tx",
            "local.6->7",
            "rank7.rx"
          ]
        },
        {
          "sender": "r7:local",
          "receiver": "r0:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 18874368,
          "element_stop": 25165824,
          "path": [
            "rank7.tx",
            "local.7->0",
            "rank0.rx"
          ]
        },
        {
          "sender": "r8:local",
          "receiver": "r9:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 25165824,
          "element_stop": 31457280,
          "path": [
            "rank8.tx",
            "local.8->9",
            "rank9.rx"
          ]
        },
        {
          "sender": "r9:local",
          "receiver": "r10:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 31457280,
          "element_stop": 37748736,
          "path": [
            "rank9.tx",
            "local.9->10",
            "rank10.rx"
          ]
        },
        {
          "sender": "r10:local",
          "receiver": "r11:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 37748736,
          "element_stop": 44040192,
          "path": [
            "rank10.tx",
            "local.10->11",
            "rank11.rx"
          ]
        },
        {
          "sender": "r11:local",
          "receiver": "r12:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 44040192,
          "element_stop": 50331648,
          "path": [
            "rank11.tx",
            "local.11->12",
            "rank12.rx"
          ]
        },
        {
          "sender": "r12:local",
          "receiver": "r13:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 0,
          "element_stop": 6291456,
          "path": [
            "rank12.tx",
            "local.12->13",
            "rank13.rx"
          ]
        },
        {
          "sender": "r13:local",
          "receiver": "r14:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 6291456,
          "element_stop": 12582912,
          "path": [
            "rank13.tx",
            "local.13->14",
            "rank14.rx"
          ]
        },
        {
          "sender": "r14:local",
          "receiver": "r15:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 12582912,
          "element_stop": 18874368,
          "path": [
            "rank14.tx",
            "local.14->15",
            "rank15.rx"
          ]
        },
        {
          "sender": "r15:local",
          "receiver": "r8:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 18874368,
          "element_stop": 25165824,
          "path": [
            "rank15.tx",
            "local.15->8",
            "rank8.rx"
          ]
        }
      ],
      "resource_bytes": {
        "rank0.tx": 12582912,
        "local.0->1": 12582912,
        "rank1.rx": 12582912,
        "rank1.tx": 12582912,
        "local.1->2": 12582912,
        "rank2.rx": 12582912,
        "rank2.tx": 12582912,
        "local.2->3": 12582912,
        "rank3.rx": 12582912,
        "rank3.tx": 12582912,
        "local.3->4": 12582912,
        "rank4.rx": 12582912,
        "rank4.tx": 12582912,
        "local.4->5": 12582912,
        "rank5.rx": 12582912,
        "rank5.tx": 12582912,
        "local.5->6": 12582912,
        "rank6.rx": 12582912,
        "rank6.tx": 12582912,
        "local.6->7": 12582912,
        "rank7.rx": 12582912,
        "rank7.tx": 12582912,
        "local.7->0": 12582912,
        "rank0.rx": 12582912,
        "rank8.tx": 12582912,
        "local.8->9": 12582912,
        "rank9.rx": 12582912,
        "rank9.tx": 12582912,
        "local.9->10": 12582912,
        "rank10.rx": 12582912,
        "rank10.tx": 12582912,
        "local.10->11": 12582912,
        "rank11.rx": 12582912,
        "rank11.tx": 12582912,
        "local.11->12": 12582912,
        "rank12.rx": 12582912,
        "rank12.tx": 12582912,
        "local.12->13": 12582912,
        "rank13.rx": 12582912,
        "rank13.tx": 12582912,
        "local.13->14": 12582912,
        "rank14.rx": 12582912,
        "rank14.tx": 12582912,
        "local.14->15": 12582912,
        "rank15.rx": 12582912,
        "rank15.tx": 12582912,
        "local.15->8": 12582912,
        "rank8.rx": 12582912
      },
      "resource_lower_seconds_exact": "4096/146484375",
      "barrier_lower_seconds_exact": "2159627/75000000000",
      "barrier_start_seconds_exact": "7485807/12500000000",
      "barrier_finish_seconds_exact": "47074469/75000000000"
    },
    {
      "round": 15,
      "stage": "local_all_gather",
      "phase": "all_gather",
      "step": 6,
      "messages": [
        {
          "sender": 0,
          "receiver": 1,
          "operation": "copy",
          "chunks": [
            6,
            7
          ],
          "element_start": 18874368,
          "element_stop": 25165824,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 6,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r0:local",
              "receiver": "r1:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 18874368,
              "element_stop": 25165824,
              "path": [
                "rank0.tx",
                "local.0->1",
                "rank1.rx"
              ]
            }
          ]
        },
        {
          "sender": 1,
          "receiver": 2,
          "operation": "copy",
          "chunks": [
            8,
            9
          ],
          "element_start": 25165824,
          "element_stop": 31457280,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 8,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r1:local",
              "receiver": "r2:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 25165824,
              "element_stop": 31457280,
              "path": [
                "rank1.tx",
                "local.1->2",
                "rank2.rx"
              ]
            }
          ]
        },
        {
          "sender": 2,
          "receiver": 3,
          "operation": "copy",
          "chunks": [
            10,
            11
          ],
          "element_start": 31457280,
          "element_stop": 37748736,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 10,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r2:local",
              "receiver": "r3:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 31457280,
              "element_stop": 37748736,
              "path": [
                "rank2.tx",
                "local.2->3",
                "rank3.rx"
              ]
            }
          ]
        },
        {
          "sender": 3,
          "receiver": 4,
          "operation": "copy",
          "chunks": [
            12,
            13
          ],
          "element_start": 37748736,
          "element_stop": 44040192,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 12,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r3:local",
              "receiver": "r4:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 37748736,
              "element_stop": 44040192,
              "path": [
                "rank3.tx",
                "local.3->4",
                "rank4.rx"
              ]
            }
          ]
        },
        {
          "sender": 4,
          "receiver": 5,
          "operation": "copy",
          "chunks": [
            14,
            15
          ],
          "element_start": 44040192,
          "element_stop": 50331648,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 14,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r4:local",
              "receiver": "r5:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 44040192,
              "element_stop": 50331648,
              "path": [
                "rank4.tx",
                "local.4->5",
                "rank5.rx"
              ]
            }
          ]
        },
        {
          "sender": 5,
          "receiver": 6,
          "operation": "copy",
          "chunks": [
            0,
            1
          ],
          "element_start": 0,
          "element_stop": 6291456,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 0,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r5:local",
              "receiver": "r6:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 0,
              "element_stop": 6291456,
              "path": [
                "rank5.tx",
                "local.5->6",
                "rank6.rx"
              ]
            }
          ]
        },
        {
          "sender": 6,
          "receiver": 7,
          "operation": "copy",
          "chunks": [
            2,
            3
          ],
          "element_start": 6291456,
          "element_stop": 12582912,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 2,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r6:local",
              "receiver": "r7:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 6291456,
              "element_stop": 12582912,
              "path": [
                "rank6.tx",
                "local.6->7",
                "rank7.rx"
              ]
            }
          ]
        },
        {
          "sender": 7,
          "receiver": 0,
          "operation": "copy",
          "chunks": [
            4,
            5
          ],
          "element_start": 12582912,
          "element_stop": 18874368,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 4,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r7:local",
              "receiver": "r0:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 12582912,
              "element_stop": 18874368,
              "path": [
                "rank7.tx",
                "local.7->0",
                "rank0.rx"
              ]
            }
          ]
        },
        {
          "sender": 8,
          "receiver": 9,
          "operation": "copy",
          "chunks": [
            6,
            7
          ],
          "element_start": 18874368,
          "element_stop": 25165824,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 6,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r8:local",
              "receiver": "r9:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 18874368,
              "element_stop": 25165824,
              "path": [
                "rank8.tx",
                "local.8->9",
                "rank9.rx"
              ]
            }
          ]
        },
        {
          "sender": 9,
          "receiver": 10,
          "operation": "copy",
          "chunks": [
            8,
            9
          ],
          "element_start": 25165824,
          "element_stop": 31457280,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 8,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r9:local",
              "receiver": "r10:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 25165824,
              "element_stop": 31457280,
              "path": [
                "rank9.tx",
                "local.9->10",
                "rank10.rx"
              ]
            }
          ]
        },
        {
          "sender": 10,
          "receiver": 11,
          "operation": "copy",
          "chunks": [
            10,
            11
          ],
          "element_start": 31457280,
          "element_stop": 37748736,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 10,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r10:local",
              "receiver": "r11:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 31457280,
              "element_stop": 37748736,
              "path": [
                "rank10.tx",
                "local.10->11",
                "rank11.rx"
              ]
            }
          ]
        },
        {
          "sender": 11,
          "receiver": 12,
          "operation": "copy",
          "chunks": [
            12,
            13
          ],
          "element_start": 37748736,
          "element_stop": 44040192,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 12,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r11:local",
              "receiver": "r12:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 37748736,
              "element_stop": 44040192,
              "path": [
                "rank11.tx",
                "local.11->12",
                "rank12.rx"
              ]
            }
          ]
        },
        {
          "sender": 12,
          "receiver": 13,
          "operation": "copy",
          "chunks": [
            14,
            15
          ],
          "element_start": 44040192,
          "element_stop": 50331648,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 14,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r12:local",
              "receiver": "r13:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 44040192,
              "element_stop": 50331648,
              "path": [
                "rank12.tx",
                "local.12->13",
                "rank13.rx"
              ]
            }
          ]
        },
        {
          "sender": 13,
          "receiver": 14,
          "operation": "copy",
          "chunks": [
            0,
            1
          ],
          "element_start": 0,
          "element_stop": 6291456,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 0,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r13:local",
              "receiver": "r14:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 0,
              "element_stop": 6291456,
              "path": [
                "rank13.tx",
                "local.13->14",
                "rank14.rx"
              ]
            }
          ]
        },
        {
          "sender": 14,
          "receiver": 15,
          "operation": "copy",
          "chunks": [
            2,
            3
          ],
          "element_start": 6291456,
          "element_stop": 12582912,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 2,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r14:local",
              "receiver": "r15:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 6291456,
              "element_stop": 12582912,
              "path": [
                "rank14.tx",
                "local.14->15",
                "rank15.rx"
              ]
            }
          ]
        },
        {
          "sender": 15,
          "receiver": 8,
          "operation": "copy",
          "chunks": [
            4,
            5
          ],
          "element_start": 12582912,
          "element_stop": 18874368,
          "bytes": 12582912,
          "contributions": [
            {
              "chunk": 4,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ],
          "remote": false,
          "stripes": [
            {
              "sender": "r15:local",
              "receiver": "r8:local",
              "bytes": 12582912,
              "nic": null,
              "element_start": 12582912,
              "element_stop": 18874368,
              "path": [
                "rank15.tx",
                "local.15->8",
                "rank8.rx"
              ]
            }
          ]
        }
      ],
      "edges": [
        {
          "sender": "r0:local",
          "receiver": "r1:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 18874368,
          "element_stop": 25165824,
          "path": [
            "rank0.tx",
            "local.0->1",
            "rank1.rx"
          ]
        },
        {
          "sender": "r1:local",
          "receiver": "r2:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 25165824,
          "element_stop": 31457280,
          "path": [
            "rank1.tx",
            "local.1->2",
            "rank2.rx"
          ]
        },
        {
          "sender": "r2:local",
          "receiver": "r3:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 31457280,
          "element_stop": 37748736,
          "path": [
            "rank2.tx",
            "local.2->3",
            "rank3.rx"
          ]
        },
        {
          "sender": "r3:local",
          "receiver": "r4:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 37748736,
          "element_stop": 44040192,
          "path": [
            "rank3.tx",
            "local.3->4",
            "rank4.rx"
          ]
        },
        {
          "sender": "r4:local",
          "receiver": "r5:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 44040192,
          "element_stop": 50331648,
          "path": [
            "rank4.tx",
            "local.4->5",
            "rank5.rx"
          ]
        },
        {
          "sender": "r5:local",
          "receiver": "r6:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 0,
          "element_stop": 6291456,
          "path": [
            "rank5.tx",
            "local.5->6",
            "rank6.rx"
          ]
        },
        {
          "sender": "r6:local",
          "receiver": "r7:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 6291456,
          "element_stop": 12582912,
          "path": [
            "rank6.tx",
            "local.6->7",
            "rank7.rx"
          ]
        },
        {
          "sender": "r7:local",
          "receiver": "r0:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 12582912,
          "element_stop": 18874368,
          "path": [
            "rank7.tx",
            "local.7->0",
            "rank0.rx"
          ]
        },
        {
          "sender": "r8:local",
          "receiver": "r9:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 18874368,
          "element_stop": 25165824,
          "path": [
            "rank8.tx",
            "local.8->9",
            "rank9.rx"
          ]
        },
        {
          "sender": "r9:local",
          "receiver": "r10:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 25165824,
          "element_stop": 31457280,
          "path": [
            "rank9.tx",
            "local.9->10",
            "rank10.rx"
          ]
        },
        {
          "sender": "r10:local",
          "receiver": "r11:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 31457280,
          "element_stop": 37748736,
          "path": [
            "rank10.tx",
            "local.10->11",
            "rank11.rx"
          ]
        },
        {
          "sender": "r11:local",
          "receiver": "r12:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 37748736,
          "element_stop": 44040192,
          "path": [
            "rank11.tx",
            "local.11->12",
            "rank12.rx"
          ]
        },
        {
          "sender": "r12:local",
          "receiver": "r13:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 44040192,
          "element_stop": 50331648,
          "path": [
            "rank12.tx",
            "local.12->13",
            "rank13.rx"
          ]
        },
        {
          "sender": "r13:local",
          "receiver": "r14:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 0,
          "element_stop": 6291456,
          "path": [
            "rank13.tx",
            "local.13->14",
            "rank14.rx"
          ]
        },
        {
          "sender": "r14:local",
          "receiver": "r15:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 6291456,
          "element_stop": 12582912,
          "path": [
            "rank14.tx",
            "local.14->15",
            "rank15.rx"
          ]
        },
        {
          "sender": "r15:local",
          "receiver": "r8:local",
          "bytes": 12582912,
          "nic": null,
          "element_start": 12582912,
          "element_stop": 18874368,
          "path": [
            "rank15.tx",
            "local.15->8",
            "rank8.rx"
          ]
        }
      ],
      "resource_bytes": {
        "rank0.tx": 12582912,
        "local.0->1": 12582912,
        "rank1.rx": 12582912,
        "rank1.tx": 12582912,
        "local.1->2": 12582912,
        "rank2.rx": 12582912,
        "rank2.tx": 12582912,
        "local.2->3": 12582912,
        "rank3.rx": 12582912,
        "rank3.tx": 12582912,
        "local.3->4": 12582912,
        "rank4.rx": 12582912,
        "rank4.tx": 12582912,
        "local.4->5": 12582912,
        "rank5.rx": 12582912,
        "rank5.tx": 12582912,
        "local.5->6": 12582912,
        "rank6.rx": 12582912,
        "rank6.tx": 12582912,
        "local.6->7": 12582912,
        "rank7.rx": 12582912,
        "rank7.tx": 12582912,
        "local.7->0": 12582912,
        "rank0.rx": 12582912,
        "rank8.tx": 12582912,
        "local.8->9": 12582912,
        "rank9.rx": 12582912,
        "rank9.tx": 12582912,
        "local.9->10": 12582912,
        "rank10.rx": 12582912,
        "rank10.tx": 12582912,
        "local.10->11": 12582912,
        "rank11.rx": 12582912,
        "rank11.tx": 12582912,
        "local.11->12": 12582912,
        "rank12.rx": 12582912,
        "rank12.tx": 12582912,
        "local.12->13": 12582912,
        "rank13.rx": 12582912,
        "rank13.tx": 12582912,
        "local.13->14": 12582912,
        "rank14.rx": 12582912,
        "rank14.tx": 12582912,
        "local.14->15": 12582912,
        "rank15.rx": 12582912,
        "rank15.tx": 12582912,
        "local.15->8": 12582912,
        "rank8.rx": 12582912
      },
      "resource_lower_seconds_exact": "4096/146484375",
      "barrier_lower_seconds_exact": "2159627/75000000000",
      "barrier_start_seconds_exact": "47074469/75000000000",
      "barrier_finish_seconds_exact": "3077131/4687500000"
    }
  ],
  "ownership_boundaries": [
    {
      "after": "initial",
      "round_count": 0,
      "ranks": [
        {
          "rank": 0,
          "chunks": [
            {
              "chunk": 0,
              "contributors": [
                0
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                0
              ]
            },
            {
              "chunk": 2,
              "contributors": [
                0
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                0
              ]
            },
            {
              "chunk": 4,
              "contributors": [
                0
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                0
              ]
            },
            {
              "chunk": 6,
              "contributors": [
                0
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                0
              ]
            },
            {
              "chunk": 8,
              "contributors": [
                0
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                0
              ]
            },
            {
              "chunk": 10,
              "contributors": [
                0
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                0
              ]
            },
            {
              "chunk": 12,
              "contributors": [
                0
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                0
              ]
            },
            {
              "chunk": 14,
              "contributors": [
                0
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                0
              ]
            }
          ]
        },
        {
          "rank": 1,
          "chunks": [
            {
              "chunk": 0,
              "contributors": [
                1
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                1
              ]
            },
            {
              "chunk": 2,
              "contributors": [
                1
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                1
              ]
            },
            {
              "chunk": 4,
              "contributors": [
                1
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                1
              ]
            },
            {
              "chunk": 6,
              "contributors": [
                1
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                1
              ]
            },
            {
              "chunk": 8,
              "contributors": [
                1
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                1
              ]
            },
            {
              "chunk": 10,
              "contributors": [
                1
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                1
              ]
            },
            {
              "chunk": 12,
              "contributors": [
                1
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                1
              ]
            },
            {
              "chunk": 14,
              "contributors": [
                1
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                1
              ]
            }
          ]
        },
        {
          "rank": 2,
          "chunks": [
            {
              "chunk": 0,
              "contributors": [
                2
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                2
              ]
            },
            {
              "chunk": 2,
              "contributors": [
                2
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                2
              ]
            },
            {
              "chunk": 4,
              "contributors": [
                2
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                2
              ]
            },
            {
              "chunk": 6,
              "contributors": [
                2
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                2
              ]
            },
            {
              "chunk": 8,
              "contributors": [
                2
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                2
              ]
            },
            {
              "chunk": 10,
              "contributors": [
                2
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                2
              ]
            },
            {
              "chunk": 12,
              "contributors": [
                2
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                2
              ]
            },
            {
              "chunk": 14,
              "contributors": [
                2
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                2
              ]
            }
          ]
        },
        {
          "rank": 3,
          "chunks": [
            {
              "chunk": 0,
              "contributors": [
                3
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                3
              ]
            },
            {
              "chunk": 2,
              "contributors": [
                3
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                3
              ]
            },
            {
              "chunk": 4,
              "contributors": [
                3
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                3
              ]
            },
            {
              "chunk": 6,
              "contributors": [
                3
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                3
              ]
            },
            {
              "chunk": 8,
              "contributors": [
                3
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                3
              ]
            },
            {
              "chunk": 10,
              "contributors": [
                3
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                3
              ]
            },
            {
              "chunk": 12,
              "contributors": [
                3
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                3
              ]
            },
            {
              "chunk": 14,
              "contributors": [
                3
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                3
              ]
            }
          ]
        },
        {
          "rank": 4,
          "chunks": [
            {
              "chunk": 0,
              "contributors": [
                4
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                4
              ]
            },
            {
              "chunk": 2,
              "contributors": [
                4
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                4
              ]
            },
            {
              "chunk": 4,
              "contributors": [
                4
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                4
              ]
            },
            {
              "chunk": 6,
              "contributors": [
                4
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                4
              ]
            },
            {
              "chunk": 8,
              "contributors": [
                4
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                4
              ]
            },
            {
              "chunk": 10,
              "contributors": [
                4
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                4
              ]
            },
            {
              "chunk": 12,
              "contributors": [
                4
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                4
              ]
            },
            {
              "chunk": 14,
              "contributors": [
                4
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                4
              ]
            }
          ]
        },
        {
          "rank": 5,
          "chunks": [
            {
              "chunk": 0,
              "contributors": [
                5
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                5
              ]
            },
            {
              "chunk": 2,
              "contributors": [
                5
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                5
              ]
            },
            {
              "chunk": 4,
              "contributors": [
                5
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                5
              ]
            },
            {
              "chunk": 6,
              "contributors": [
                5
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                5
              ]
            },
            {
              "chunk": 8,
              "contributors": [
                5
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                5
              ]
            },
            {
              "chunk": 10,
              "contributors": [
                5
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                5
              ]
            },
            {
              "chunk": 12,
              "contributors": [
                5
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                5
              ]
            },
            {
              "chunk": 14,
              "contributors": [
                5
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                5
              ]
            }
          ]
        },
        {
          "rank": 6,
          "chunks": [
            {
              "chunk": 0,
              "contributors": [
                6
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                6
              ]
            },
            {
              "chunk": 2,
              "contributors": [
                6
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                6
              ]
            },
            {
              "chunk": 4,
              "contributors": [
                6
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                6
              ]
            },
            {
              "chunk": 6,
              "contributors": [
                6
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                6
              ]
            },
            {
              "chunk": 8,
              "contributors": [
                6
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                6
              ]
            },
            {
              "chunk": 10,
              "contributors": [
                6
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                6
              ]
            },
            {
              "chunk": 12,
              "contributors": [
                6
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                6
              ]
            },
            {
              "chunk": 14,
              "contributors": [
                6
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                6
              ]
            }
          ]
        },
        {
          "rank": 7,
          "chunks": [
            {
              "chunk": 0,
              "contributors": [
                7
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                7
              ]
            },
            {
              "chunk": 2,
              "contributors": [
                7
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                7
              ]
            },
            {
              "chunk": 4,
              "contributors": [
                7
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                7
              ]
            },
            {
              "chunk": 6,
              "contributors": [
                7
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                7
              ]
            },
            {
              "chunk": 8,
              "contributors": [
                7
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                7
              ]
            },
            {
              "chunk": 10,
              "contributors": [
                7
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                7
              ]
            },
            {
              "chunk": 12,
              "contributors": [
                7
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                7
              ]
            },
            {
              "chunk": 14,
              "contributors": [
                7
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                7
              ]
            }
          ]
        },
        {
          "rank": 8,
          "chunks": [
            {
              "chunk": 0,
              "contributors": [
                8
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                8
              ]
            },
            {
              "chunk": 2,
              "contributors": [
                8
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                8
              ]
            },
            {
              "chunk": 4,
              "contributors": [
                8
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                8
              ]
            },
            {
              "chunk": 6,
              "contributors": [
                8
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                8
              ]
            },
            {
              "chunk": 8,
              "contributors": [
                8
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                8
              ]
            },
            {
              "chunk": 10,
              "contributors": [
                8
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                8
              ]
            },
            {
              "chunk": 12,
              "contributors": [
                8
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                8
              ]
            },
            {
              "chunk": 14,
              "contributors": [
                8
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                8
              ]
            }
          ]
        },
        {
          "rank": 9,
          "chunks": [
            {
              "chunk": 0,
              "contributors": [
                9
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                9
              ]
            },
            {
              "chunk": 2,
              "contributors": [
                9
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                9
              ]
            },
            {
              "chunk": 4,
              "contributors": [
                9
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                9
              ]
            },
            {
              "chunk": 6,
              "contributors": [
                9
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                9
              ]
            },
            {
              "chunk": 8,
              "contributors": [
                9
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                9
              ]
            },
            {
              "chunk": 10,
              "contributors": [
                9
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                9
              ]
            },
            {
              "chunk": 12,
              "contributors": [
                9
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                9
              ]
            },
            {
              "chunk": 14,
              "contributors": [
                9
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                9
              ]
            }
          ]
        },
        {
          "rank": 10,
          "chunks": [
            {
              "chunk": 0,
              "contributors": [
                10
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                10
              ]
            },
            {
              "chunk": 2,
              "contributors": [
                10
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                10
              ]
            },
            {
              "chunk": 4,
              "contributors": [
                10
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                10
              ]
            },
            {
              "chunk": 6,
              "contributors": [
                10
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                10
              ]
            },
            {
              "chunk": 8,
              "contributors": [
                10
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                10
              ]
            },
            {
              "chunk": 10,
              "contributors": [
                10
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                10
              ]
            },
            {
              "chunk": 12,
              "contributors": [
                10
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                10
              ]
            },
            {
              "chunk": 14,
              "contributors": [
                10
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                10
              ]
            }
          ]
        },
        {
          "rank": 11,
          "chunks": [
            {
              "chunk": 0,
              "contributors": [
                11
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                11
              ]
            },
            {
              "chunk": 2,
              "contributors": [
                11
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                11
              ]
            },
            {
              "chunk": 4,
              "contributors": [
                11
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                11
              ]
            },
            {
              "chunk": 6,
              "contributors": [
                11
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                11
              ]
            },
            {
              "chunk": 8,
              "contributors": [
                11
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                11
              ]
            },
            {
              "chunk": 10,
              "contributors": [
                11
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                11
              ]
            },
            {
              "chunk": 12,
              "contributors": [
                11
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                11
              ]
            },
            {
              "chunk": 14,
              "contributors": [
                11
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                11
              ]
            }
          ]
        },
        {
          "rank": 12,
          "chunks": [
            {
              "chunk": 0,
              "contributors": [
                12
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                12
              ]
            },
            {
              "chunk": 2,
              "contributors": [
                12
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                12
              ]
            },
            {
              "chunk": 4,
              "contributors": [
                12
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                12
              ]
            },
            {
              "chunk": 6,
              "contributors": [
                12
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                12
              ]
            },
            {
              "chunk": 8,
              "contributors": [
                12
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                12
              ]
            },
            {
              "chunk": 10,
              "contributors": [
                12
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                12
              ]
            },
            {
              "chunk": 12,
              "contributors": [
                12
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                12
              ]
            },
            {
              "chunk": 14,
              "contributors": [
                12
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                12
              ]
            }
          ]
        },
        {
          "rank": 13,
          "chunks": [
            {
              "chunk": 0,
              "contributors": [
                13
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                13
              ]
            },
            {
              "chunk": 2,
              "contributors": [
                13
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                13
              ]
            },
            {
              "chunk": 4,
              "contributors": [
                13
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                13
              ]
            },
            {
              "chunk": 6,
              "contributors": [
                13
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                13
              ]
            },
            {
              "chunk": 8,
              "contributors": [
                13
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                13
              ]
            },
            {
              "chunk": 10,
              "contributors": [
                13
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                13
              ]
            },
            {
              "chunk": 12,
              "contributors": [
                13
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                13
              ]
            },
            {
              "chunk": 14,
              "contributors": [
                13
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                13
              ]
            }
          ]
        },
        {
          "rank": 14,
          "chunks": [
            {
              "chunk": 0,
              "contributors": [
                14
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                14
              ]
            },
            {
              "chunk": 2,
              "contributors": [
                14
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                14
              ]
            },
            {
              "chunk": 4,
              "contributors": [
                14
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                14
              ]
            },
            {
              "chunk": 6,
              "contributors": [
                14
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                14
              ]
            },
            {
              "chunk": 8,
              "contributors": [
                14
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                14
              ]
            },
            {
              "chunk": 10,
              "contributors": [
                14
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                14
              ]
            },
            {
              "chunk": 12,
              "contributors": [
                14
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                14
              ]
            },
            {
              "chunk": 14,
              "contributors": [
                14
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                14
              ]
            }
          ]
        },
        {
          "rank": 15,
          "chunks": [
            {
              "chunk": 0,
              "contributors": [
                15
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                15
              ]
            },
            {
              "chunk": 2,
              "contributors": [
                15
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                15
              ]
            },
            {
              "chunk": 4,
              "contributors": [
                15
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                15
              ]
            },
            {
              "chunk": 6,
              "contributors": [
                15
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                15
              ]
            },
            {
              "chunk": 8,
              "contributors": [
                15
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                15
              ]
            },
            {
              "chunk": 10,
              "contributors": [
                15
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                15
              ]
            },
            {
              "chunk": 12,
              "contributors": [
                15
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                15
              ]
            },
            {
              "chunk": 14,
              "contributors": [
                15
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                15
              ]
            }
          ]
        }
      ]
    },
    {
      "after": "local_reduce_scatter:reduce_scatter",
      "round_count": 7,
      "ranks": [
        {
          "rank": 0,
          "chunks": [
            {
              "chunk": 2,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7
              ]
            }
          ]
        },
        {
          "rank": 1,
          "chunks": [
            {
              "chunk": 4,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7
              ]
            }
          ]
        },
        {
          "rank": 2,
          "chunks": [
            {
              "chunk": 6,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7
              ]
            }
          ]
        },
        {
          "rank": 3,
          "chunks": [
            {
              "chunk": 8,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7
              ]
            }
          ]
        },
        {
          "rank": 4,
          "chunks": [
            {
              "chunk": 10,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7
              ]
            }
          ]
        },
        {
          "rank": 5,
          "chunks": [
            {
              "chunk": 12,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7
              ]
            }
          ]
        },
        {
          "rank": 6,
          "chunks": [
            {
              "chunk": 14,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7
              ]
            }
          ]
        },
        {
          "rank": 7,
          "chunks": [
            {
              "chunk": 0,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7
              ]
            }
          ]
        },
        {
          "rank": 8,
          "chunks": [
            {
              "chunk": 2,
              "contributors": [
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 9,
          "chunks": [
            {
              "chunk": 4,
              "contributors": [
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 10,
          "chunks": [
            {
              "chunk": 6,
              "contributors": [
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 11,
          "chunks": [
            {
              "chunk": 8,
              "contributors": [
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 12,
          "chunks": [
            {
              "chunk": 10,
              "contributors": [
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 13,
          "chunks": [
            {
              "chunk": 12,
              "contributors": [
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 14,
          "chunks": [
            {
              "chunk": 14,
              "contributors": [
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 15,
          "chunks": [
            {
              "chunk": 0,
              "contributors": [
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        }
      ]
    },
    {
      "after": "cross_server_allreduce:reduce_scatter",
      "round_count": 8,
      "ranks": [
        {
          "rank": 0,
          "chunks": [
            {
              "chunk": 3,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 1,
          "chunks": [
            {
              "chunk": 5,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 2,
          "chunks": [
            {
              "chunk": 7,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 3,
          "chunks": [
            {
              "chunk": 9,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 4,
          "chunks": [
            {
              "chunk": 11,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 5,
          "chunks": [
            {
              "chunk": 13,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 6,
          "chunks": [
            {
              "chunk": 15,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 7,
          "chunks": [
            {
              "chunk": 1,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 8,
          "chunks": [
            {
              "chunk": 2,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 9,
          "chunks": [
            {
              "chunk": 4,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 10,
          "chunks": [
            {
              "chunk": 6,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 11,
          "chunks": [
            {
              "chunk": 8,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 12,
          "chunks": [
            {
              "chunk": 10,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 13,
          "chunks": [
            {
              "chunk": 12,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 14,
          "chunks": [
            {
              "chunk": 14,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 15,
          "chunks": [
            {
              "chunk": 0,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        }
      ]
    },
    {
      "after": "cross_server_allreduce:all_gather",
      "round_count": 9,
      "ranks": [
        {
          "rank": 0,
          "chunks": [
            {
              "chunk": 2,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 1,
          "chunks": [
            {
              "chunk": 4,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 2,
          "chunks": [
            {
              "chunk": 6,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 3,
          "chunks": [
            {
              "chunk": 8,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 4,
          "chunks": [
            {
              "chunk": 10,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 5,
          "chunks": [
            {
              "chunk": 12,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 6,
          "chunks": [
            {
              "chunk": 14,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 7,
          "chunks": [
            {
              "chunk": 0,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 8,
          "chunks": [
            {
              "chunk": 2,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 9,
          "chunks": [
            {
              "chunk": 4,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 10,
          "chunks": [
            {
              "chunk": 6,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 11,
          "chunks": [
            {
              "chunk": 8,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 12,
          "chunks": [
            {
              "chunk": 10,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 13,
          "chunks": [
            {
              "chunk": 12,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 14,
          "chunks": [
            {
              "chunk": 14,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 15,
          "chunks": [
            {
              "chunk": 0,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        }
      ]
    },
    {
      "after": "local_all_gather:all_gather",
      "round_count": 16,
      "ranks": [
        {
          "rank": 0,
          "chunks": [
            {
              "chunk": 0,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 2,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 4,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 6,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 8,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 10,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 12,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 14,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 1,
          "chunks": [
            {
              "chunk": 0,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 2,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 4,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 6,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 8,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 10,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 12,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 14,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 2,
          "chunks": [
            {
              "chunk": 0,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 2,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 4,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 6,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 8,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 10,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 12,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 14,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 3,
          "chunks": [
            {
              "chunk": 0,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 2,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 4,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 6,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 8,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 10,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 12,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 14,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 4,
          "chunks": [
            {
              "chunk": 0,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 2,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 4,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 6,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 8,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 10,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 12,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 14,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 5,
          "chunks": [
            {
              "chunk": 0,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 2,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 4,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 6,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 8,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 10,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 12,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 14,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 6,
          "chunks": [
            {
              "chunk": 0,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 2,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 4,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 6,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 8,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 10,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 12,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 14,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 7,
          "chunks": [
            {
              "chunk": 0,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 2,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 4,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 6,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 8,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 10,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 12,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 14,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 8,
          "chunks": [
            {
              "chunk": 0,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 2,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 4,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 6,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 8,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 10,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 12,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 14,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 9,
          "chunks": [
            {
              "chunk": 0,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 2,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 4,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 6,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 8,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 10,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 12,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 14,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 10,
          "chunks": [
            {
              "chunk": 0,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 2,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 4,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 6,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 8,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 10,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 12,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 14,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 11,
          "chunks": [
            {
              "chunk": 0,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 2,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 4,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 6,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 8,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 10,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 12,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 14,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 12,
          "chunks": [
            {
              "chunk": 0,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 2,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 4,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 6,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 8,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 10,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 12,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 14,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 13,
          "chunks": [
            {
              "chunk": 0,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 2,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 4,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 6,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 8,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 10,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 12,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 14,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 14,
          "chunks": [
            {
              "chunk": 0,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 2,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 4,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 6,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 8,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 10,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 12,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 14,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        },
        {
          "rank": 15,
          "chunks": [
            {
              "chunk": 0,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 1,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 2,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 3,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 4,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 5,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 6,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 7,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 8,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 9,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 10,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 11,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 12,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 13,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 14,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            },
            {
              "chunk": 15,
              "contributors": [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
              ]
            }
          ]
        }
      ]
    }
  ],
  "resources": [
    {
      "resource": "cut.0->1",
      "bytes": 100663296,
      "bandwidth_bytes_per_second": 400000000000,
      "service_seconds_exact": "12288/48828125"
    },
    {
      "resource": "cut.1->0",
      "bytes": 100663296,
      "bandwidth_bytes_per_second": 400000000000,
      "service_seconds_exact": "12288/48828125"
    },
    {
      "resource": "local.0->1",
      "bytes": 176160768,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "57344/146484375"
    },
    {
      "resource": "local.1->2",
      "bytes": 176160768,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "57344/146484375"
    },
    {
      "resource": "local.10->11",
      "bytes": 176160768,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "57344/146484375"
    },
    {
      "resource": "local.11->12",
      "bytes": 176160768,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "57344/146484375"
    },
    {
      "resource": "local.12->13",
      "bytes": 176160768,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "57344/146484375"
    },
    {
      "resource": "local.13->14",
      "bytes": 176160768,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "57344/146484375"
    },
    {
      "resource": "local.14->15",
      "bytes": 176160768,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "57344/146484375"
    },
    {
      "resource": "local.15->8",
      "bytes": 176160768,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "57344/146484375"
    },
    {
      "resource": "local.2->3",
      "bytes": 176160768,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "57344/146484375"
    },
    {
      "resource": "local.3->4",
      "bytes": 176160768,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "57344/146484375"
    },
    {
      "resource": "local.4->5",
      "bytes": 176160768,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "57344/146484375"
    },
    {
      "resource": "local.5->6",
      "bytes": 176160768,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "57344/146484375"
    },
    {
      "resource": "local.6->7",
      "bytes": 176160768,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "57344/146484375"
    },
    {
      "resource": "local.7->0",
      "bytes": 176160768,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "57344/146484375"
    },
    {
      "resource": "local.8->9",
      "bytes": 176160768,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "57344/146484375"
    },
    {
      "resource": "local.9->10",
      "bytes": 176160768,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "57344/146484375"
    },
    {
      "resource": "rank0.rx",
      "bytes": 188743680,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "4096/9765625"
    },
    {
      "resource": "rank0.tx",
      "bytes": 188743680,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "4096/9765625"
    },
    {
      "resource": "rank1.rx",
      "bytes": 188743680,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "4096/9765625"
    },
    {
      "resource": "rank1.tx",
      "bytes": 188743680,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "4096/9765625"
    },
    {
      "resource": "rank10.rx",
      "bytes": 188743680,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "4096/9765625"
    },
    {
      "resource": "rank10.tx",
      "bytes": 188743680,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "4096/9765625"
    },
    {
      "resource": "rank11.rx",
      "bytes": 188743680,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "4096/9765625"
    },
    {
      "resource": "rank11.tx",
      "bytes": 188743680,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "4096/9765625"
    },
    {
      "resource": "rank12.rx",
      "bytes": 188743680,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "4096/9765625"
    },
    {
      "resource": "rank12.tx",
      "bytes": 188743680,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "4096/9765625"
    },
    {
      "resource": "rank13.rx",
      "bytes": 188743680,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "4096/9765625"
    },
    {
      "resource": "rank13.tx",
      "bytes": 188743680,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "4096/9765625"
    },
    {
      "resource": "rank14.rx",
      "bytes": 188743680,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "4096/9765625"
    },
    {
      "resource": "rank14.tx",
      "bytes": 188743680,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "4096/9765625"
    },
    {
      "resource": "rank15.rx",
      "bytes": 188743680,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "4096/9765625"
    },
    {
      "resource": "rank15.tx",
      "bytes": 188743680,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "4096/9765625"
    },
    {
      "resource": "rank2.rx",
      "bytes": 188743680,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "4096/9765625"
    },
    {
      "resource": "rank2.tx",
      "bytes": 188743680,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "4096/9765625"
    },
    {
      "resource": "rank3.rx",
      "bytes": 188743680,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "4096/9765625"
    },
    {
      "resource": "rank3.tx",
      "bytes": 188743680,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "4096/9765625"
    },
    {
      "resource": "rank4.rx",
      "bytes": 188743680,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "4096/9765625"
    },
    {
      "resource": "rank4.tx",
      "bytes": 188743680,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "4096/9765625"
    },
    {
      "resource": "rank5.rx",
      "bytes": 188743680,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "4096/9765625"
    },
    {
      "resource": "rank5.tx",
      "bytes": 188743680,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "4096/9765625"
    },
    {
      "resource": "rank6.rx",
      "bytes": 188743680,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "4096/9765625"
    },
    {
      "resource": "rank6.tx",
      "bytes": 188743680,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "4096/9765625"
    },
    {
      "resource": "rank7.rx",
      "bytes": 188743680,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "4096/9765625"
    },
    {
      "resource": "rank7.tx",
      "bytes": 188743680,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "4096/9765625"
    },
    {
      "resource": "rank8.rx",
      "bytes": 188743680,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "4096/9765625"
    },
    {
      "resource": "rank8.tx",
      "bytes": 188743680,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "4096/9765625"
    },
    {
      "resource": "rank9.rx",
      "bytes": 188743680,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "4096/9765625"
    },
    {
      "resource": "rank9.tx",
      "bytes": 188743680,
      "bandwidth_bytes_per_second": 450000000000,
      "service_seconds_exact": "4096/9765625"
    },
    {
      "resource": "server0.nic0.rx",
      "bytes": 12582912,
      "bandwidth_bytes_per_second": 50000000000,
      "service_seconds_exact": "12288/48828125"
    },
    {
      "resource": "server0.nic0.tx",
      "bytes": 12582912,
      "bandwidth_bytes_per_second": 50000000000,
      "service_seconds_exact": "12288/48828125"
    },
    {
      "resource": "server0.nic1.rx",
      "bytes": 12582912,
      "bandwidth_bytes_per_second": 50000000000,
      "service_seconds_exact": "12288/48828125"
    },
    {
      "resource": "server0.nic1.tx",
      "bytes": 12582912,
      "bandwidth_bytes_per_second": 50000000000,
      "service_seconds_exact": "12288/48828125"
    },
    {
      "resource": "server0.nic2.rx",
      "bytes": 12582912,
      "bandwidth_bytes_per_second": 50000000000,
      "service_seconds_exact": "12288/48828125"
    },
    {
      "resource": "server0.nic2.tx",
      "bytes": 12582912,
      "bandwidth_bytes_per_second": 50000000000,
      "service_seconds_exact": "12288/48828125"
    },
    {
      "resource": "server0.nic3.rx",
      "bytes": 12582912,
      "bandwidth_bytes_per_second": 50000000000,
      "service_seconds_exact": "12288/48828125"
    },
    {
      "resource": "server0.nic3.tx",
      "bytes": 12582912,
      "bandwidth_bytes_per_second": 50000000000,
      "service_seconds_exact": "12288/48828125"
    },
    {
      "resource": "server0.nic4.rx",
      "bytes": 12582912,
      "bandwidth_bytes_per_second": 50000000000,
      "service_seconds_exact": "12288/48828125"
    },
    {
      "resource": "server0.nic4.tx",
      "bytes": 12582912,
      "bandwidth_bytes_per_second": 50000000000,
      "service_seconds_exact": "12288/48828125"
    },
    {
      "resource": "server0.nic5.rx",
      "bytes": 12582912,
      "bandwidth_bytes_per_second": 50000000000,
      "service_seconds_exact": "12288/48828125"
    },
    {
      "resource": "server0.nic5.tx",
      "bytes": 12582912,
      "bandwidth_bytes_per_second": 50000000000,
      "service_seconds_exact": "12288/48828125"
    },
    {
      "resource": "server0.nic6.rx",
      "bytes": 12582912,
      "bandwidth_bytes_per_second": 50000000000,
      "service_seconds_exact": "12288/48828125"
    },
    {
      "resource": "server0.nic6.tx",
      "bytes": 12582912,
      "bandwidth_bytes_per_second": 50000000000,
      "service_seconds_exact": "12288/48828125"
    },
    {
      "resource": "server0.nic7.rx",
      "bytes": 12582912,
      "bandwidth_bytes_per_second": 50000000000,
      "service_seconds_exact": "12288/48828125"
    },
    {
      "resource": "server0.nic7.tx",
      "bytes": 12582912,
      "bandwidth_bytes_per_second": 50000000000,
      "service_seconds_exact": "12288/48828125"
    },
    {
      "resource": "server1.nic0.rx",
      "bytes": 12582912,
      "bandwidth_bytes_per_second": 50000000000,
      "service_seconds_exact": "12288/48828125"
    },
    {
      "resource": "server1.nic0.tx",
      "bytes": 12582912,
      "bandwidth_bytes_per_second": 50000000000,
      "service_seconds_exact": "12288/48828125"
    },
    {
      "resource": "server1.nic1.rx",
      "bytes": 12582912,
      "bandwidth_bytes_per_second": 50000000000,
      "service_seconds_exact": "12288/48828125"
    },
    {
      "resource": "server1.nic1.tx",
      "bytes": 12582912,
      "bandwidth_bytes_per_second": 50000000000,
      "service_seconds_exact": "12288/48828125"
    },
    {
      "resource": "server1.nic2.rx",
      "bytes": 12582912,
      "bandwidth_bytes_per_second": 50000000000,
      "service_seconds_exact": "12288/48828125"
    },
    {
      "resource": "server1.nic2.tx",
      "bytes": 12582912,
      "bandwidth_bytes_per_second": 50000000000,
      "service_seconds_exact": "12288/48828125"
    },
    {
      "resource": "server1.nic3.rx",
      "bytes": 12582912,
      "bandwidth_bytes_per_second": 50000000000,
      "service_seconds_exact": "12288/48828125"
    },
    {
      "resource": "server1.nic3.tx",
      "bytes": 12582912,
      "bandwidth_bytes_per_second": 50000000000,
      "service_seconds_exact": "12288/48828125"
    },
    {
      "resource": "server1.nic4.rx",
      "bytes": 12582912,
      "bandwidth_bytes_per_second": 50000000000,
      "service_seconds_exact": "12288/48828125"
    },
    {
      "resource": "server1.nic4.tx",
      "bytes": 12582912,
      "bandwidth_bytes_per_second": 50000000000,
      "service_seconds_exact": "12288/48828125"
    },
    {
      "resource": "server1.nic5.rx",
      "bytes": 12582912,
      "bandwidth_bytes_per_second": 50000000000,
      "service_seconds_exact": "12288/48828125"
    },
    {
      "resource": "server1.nic5.tx",
      "bytes": 12582912,
      "bandwidth_bytes_per_second": 50000000000,
      "service_seconds_exact": "12288/48828125"
    },
    {
      "resource": "server1.nic6.rx",
      "bytes": 12582912,
      "bandwidth_bytes_per_second": 50000000000,
      "service_seconds_exact": "12288/48828125"
    },
    {
      "resource": "server1.nic6.tx",
      "bytes": 12582912,
      "bandwidth_bytes_per_second": 50000000000,
      "service_seconds_exact": "12288/48828125"
    },
    {
      "resource": "server1.nic7.rx",
      "bytes": 12582912,
      "bandwidth_bytes_per_second": 50000000000,
      "service_seconds_exact": "12288/48828125"
    },
    {
      "resource": "server1.nic7.tx",
      "bytes": 12582912,
      "bandwidth_bytes_per_second": 50000000000,
      "service_seconds_exact": "12288/48828125"
    },
    {
      "resource": "shared_cut.bidirectional",
      "bytes": 201326592,
      "bandwidth_bytes_per_second": 800000000000,
      "service_seconds_exact": "12288/48828125"
    }
  ],
  "stages": [
    {
      "stage": "local_reduce_scatter",
      "rounds": 7,
      "send_bytes": 1409286144,
      "remote_send_bytes": 0,
      "barrier_lower_seconds_exact": "15117389/75000000000"
    },
    {
      "stage": "cross_server_allreduce",
      "rounds": 2,
      "send_bytes": 201326592,
      "remote_send_bytes": 201326592,
      "barrier_lower_seconds_exact": "3166553/12500000000"
    },
    {
      "stage": "local_all_gather",
      "rounds": 7,
      "send_bytes": 1409286144,
      "remote_send_bytes": 0,
      "barrier_lower_seconds_exact": "15117389/75000000000"
    }
  ],
  "traffic_account": {
    "logical_send_bytes": 3019898880,
    "resources": [
      {
        "resource": "cut.0->1",
        "bytes": 100663296,
        "bandwidth_bytes_per_second": 400000000000,
        "service_seconds": 0.00025165824
      },
      {
        "resource": "cut.1->0",
        "bytes": 100663296,
        "bandwidth_bytes_per_second": 400000000000,
        "service_seconds": 0.00025165824
      },
      {
        "resource": "local.0->1",
        "bytes": 176160768,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.00039146837333333334
      },
      {
        "resource": "local.1->2",
        "bytes": 176160768,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.00039146837333333334
      },
      {
        "resource": "local.10->11",
        "bytes": 176160768,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.00039146837333333334
      },
      {
        "resource": "local.11->12",
        "bytes": 176160768,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.00039146837333333334
      },
      {
        "resource": "local.12->13",
        "bytes": 176160768,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.00039146837333333334
      },
      {
        "resource": "local.13->14",
        "bytes": 176160768,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.00039146837333333334
      },
      {
        "resource": "local.14->15",
        "bytes": 176160768,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.00039146837333333334
      },
      {
        "resource": "local.15->8",
        "bytes": 176160768,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.00039146837333333334
      },
      {
        "resource": "local.2->3",
        "bytes": 176160768,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.00039146837333333334
      },
      {
        "resource": "local.3->4",
        "bytes": 176160768,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.00039146837333333334
      },
      {
        "resource": "local.4->5",
        "bytes": 176160768,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.00039146837333333334
      },
      {
        "resource": "local.5->6",
        "bytes": 176160768,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.00039146837333333334
      },
      {
        "resource": "local.6->7",
        "bytes": 176160768,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.00039146837333333334
      },
      {
        "resource": "local.7->0",
        "bytes": 176160768,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.00039146837333333334
      },
      {
        "resource": "local.8->9",
        "bytes": 176160768,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.00039146837333333334
      },
      {
        "resource": "local.9->10",
        "bytes": 176160768,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.00039146837333333334
      },
      {
        "resource": "rank0.rx",
        "bytes": 188743680,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.0004194304
      },
      {
        "resource": "rank0.tx",
        "bytes": 188743680,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.0004194304
      },
      {
        "resource": "rank1.rx",
        "bytes": 188743680,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.0004194304
      },
      {
        "resource": "rank1.tx",
        "bytes": 188743680,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.0004194304
      },
      {
        "resource": "rank10.rx",
        "bytes": 188743680,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.0004194304
      },
      {
        "resource": "rank10.tx",
        "bytes": 188743680,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.0004194304
      },
      {
        "resource": "rank11.rx",
        "bytes": 188743680,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.0004194304
      },
      {
        "resource": "rank11.tx",
        "bytes": 188743680,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.0004194304
      },
      {
        "resource": "rank12.rx",
        "bytes": 188743680,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.0004194304
      },
      {
        "resource": "rank12.tx",
        "bytes": 188743680,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.0004194304
      },
      {
        "resource": "rank13.rx",
        "bytes": 188743680,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.0004194304
      },
      {
        "resource": "rank13.tx",
        "bytes": 188743680,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.0004194304
      },
      {
        "resource": "rank14.rx",
        "bytes": 188743680,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.0004194304
      },
      {
        "resource": "rank14.tx",
        "bytes": 188743680,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.0004194304
      },
      {
        "resource": "rank15.rx",
        "bytes": 188743680,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.0004194304
      },
      {
        "resource": "rank15.tx",
        "bytes": 188743680,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.0004194304
      },
      {
        "resource": "rank2.rx",
        "bytes": 188743680,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.0004194304
      },
      {
        "resource": "rank2.tx",
        "bytes": 188743680,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.0004194304
      },
      {
        "resource": "rank3.rx",
        "bytes": 188743680,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.0004194304
      },
      {
        "resource": "rank3.tx",
        "bytes": 188743680,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.0004194304
      },
      {
        "resource": "rank4.rx",
        "bytes": 188743680,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.0004194304
      },
      {
        "resource": "rank4.tx",
        "bytes": 188743680,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.0004194304
      },
      {
        "resource": "rank5.rx",
        "bytes": 188743680,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.0004194304
      },
      {
        "resource": "rank5.tx",
        "bytes": 188743680,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.0004194304
      },
      {
        "resource": "rank6.rx",
        "bytes": 188743680,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.0004194304
      },
      {
        "resource": "rank6.tx",
        "bytes": 188743680,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.0004194304
      },
      {
        "resource": "rank7.rx",
        "bytes": 188743680,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.0004194304
      },
      {
        "resource": "rank7.tx",
        "bytes": 188743680,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.0004194304
      },
      {
        "resource": "rank8.rx",
        "bytes": 188743680,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.0004194304
      },
      {
        "resource": "rank8.tx",
        "bytes": 188743680,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.0004194304
      },
      {
        "resource": "rank9.rx",
        "bytes": 188743680,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.0004194304
      },
      {
        "resource": "rank9.tx",
        "bytes": 188743680,
        "bandwidth_bytes_per_second": 450000000000,
        "service_seconds": 0.0004194304
      },
      {
        "resource": "server0.nic0.rx",
        "bytes": 12582912,
        "bandwidth_bytes_per_second": 50000000000,
        "service_seconds": 0.00025165824
      },
      {
        "resource": "server0.nic0.tx",
        "bytes": 12582912,
        "bandwidth_bytes_per_second": 50000000000,
        "service_seconds": 0.00025165824
      },
      {
        "resource": "server0.nic1.rx",
        "bytes": 12582912,
        "bandwidth_bytes_per_second": 50000000000,
        "service_seconds": 0.00025165824
      },
      {
        "resource": "server0.nic1.tx",
        "bytes": 12582912,
        "bandwidth_bytes_per_second": 50000000000,
        "service_seconds": 0.00025165824
      },
      {
        "resource": "server0.nic2.rx",
        "bytes": 12582912,
        "bandwidth_bytes_per_second": 50000000000,
        "service_seconds": 0.00025165824
      },
      {
        "resource": "server0.nic2.tx",
        "bytes": 12582912,
        "bandwidth_bytes_per_second": 50000000000,
        "service_seconds": 0.00025165824
      },
      {
        "resource": "server0.nic3.rx",
        "bytes": 12582912,
        "bandwidth_bytes_per_second": 50000000000,
        "service_seconds": 0.00025165824
      },
      {
        "resource": "server0.nic3.tx",
        "bytes": 12582912,
        "bandwidth_bytes_per_second": 50000000000,
        "service_seconds": 0.00025165824
      },
      {
        "resource": "server0.nic4.rx",
        "bytes": 12582912,
        "bandwidth_bytes_per_second": 50000000000,
        "service_seconds": 0.00025165824
      },
      {
        "resource": "server0.nic4.tx",
        "bytes": 12582912,
        "bandwidth_bytes_per_second": 50000000000,
        "service_seconds": 0.00025165824
      },
      {
        "resource": "server0.nic5.rx",
        "bytes": 12582912,
        "bandwidth_bytes_per_second": 50000000000,
        "service_seconds": 0.00025165824
      },
      {
        "resource": "server0.nic5.tx",
        "bytes": 12582912,
        "bandwidth_bytes_per_second": 50000000000,
        "service_seconds": 0.00025165824
      },
      {
        "resource": "server0.nic6.rx",
        "bytes": 12582912,
        "bandwidth_bytes_per_second": 50000000000,
        "service_seconds": 0.00025165824
      },
      {
        "resource": "server0.nic6.tx",
        "bytes": 12582912,
        "bandwidth_bytes_per_second": 50000000000,
        "service_seconds": 0.00025165824
      },
      {
        "resource": "server0.nic7.rx",
        "bytes": 12582912,
        "bandwidth_bytes_per_second": 50000000000,
        "service_seconds": 0.00025165824
      },
      {
        "resource": "server0.nic7.tx",
        "bytes": 12582912,
        "bandwidth_bytes_per_second": 50000000000,
        "service_seconds": 0.00025165824
      },
      {
        "resource": "server1.nic0.rx",
        "bytes": 12582912,
        "bandwidth_bytes_per_second": 50000000000,
        "service_seconds": 0.00025165824
      },
      {
        "resource": "server1.nic0.tx",
        "bytes": 12582912,
        "bandwidth_bytes_per_second": 50000000000,
        "service_seconds": 0.00025165824
      },
      {
        "resource": "server1.nic1.rx",
        "bytes": 12582912,
        "bandwidth_bytes_per_second": 50000000000,
        "service_seconds": 0.00025165824
      },
      {
        "resource": "server1.nic1.tx",
        "bytes": 12582912,
        "bandwidth_bytes_per_second": 50000000000,
        "service_seconds": 0.00025165824
      },
      {
        "resource": "server1.nic2.rx",
        "bytes": 12582912,
        "bandwidth_bytes_per_second": 50000000000,
        "service_seconds": 0.00025165824
      },
      {
        "resource": "server1.nic2.tx",
        "bytes": 12582912,
        "bandwidth_bytes_per_second": 50000000000,
        "service_seconds": 0.00025165824
      },
      {
        "resource": "server1.nic3.rx",
        "bytes": 12582912,
        "bandwidth_bytes_per_second": 50000000000,
        "service_seconds": 0.00025165824
      },
      {
        "resource": "server1.nic3.tx",
        "bytes": 12582912,
        "bandwidth_bytes_per_second": 50000000000,
        "service_seconds": 0.00025165824
      },
      {
        "resource": "server1.nic4.rx",
        "bytes": 12582912,
        "bandwidth_bytes_per_second": 50000000000,
        "service_seconds": 0.00025165824
      },
      {
        "resource": "server1.nic4.tx",
        "bytes": 12582912,
        "bandwidth_bytes_per_second": 50000000000,
        "service_seconds": 0.00025165824
      },
      {
        "resource": "server1.nic5.rx",
        "bytes": 12582912,
        "bandwidth_bytes_per_second": 50000000000,
        "service_seconds": 0.00025165824
      },
      {
        "resource": "server1.nic5.tx",
        "bytes": 12582912,
        "bandwidth_bytes_per_second": 50000000000,
        "service_seconds": 0.00025165824
      },
      {
        "resource": "server1.nic6.rx",
        "bytes": 12582912,
        "bandwidth_bytes_per_second": 50000000000,
        "service_seconds": 0.00025165824
      },
      {
        "resource": "server1.nic6.tx",
        "bytes": 12582912,
        "bandwidth_bytes_per_second": 50000000000,
        "service_seconds": 0.00025165824
      },
      {
        "resource": "server1.nic7.rx",
        "bytes": 12582912,
        "bandwidth_bytes_per_second": 50000000000,
        "service_seconds": 0.00025165824
      },
      {
        "resource": "server1.nic7.tx",
        "bytes": 12582912,
        "bandwidth_bytes_per_second": 50000000000,
        "service_seconds": 0.00025165824
      },
      {
        "resource": "shared_cut.bidirectional",
        "bytes": 201326592,
        "bandwidth_bytes_per_second": 800000000000,
        "service_seconds": 0.00025165824
      }
    ],
    "rounds": [
      {
        "round": 0,
        "phase": "reduce_scatter",
        "resource_bytes": {
          "rank0.tx": 12582912,
          "local.0->1": 12582912,
          "rank1.rx": 12582912,
          "rank1.tx": 12582912,
          "local.1->2": 12582912,
          "rank2.rx": 12582912,
          "rank2.tx": 12582912,
          "local.2->3": 12582912,
          "rank3.rx": 12582912,
          "rank3.tx": 12582912,
          "local.3->4": 12582912,
          "rank4.rx": 12582912,
          "rank4.tx": 12582912,
          "local.4->5": 12582912,
          "rank5.rx": 12582912,
          "rank5.tx": 12582912,
          "local.5->6": 12582912,
          "rank6.rx": 12582912,
          "rank6.tx": 12582912,
          "local.6->7": 12582912,
          "rank7.rx": 12582912,
          "rank7.tx": 12582912,
          "local.7->0": 12582912,
          "rank0.rx": 12582912,
          "rank8.tx": 12582912,
          "local.8->9": 12582912,
          "rank9.rx": 12582912,
          "rank9.tx": 12582912,
          "local.9->10": 12582912,
          "rank10.rx": 12582912,
          "rank10.tx": 12582912,
          "local.10->11": 12582912,
          "rank11.rx": 12582912,
          "rank11.tx": 12582912,
          "local.11->12": 12582912,
          "rank12.rx": 12582912,
          "rank12.tx": 12582912,
          "local.12->13": 12582912,
          "rank13.rx": 12582912,
          "rank13.tx": 12582912,
          "local.13->14": 12582912,
          "rank14.rx": 12582912,
          "rank14.tx": 12582912,
          "local.14->15": 12582912,
          "rank15.rx": 12582912,
          "rank15.tx": 12582912,
          "local.15->8": 12582912,
          "rank8.rx": 12582912
        },
        "resource_lower_seconds": 2.7962026666666665e-05,
        "barrier_lower_with_startup_seconds": 2.8795026666666665e-05
      },
      {
        "round": 1,
        "phase": "reduce_scatter",
        "resource_bytes": {
          "rank0.tx": 12582912,
          "local.0->1": 12582912,
          "rank1.rx": 12582912,
          "rank1.tx": 12582912,
          "local.1->2": 12582912,
          "rank2.rx": 12582912,
          "rank2.tx": 12582912,
          "local.2->3": 12582912,
          "rank3.rx": 12582912,
          "rank3.tx": 12582912,
          "local.3->4": 12582912,
          "rank4.rx": 12582912,
          "rank4.tx": 12582912,
          "local.4->5": 12582912,
          "rank5.rx": 12582912,
          "rank5.tx": 12582912,
          "local.5->6": 12582912,
          "rank6.rx": 12582912,
          "rank6.tx": 12582912,
          "local.6->7": 12582912,
          "rank7.rx": 12582912,
          "rank7.tx": 12582912,
          "local.7->0": 12582912,
          "rank0.rx": 12582912,
          "rank8.tx": 12582912,
          "local.8->9": 12582912,
          "rank9.rx": 12582912,
          "rank9.tx": 12582912,
          "local.9->10": 12582912,
          "rank10.rx": 12582912,
          "rank10.tx": 12582912,
          "local.10->11": 12582912,
          "rank11.rx": 12582912,
          "rank11.tx": 12582912,
          "local.11->12": 12582912,
          "rank12.rx": 12582912,
          "rank12.tx": 12582912,
          "local.12->13": 12582912,
          "rank13.rx": 12582912,
          "rank13.tx": 12582912,
          "local.13->14": 12582912,
          "rank14.rx": 12582912,
          "rank14.tx": 12582912,
          "local.14->15": 12582912,
          "rank15.rx": 12582912,
          "rank15.tx": 12582912,
          "local.15->8": 12582912,
          "rank8.rx": 12582912
        },
        "resource_lower_seconds": 2.7962026666666665e-05,
        "barrier_lower_with_startup_seconds": 2.8795026666666665e-05
      },
      {
        "round": 2,
        "phase": "reduce_scatter",
        "resource_bytes": {
          "rank0.tx": 12582912,
          "local.0->1": 12582912,
          "rank1.rx": 12582912,
          "rank1.tx": 12582912,
          "local.1->2": 12582912,
          "rank2.rx": 12582912,
          "rank2.tx": 12582912,
          "local.2->3": 12582912,
          "rank3.rx": 12582912,
          "rank3.tx": 12582912,
          "local.3->4": 12582912,
          "rank4.rx": 12582912,
          "rank4.tx": 12582912,
          "local.4->5": 12582912,
          "rank5.rx": 12582912,
          "rank5.tx": 12582912,
          "local.5->6": 12582912,
          "rank6.rx": 12582912,
          "rank6.tx": 12582912,
          "local.6->7": 12582912,
          "rank7.rx": 12582912,
          "rank7.tx": 12582912,
          "local.7->0": 12582912,
          "rank0.rx": 12582912,
          "rank8.tx": 12582912,
          "local.8->9": 12582912,
          "rank9.rx": 12582912,
          "rank9.tx": 12582912,
          "local.9->10": 12582912,
          "rank10.rx": 12582912,
          "rank10.tx": 12582912,
          "local.10->11": 12582912,
          "rank11.rx": 12582912,
          "rank11.tx": 12582912,
          "local.11->12": 12582912,
          "rank12.rx": 12582912,
          "rank12.tx": 12582912,
          "local.12->13": 12582912,
          "rank13.rx": 12582912,
          "rank13.tx": 12582912,
          "local.13->14": 12582912,
          "rank14.rx": 12582912,
          "rank14.tx": 12582912,
          "local.14->15": 12582912,
          "rank15.rx": 12582912,
          "rank15.tx": 12582912,
          "local.15->8": 12582912,
          "rank8.rx": 12582912
        },
        "resource_lower_seconds": 2.7962026666666665e-05,
        "barrier_lower_with_startup_seconds": 2.8795026666666665e-05
      },
      {
        "round": 3,
        "phase": "reduce_scatter",
        "resource_bytes": {
          "rank0.tx": 12582912,
          "local.0->1": 12582912,
          "rank1.rx": 12582912,
          "rank1.tx": 12582912,
          "local.1->2": 12582912,
          "rank2.rx": 12582912,
          "rank2.tx": 12582912,
          "local.2->3": 12582912,
          "rank3.rx": 12582912,
          "rank3.tx": 12582912,
          "local.3->4": 12582912,
          "rank4.rx": 12582912,
          "rank4.tx": 12582912,
          "local.4->5": 12582912,
          "rank5.rx": 12582912,
          "rank5.tx": 12582912,
          "local.5->6": 12582912,
          "rank6.rx": 12582912,
          "rank6.tx": 12582912,
          "local.6->7": 12582912,
          "rank7.rx": 12582912,
          "rank7.tx": 12582912,
          "local.7->0": 12582912,
          "rank0.rx": 12582912,
          "rank8.tx": 12582912,
          "local.8->9": 12582912,
          "rank9.rx": 12582912,
          "rank9.tx": 12582912,
          "local.9->10": 12582912,
          "rank10.rx": 12582912,
          "rank10.tx": 12582912,
          "local.10->11": 12582912,
          "rank11.rx": 12582912,
          "rank11.tx": 12582912,
          "local.11->12": 12582912,
          "rank12.rx": 12582912,
          "rank12.tx": 12582912,
          "local.12->13": 12582912,
          "rank13.rx": 12582912,
          "rank13.tx": 12582912,
          "local.13->14": 12582912,
          "rank14.rx": 12582912,
          "rank14.tx": 12582912,
          "local.14->15": 12582912,
          "rank15.rx": 12582912,
          "rank15.tx": 12582912,
          "local.15->8": 12582912,
          "rank8.rx": 12582912
        },
        "resource_lower_seconds": 2.7962026666666665e-05,
        "barrier_lower_with_startup_seconds": 2.8795026666666665e-05
      },
      {
        "round": 4,
        "phase": "reduce_scatter",
        "resource_bytes": {
          "rank0.tx": 12582912,
          "local.0->1": 12582912,
          "rank1.rx": 12582912,
          "rank1.tx": 12582912,
          "local.1->2": 12582912,
          "rank2.rx": 12582912,
          "rank2.tx": 12582912,
          "local.2->3": 12582912,
          "rank3.rx": 12582912,
          "rank3.tx": 12582912,
          "local.3->4": 12582912,
          "rank4.rx": 12582912,
          "rank4.tx": 12582912,
          "local.4->5": 12582912,
          "rank5.rx": 12582912,
          "rank5.tx": 12582912,
          "local.5->6": 12582912,
          "rank6.rx": 12582912,
          "rank6.tx": 12582912,
          "local.6->7": 12582912,
          "rank7.rx": 12582912,
          "rank7.tx": 12582912,
          "local.7->0": 12582912,
          "rank0.rx": 12582912,
          "rank8.tx": 12582912,
          "local.8->9": 12582912,
          "rank9.rx": 12582912,
          "rank9.tx": 12582912,
          "local.9->10": 12582912,
          "rank10.rx": 12582912,
          "rank10.tx": 12582912,
          "local.10->11": 12582912,
          "rank11.rx": 12582912,
          "rank11.tx": 12582912,
          "local.11->12": 12582912,
          "rank12.rx": 12582912,
          "rank12.tx": 12582912,
          "local.12->13": 12582912,
          "rank13.rx": 12582912,
          "rank13.tx": 12582912,
          "local.13->14": 12582912,
          "rank14.rx": 12582912,
          "rank14.tx": 12582912,
          "local.14->15": 12582912,
          "rank15.rx": 12582912,
          "rank15.tx": 12582912,
          "local.15->8": 12582912,
          "rank8.rx": 12582912
        },
        "resource_lower_seconds": 2.7962026666666665e-05,
        "barrier_lower_with_startup_seconds": 2.8795026666666665e-05
      },
      {
        "round": 5,
        "phase": "reduce_scatter",
        "resource_bytes": {
          "rank0.tx": 12582912,
          "local.0->1": 12582912,
          "rank1.rx": 12582912,
          "rank1.tx": 12582912,
          "local.1->2": 12582912,
          "rank2.rx": 12582912,
          "rank2.tx": 12582912,
          "local.2->3": 12582912,
          "rank3.rx": 12582912,
          "rank3.tx": 12582912,
          "local.3->4": 12582912,
          "rank4.rx": 12582912,
          "rank4.tx": 12582912,
          "local.4->5": 12582912,
          "rank5.rx": 12582912,
          "rank5.tx": 12582912,
          "local.5->6": 12582912,
          "rank6.rx": 12582912,
          "rank6.tx": 12582912,
          "local.6->7": 12582912,
          "rank7.rx": 12582912,
          "rank7.tx": 12582912,
          "local.7->0": 12582912,
          "rank0.rx": 12582912,
          "rank8.tx": 12582912,
          "local.8->9": 12582912,
          "rank9.rx": 12582912,
          "rank9.tx": 12582912,
          "local.9->10": 12582912,
          "rank10.rx": 12582912,
          "rank10.tx": 12582912,
          "local.10->11": 12582912,
          "rank11.rx": 12582912,
          "rank11.tx": 12582912,
          "local.11->12": 12582912,
          "rank12.rx": 12582912,
          "rank12.tx": 12582912,
          "local.12->13": 12582912,
          "rank13.rx": 12582912,
          "rank13.tx": 12582912,
          "local.13->14": 12582912,
          "rank14.rx": 12582912,
          "rank14.tx": 12582912,
          "local.14->15": 12582912,
          "rank15.rx": 12582912,
          "rank15.tx": 12582912,
          "local.15->8": 12582912,
          "rank8.rx": 12582912
        },
        "resource_lower_seconds": 2.7962026666666665e-05,
        "barrier_lower_with_startup_seconds": 2.8795026666666665e-05
      },
      {
        "round": 6,
        "phase": "reduce_scatter",
        "resource_bytes": {
          "rank0.tx": 12582912,
          "local.0->1": 12582912,
          "rank1.rx": 12582912,
          "rank1.tx": 12582912,
          "local.1->2": 12582912,
          "rank2.rx": 12582912,
          "rank2.tx": 12582912,
          "local.2->3": 12582912,
          "rank3.rx": 12582912,
          "rank3.tx": 12582912,
          "local.3->4": 12582912,
          "rank4.rx": 12582912,
          "rank4.tx": 12582912,
          "local.4->5": 12582912,
          "rank5.rx": 12582912,
          "rank5.tx": 12582912,
          "local.5->6": 12582912,
          "rank6.rx": 12582912,
          "rank6.tx": 12582912,
          "local.6->7": 12582912,
          "rank7.rx": 12582912,
          "rank7.tx": 12582912,
          "local.7->0": 12582912,
          "rank0.rx": 12582912,
          "rank8.tx": 12582912,
          "local.8->9": 12582912,
          "rank9.rx": 12582912,
          "rank9.tx": 12582912,
          "local.9->10": 12582912,
          "rank10.rx": 12582912,
          "rank10.tx": 12582912,
          "local.10->11": 12582912,
          "rank11.rx": 12582912,
          "rank11.tx": 12582912,
          "local.11->12": 12582912,
          "rank12.rx": 12582912,
          "rank12.tx": 12582912,
          "local.12->13": 12582912,
          "rank13.rx": 12582912,
          "rank13.tx": 12582912,
          "local.13->14": 12582912,
          "rank14.rx": 12582912,
          "rank14.tx": 12582912,
          "local.14->15": 12582912,
          "rank15.rx": 12582912,
          "rank15.tx": 12582912,
          "local.15->8": 12582912,
          "rank8.rx": 12582912
        },
        "resource_lower_seconds": 2.7962026666666665e-05,
        "barrier_lower_with_startup_seconds": 2.8795026666666665e-05
      },
      {
        "round": 7,
        "phase": "reduce_scatter",
        "resource_bytes": {
          "rank7.tx": 6291456,
          "server0.nic7.tx": 6291456,
          "cut.0->1": 50331648,
          "shared_cut.bidirectional": 100663296,
          "server1.nic7.rx": 6291456,
          "rank15.rx": 6291456,
          "rank15.tx": 6291456,
          "server1.nic7.tx": 6291456,
          "cut.1->0": 50331648,
          "server0.nic7.rx": 6291456,
          "rank7.rx": 6291456,
          "rank0.tx": 6291456,
          "server0.nic0.tx": 6291456,
          "server1.nic0.rx": 6291456,
          "rank8.rx": 6291456,
          "rank8.tx": 6291456,
          "server1.nic0.tx": 6291456,
          "server0.nic0.rx": 6291456,
          "rank0.rx": 6291456,
          "rank1.tx": 6291456,
          "server0.nic1.tx": 6291456,
          "server1.nic1.rx": 6291456,
          "rank9.rx": 6291456,
          "rank9.tx": 6291456,
          "server1.nic1.tx": 6291456,
          "server0.nic1.rx": 6291456,
          "rank1.rx": 6291456,
          "rank2.tx": 6291456,
          "server0.nic2.tx": 6291456,
          "server1.nic2.rx": 6291456,
          "rank10.rx": 6291456,
          "rank10.tx": 6291456,
          "server1.nic2.tx": 6291456,
          "server0.nic2.rx": 6291456,
          "rank2.rx": 6291456,
          "rank3.tx": 6291456,
          "server0.nic3.tx": 6291456,
          "server1.nic3.rx": 6291456,
          "rank11.rx": 6291456,
          "rank11.tx": 6291456,
          "server1.nic3.tx": 6291456,
          "server0.nic3.rx": 6291456,
          "rank3.rx": 6291456,
          "rank4.tx": 6291456,
          "server0.nic4.tx": 6291456,
          "server1.nic4.rx": 6291456,
          "rank12.rx": 6291456,
          "rank12.tx": 6291456,
          "server1.nic4.tx": 6291456,
          "server0.nic4.rx": 6291456,
          "rank4.rx": 6291456,
          "rank5.tx": 6291456,
          "server0.nic5.tx": 6291456,
          "server1.nic5.rx": 6291456,
          "rank13.rx": 6291456,
          "rank13.tx": 6291456,
          "server1.nic5.tx": 6291456,
          "server0.nic5.rx": 6291456,
          "rank5.rx": 6291456,
          "rank6.tx": 6291456,
          "server0.nic6.tx": 6291456,
          "server1.nic6.rx": 6291456,
          "rank14.rx": 6291456,
          "rank14.tx": 6291456,
          "server1.nic6.tx": 6291456,
          "server0.nic6.rx": 6291456,
          "rank6.rx": 6291456
        },
        "resource_lower_seconds": 0.00012582912,
        "barrier_lower_with_startup_seconds": 0.00012666212
      },
      {
        "round": 8,
        "phase": "all_gather",
        "resource_bytes": {
          "rank7.tx": 6291456,
          "server0.nic7.tx": 6291456,
          "cut.0->1": 50331648,
          "shared_cut.bidirectional": 100663296,
          "server1.nic7.rx": 6291456,
          "rank15.rx": 6291456,
          "rank15.tx": 6291456,
          "server1.nic7.tx": 6291456,
          "cut.1->0": 50331648,
          "server0.nic7.rx": 6291456,
          "rank7.rx": 6291456,
          "rank0.tx": 6291456,
          "server0.nic0.tx": 6291456,
          "server1.nic0.rx": 6291456,
          "rank8.rx": 6291456,
          "rank8.tx": 6291456,
          "server1.nic0.tx": 6291456,
          "server0.nic0.rx": 6291456,
          "rank0.rx": 6291456,
          "rank1.tx": 6291456,
          "server0.nic1.tx": 6291456,
          "server1.nic1.rx": 6291456,
          "rank9.rx": 6291456,
          "rank9.tx": 6291456,
          "server1.nic1.tx": 6291456,
          "server0.nic1.rx": 6291456,
          "rank1.rx": 6291456,
          "rank2.tx": 6291456,
          "server0.nic2.tx": 6291456,
          "server1.nic2.rx": 6291456,
          "rank10.rx": 6291456,
          "rank10.tx": 6291456,
          "server1.nic2.tx": 6291456,
          "server0.nic2.rx": 6291456,
          "rank2.rx": 6291456,
          "rank3.tx": 6291456,
          "server0.nic3.tx": 6291456,
          "server1.nic3.rx": 6291456,
          "rank11.rx": 6291456,
          "rank11.tx": 6291456,
          "server1.nic3.tx": 6291456,
          "server0.nic3.rx": 6291456,
          "rank3.rx": 6291456,
          "rank4.tx": 6291456,
          "server0.nic4.tx": 6291456,
          "server1.nic4.rx": 6291456,
          "rank12.rx": 6291456,
          "rank12.tx": 6291456,
          "server1.nic4.tx": 6291456,
          "server0.nic4.rx": 6291456,
          "rank4.rx": 6291456,
          "rank5.tx": 6291456,
          "server0.nic5.tx": 6291456,
          "server1.nic5.rx": 6291456,
          "rank13.rx": 6291456,
          "rank13.tx": 6291456,
          "server1.nic5.tx": 6291456,
          "server0.nic5.rx": 6291456,
          "rank5.rx": 6291456,
          "rank6.tx": 6291456,
          "server0.nic6.tx": 6291456,
          "server1.nic6.rx": 6291456,
          "rank14.rx": 6291456,
          "rank14.tx": 6291456,
          "server1.nic6.tx": 6291456,
          "server0.nic6.rx": 6291456,
          "rank6.rx": 6291456
        },
        "resource_lower_seconds": 0.00012582912,
        "barrier_lower_with_startup_seconds": 0.00012666212
      },
      {
        "round": 9,
        "phase": "all_gather",
        "resource_bytes": {
          "rank0.tx": 12582912,
          "local.0->1": 12582912,
          "rank1.rx": 12582912,
          "rank1.tx": 12582912,
          "local.1->2": 12582912,
          "rank2.rx": 12582912,
          "rank2.tx": 12582912,
          "local.2->3": 12582912,
          "rank3.rx": 12582912,
          "rank3.tx": 12582912,
          "local.3->4": 12582912,
          "rank4.rx": 12582912,
          "rank4.tx": 12582912,
          "local.4->5": 12582912,
          "rank5.rx": 12582912,
          "rank5.tx": 12582912,
          "local.5->6": 12582912,
          "rank6.rx": 12582912,
          "rank6.tx": 12582912,
          "local.6->7": 12582912,
          "rank7.rx": 12582912,
          "rank7.tx": 12582912,
          "local.7->0": 12582912,
          "rank0.rx": 12582912,
          "rank8.tx": 12582912,
          "local.8->9": 12582912,
          "rank9.rx": 12582912,
          "rank9.tx": 12582912,
          "local.9->10": 12582912,
          "rank10.rx": 12582912,
          "rank10.tx": 12582912,
          "local.10->11": 12582912,
          "rank11.rx": 12582912,
          "rank11.tx": 12582912,
          "local.11->12": 12582912,
          "rank12.rx": 12582912,
          "rank12.tx": 12582912,
          "local.12->13": 12582912,
          "rank13.rx": 12582912,
          "rank13.tx": 12582912,
          "local.13->14": 12582912,
          "rank14.rx": 12582912,
          "rank14.tx": 12582912,
          "local.14->15": 12582912,
          "rank15.rx": 12582912,
          "rank15.tx": 12582912,
          "local.15->8": 12582912,
          "rank8.rx": 12582912
        },
        "resource_lower_seconds": 2.7962026666666665e-05,
        "barrier_lower_with_startup_seconds": 2.8795026666666665e-05
      },
      {
        "round": 10,
        "phase": "all_gather",
        "resource_bytes": {
          "rank0.tx": 12582912,
          "local.0->1": 12582912,
          "rank1.rx": 12582912,
          "rank1.tx": 12582912,
          "local.1->2": 12582912,
          "rank2.rx": 12582912,
          "rank2.tx": 12582912,
          "local.2->3": 12582912,
          "rank3.rx": 12582912,
          "rank3.tx": 12582912,
          "local.3->4": 12582912,
          "rank4.rx": 12582912,
          "rank4.tx": 12582912,
          "local.4->5": 12582912,
          "rank5.rx": 12582912,
          "rank5.tx": 12582912,
          "local.5->6": 12582912,
          "rank6.rx": 12582912,
          "rank6.tx": 12582912,
          "local.6->7": 12582912,
          "rank7.rx": 12582912,
          "rank7.tx": 12582912,
          "local.7->0": 12582912,
          "rank0.rx": 12582912,
          "rank8.tx": 12582912,
          "local.8->9": 12582912,
          "rank9.rx": 12582912,
          "rank9.tx": 12582912,
          "local.9->10": 12582912,
          "rank10.rx": 12582912,
          "rank10.tx": 12582912,
          "local.10->11": 12582912,
          "rank11.rx": 12582912,
          "rank11.tx": 12582912,
          "local.11->12": 12582912,
          "rank12.rx": 12582912,
          "rank12.tx": 12582912,
          "local.12->13": 12582912,
          "rank13.rx": 12582912,
          "rank13.tx": 12582912,
          "local.13->14": 12582912,
          "rank14.rx": 12582912,
          "rank14.tx": 12582912,
          "local.14->15": 12582912,
          "rank15.rx": 12582912,
          "rank15.tx": 12582912,
          "local.15->8": 12582912,
          "rank8.rx": 12582912
        },
        "resource_lower_seconds": 2.7962026666666665e-05,
        "barrier_lower_with_startup_seconds": 2.8795026666666665e-05
      },
      {
        "round": 11,
        "phase": "all_gather",
        "resource_bytes": {
          "rank0.tx": 12582912,
          "local.0->1": 12582912,
          "rank1.rx": 12582912,
          "rank1.tx": 12582912,
          "local.1->2": 12582912,
          "rank2.rx": 12582912,
          "rank2.tx": 12582912,
          "local.2->3": 12582912,
          "rank3.rx": 12582912,
          "rank3.tx": 12582912,
          "local.3->4": 12582912,
          "rank4.rx": 12582912,
          "rank4.tx": 12582912,
          "local.4->5": 12582912,
          "rank5.rx": 12582912,
          "rank5.tx": 12582912,
          "local.5->6": 12582912,
          "rank6.rx": 12582912,
          "rank6.tx": 12582912,
          "local.6->7": 12582912,
          "rank7.rx": 12582912,
          "rank7.tx": 12582912,
          "local.7->0": 12582912,
          "rank0.rx": 12582912,
          "rank8.tx": 12582912,
          "local.8->9": 12582912,
          "rank9.rx": 12582912,
          "rank9.tx": 12582912,
          "local.9->10": 12582912,
          "rank10.rx": 12582912,
          "rank10.tx": 12582912,
          "local.10->11": 12582912,
          "rank11.rx": 12582912,
          "rank11.tx": 12582912,
          "local.11->12": 12582912,
          "rank12.rx": 12582912,
          "rank12.tx": 12582912,
          "local.12->13": 12582912,
          "rank13.rx": 12582912,
          "rank13.tx": 12582912,
          "local.13->14": 12582912,
          "rank14.rx": 12582912,
          "rank14.tx": 12582912,
          "local.14->15": 12582912,
          "rank15.rx": 12582912,
          "rank15.tx": 12582912,
          "local.15->8": 12582912,
          "rank8.rx": 12582912
        },
        "resource_lower_seconds": 2.7962026666666665e-05,
        "barrier_lower_with_startup_seconds": 2.8795026666666665e-05
      },
      {
        "round": 12,
        "phase": "all_gather",
        "resource_bytes": {
          "rank0.tx": 12582912,
          "local.0->1": 12582912,
          "rank1.rx": 12582912,
          "rank1.tx": 12582912,
          "local.1->2": 12582912,
          "rank2.rx": 12582912,
          "rank2.tx": 12582912,
          "local.2->3": 12582912,
          "rank3.rx": 12582912,
          "rank3.tx": 12582912,
          "local.3->4": 12582912,
          "rank4.rx": 12582912,
          "rank4.tx": 12582912,
          "local.4->5": 12582912,
          "rank5.rx": 12582912,
          "rank5.tx": 12582912,
          "local.5->6": 12582912,
          "rank6.rx": 12582912,
          "rank6.tx": 12582912,
          "local.6->7": 12582912,
          "rank7.rx": 12582912,
          "rank7.tx": 12582912,
          "local.7->0": 12582912,
          "rank0.rx": 12582912,
          "rank8.tx": 12582912,
          "local.8->9": 12582912,
          "rank9.rx": 12582912,
          "rank9.tx": 12582912,
          "local.9->10": 12582912,
          "rank10.rx": 12582912,
          "rank10.tx": 12582912,
          "local.10->11": 12582912,
          "rank11.rx": 12582912,
          "rank11.tx": 12582912,
          "local.11->12": 12582912,
          "rank12.rx": 12582912,
          "rank12.tx": 12582912,
          "local.12->13": 12582912,
          "rank13.rx": 12582912,
          "rank13.tx": 12582912,
          "local.13->14": 12582912,
          "rank14.rx": 12582912,
          "rank14.tx": 12582912,
          "local.14->15": 12582912,
          "rank15.rx": 12582912,
          "rank15.tx": 12582912,
          "local.15->8": 12582912,
          "rank8.rx": 12582912
        },
        "resource_lower_seconds": 2.7962026666666665e-05,
        "barrier_lower_with_startup_seconds": 2.8795026666666665e-05
      },
      {
        "round": 13,
        "phase": "all_gather",
        "resource_bytes": {
          "rank0.tx": 12582912,
          "local.0->1": 12582912,
          "rank1.rx": 12582912,
          "rank1.tx": 12582912,
          "local.1->2": 12582912,
          "rank2.rx": 12582912,
          "rank2.tx": 12582912,
          "local.2->3": 12582912,
          "rank3.rx": 12582912,
          "rank3.tx": 12582912,
          "local.3->4": 12582912,
          "rank4.rx": 12582912,
          "rank4.tx": 12582912,
          "local.4->5": 12582912,
          "rank5.rx": 12582912,
          "rank5.tx": 12582912,
          "local.5->6": 12582912,
          "rank6.rx": 12582912,
          "rank6.tx": 12582912,
          "local.6->7": 12582912,
          "rank7.rx": 12582912,
          "rank7.tx": 12582912,
          "local.7->0": 12582912,
          "rank0.rx": 12582912,
          "rank8.tx": 12582912,
          "local.8->9": 12582912,
          "rank9.rx": 12582912,
          "rank9.tx": 12582912,
          "local.9->10": 12582912,
          "rank10.rx": 12582912,
          "rank10.tx": 12582912,
          "local.10->11": 12582912,
          "rank11.rx": 12582912,
          "rank11.tx": 12582912,
          "local.11->12": 12582912,
          "rank12.rx": 12582912,
          "rank12.tx": 12582912,
          "local.12->13": 12582912,
          "rank13.rx": 12582912,
          "rank13.tx": 12582912,
          "local.13->14": 12582912,
          "rank14.rx": 12582912,
          "rank14.tx": 12582912,
          "local.14->15": 12582912,
          "rank15.rx": 12582912,
          "rank15.tx": 12582912,
          "local.15->8": 12582912,
          "rank8.rx": 12582912
        },
        "resource_lower_seconds": 2.7962026666666665e-05,
        "barrier_lower_with_startup_seconds": 2.8795026666666665e-05
      },
      {
        "round": 14,
        "phase": "all_gather",
        "resource_bytes": {
          "rank0.tx": 12582912,
          "local.0->1": 12582912,
          "rank1.rx": 12582912,
          "rank1.tx": 12582912,
          "local.1->2": 12582912,
          "rank2.rx": 12582912,
          "rank2.tx": 12582912,
          "local.2->3": 12582912,
          "rank3.rx": 12582912,
          "rank3.tx": 12582912,
          "local.3->4": 12582912,
          "rank4.rx": 12582912,
          "rank4.tx": 12582912,
          "local.4->5": 12582912,
          "rank5.rx": 12582912,
          "rank5.tx": 12582912,
          "local.5->6": 12582912,
          "rank6.rx": 12582912,
          "rank6.tx": 12582912,
          "local.6->7": 12582912,
          "rank7.rx": 12582912,
          "rank7.tx": 12582912,
          "local.7->0": 12582912,
          "rank0.rx": 12582912,
          "rank8.tx": 12582912,
          "local.8->9": 12582912,
          "rank9.rx": 12582912,
          "rank9.tx": 12582912,
          "local.9->10": 12582912,
          "rank10.rx": 12582912,
          "rank10.tx": 12582912,
          "local.10->11": 12582912,
          "rank11.rx": 12582912,
          "rank11.tx": 12582912,
          "local.11->12": 12582912,
          "rank12.rx": 12582912,
          "rank12.tx": 12582912,
          "local.12->13": 12582912,
          "rank13.rx": 12582912,
          "rank13.tx": 12582912,
          "local.13->14": 12582912,
          "rank14.rx": 12582912,
          "rank14.tx": 12582912,
          "local.14->15": 12582912,
          "rank15.rx": 12582912,
          "rank15.tx": 12582912,
          "local.15->8": 12582912,
          "rank8.rx": 12582912
        },
        "resource_lower_seconds": 2.7962026666666665e-05,
        "barrier_lower_with_startup_seconds": 2.8795026666666665e-05
      },
      {
        "round": 15,
        "phase": "all_gather",
        "resource_bytes": {
          "rank0.tx": 12582912,
          "local.0->1": 12582912,
          "rank1.rx": 12582912,
          "rank1.tx": 12582912,
          "local.1->2": 12582912,
          "rank2.rx": 12582912,
          "rank2.tx": 12582912,
          "local.2->3": 12582912,
          "rank3.rx": 12582912,
          "rank3.tx": 12582912,
          "local.3->4": 12582912,
          "rank4.rx": 12582912,
          "rank4.tx": 12582912,
          "local.4->5": 12582912,
          "rank5.rx": 12582912,
          "rank5.tx": 12582912,
          "local.5->6": 12582912,
          "rank6.rx": 12582912,
          "rank6.tx": 12582912,
          "local.6->7": 12582912,
          "rank7.rx": 12582912,
          "rank7.tx": 12582912,
          "local.7->0": 12582912,
          "rank0.rx": 12582912,
          "rank8.tx": 12582912,
          "local.8->9": 12582912,
          "rank9.rx": 12582912,
          "rank9.tx": 12582912,
          "local.9->10": 12582912,
          "rank10.rx": 12582912,
          "rank10.tx": 12582912,
          "local.10->11": 12582912,
          "rank11.rx": 12582912,
          "rank11.tx": 12582912,
          "local.11->12": 12582912,
          "rank12.rx": 12582912,
          "rank12.tx": 12582912,
          "local.12->13": 12582912,
          "rank13.rx": 12582912,
          "rank13.tx": 12582912,
          "local.13->14": 12582912,
          "rank14.rx": 12582912,
          "rank14.tx": 12582912,
          "local.14->15": 12582912,
          "rank15.rx": 12582912,
          "rank15.tx": 12582912,
          "local.15->8": 12582912,
          "rank8.rx": 12582912
        },
        "resource_lower_seconds": 2.7962026666666665e-05,
        "barrier_lower_with_startup_seconds": 2.8795026666666665e-05
      }
    ],
    "aggregate_resource_lower_seconds": 0.0004194304,
    "sum_round_resource_lower_seconds": 0.0006431266133333333,
    "barrier_lower_with_startup_seconds": 0.0006564546133333333
  },
  "summary": {
    "network_send_bytes": 3019898880,
    "local_send_bytes": 2818572288,
    "remote_send_bytes": 201326592,
    "remote_send_bytes_per_direction": 100663296,
    "reduction_scalar_adds": 754974720,
    "final_gradient_bytes_per_rank": [
      100663296,
      100663296,
      100663296,
      100663296,
      100663296,
      100663296,
      100663296,
      100663296,
      100663296,
      100663296,
      100663296,
      100663296,
      100663296,
      100663296,
      100663296,
      100663296
    ],
    "rounds": 16,
    "first_round_remote_edges": 0,
    "remote_nics_used_per_server": 8,
    "aggregate_resource_lower_seconds_exact": "4096/9765625",
    "largest_aggregate_resources": [
      "rank0.rx",
      "rank0.tx",
      "rank1.rx",
      "rank1.tx",
      "rank10.rx",
      "rank10.tx",
      "rank11.rx",
      "rank11.tx",
      "rank12.rx",
      "rank12.tx",
      "rank13.rx",
      "rank13.tx",
      "rank14.rx",
      "rank14.tx",
      "rank15.rx",
      "rank15.tx",
      "rank2.rx",
      "rank2.tx",
      "rank3.rx",
      "rank3.tx",
      "rank4.rx",
      "rank4.tx",
      "rank5.rx",
      "rank5.tx",
      "rank6.rx",
      "rank6.tx",
      "rank7.rx",
      "rank7.tx",
      "rank8.rx",
      "rank8.tx",
      "rank9.rx",
      "rank9.tx"
    ],
    "serial_barrier_lower_seconds_exact": "3077131/4687500000",
    "necessary_budget_not_excluded": true,
    "actual_training_deadline_feasible": null,
    "measured_seconds": null
  },
  "assumptions": [
    "One real first-layer gate parameter gradient per rank; each rank contributes different sample data to the same coordinates. Not activations, whole-model gradients, or framework buckets.",
    "FP32/BF16 are declared gradient wire/operand widths. Rank contribution identities prove algebraic sum coverage, not floating-point reassociation equivalence or backend accumulation precision.",
    "Two servers each own 8 fixed ranks. Hierarchy executes local RS over 8 ranks, corresponding-owner two-rank AR, local AG with stage/round barriers; no overlapping stages or unmodeled algorithm substitutions.",
    "Every rank owns one NIC: a remote message leaves through the sender NIC and enters through the receiver NIC, never striped or relayed. The switch cut between the servers carries the aggregate NIC rate; no shared server egress is declared.",
    "All rates and startup are declared inputs. Each round bound is max(resource bytes/rate)+startup; serialized barrier bounds omit reduction work, propagation, buffering, topology latency and interference. They are not executable timing or deadline guarantees.",
    "Logical network sends count payload once. Endpoint receive, NIC, ingress and cut counters represent distinct resource demands; their sum is not additional gradient payload or HBM traffic.",
    "No padding is introduced. Missing paths/resources or invalid rates reject. Budget pass only means this communication lower bound has not excluded the candidate; real training feasibility remains unknown."
  ]
}
```
