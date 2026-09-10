<!-- 从 graphcore-bow2000.html 迁移的资料快照；原始 HTML SHA-256: 1c5684177e94b9a570a251ad1b30201ffa97e08000b46aacc63b63231e646a1f。 -->

# 2. Product description[](#product-description "Permalink to this headline")

## 2.1. Bow-2000 in Bow Pod systems[](#bow-2000-in-bow-pod-systems "Permalink to this headline")

Graphcore’s Bow-2000 IPU-Machine is designed to support scale-up and scale-out machine intelligence compute. The Bow Pod reference designs, based on the Bow-2000, deliver scalable building blocks for the Bow Pod systems range of products: Bow Pod₁₆ (4 Bow-2000 machines directly attach to a single host server), Bow Pod₆₄ (16 Bow-2000 machines in a switched system with 1-4 host servers), and Bow Pod₂₅₆ (64 Bow-2000 machines in a switched system with 4-16 host servers). Bow Pod₁₀₂₄ is currently available for early access.

Virtualization and provisioning software allow the AI compute resources to be elastically allocated to users and be grouped for both model-parallel and data-parallel AI compute in all Bow Pod systems, supporting multiple users and mixed workloads as well as single systems for large models.

Bow Pod system level products, including Bow-2000 machines, host servers and network switches, are available from Graphcore channel partners globally. Customers can select their preferred server brand from a range of leading server vendors. There are multiple host servers from different vendors approved for use in Bow Pod systems, see the [approved server list](https://docs.graphcore.ai/projects/graphcore-approved-server-list/en/latest/index.html) for details. The disaggregated host architecture allows for different server requirements based on workload.

The Bow-2000 is backwards compatible with the IPU-M2000™ IPU-Machine and has up to 40% performance improvement and up to 16% more power efficiency for real world AI workloads compared to the IPU-M2000 with no code changes.

The “Founder’s Edition” Bow-2000 comes complete with all the cables required for installation in Bow Pod systems.

## 2.2. Software[](#software "Permalink to this headline")

Bow Pod systems are fully supported by Graphcore’s Poplar® software development environment, providing a complete and mature platform for ML development and deployment. Standard ML frameworks including TensorFlow, Keras, ONNX, Halo, PaddlePaddle, HuggingFace, PyTorch and PyTorch Lightning are fully supported along with access to PopLibs through our Poplar C++ API. Note that PopLibs, PopART and TensorFlow are available as open source in the Graphcore GitHub repo [https://github.com/graphcore](https://github.com/graphcore). PopTorch provides a simple wrapper around PyTorch programs to enable the programs to run seamlessly on IPUs. The Poplar SDK also includes the PopVision™ visualisation and analysis tools which provide performance monitoring for IPUs - the graphical analysis enables detailed inspection of all processing activities.

In addition to these Poplar development tools, Bow Pod systems are enabled with software support for industry standard converged infrastructure management tools including OpenBMC, Redfish, Docker containers, and orchestration with Slurm and Kubernetes.

[![](_images/software.png)](_images/software.png)

Fig. 2.1 Bow Pod software[](#id1 "Permalink to this image")

[TABLE]

Table 2.1 Poplar SDK[](#id2 "Permalink to this table") {#id2}

To see a full list of supported OS, VM and container options go to the Graphcore support portal [https://www.graphcore.ai/support](https://www.graphcore.ai/support)

[TABLE]

Table 2.2 Graphcore Virtual IPU SW[](#id3 "Permalink to this table") {#id3}

|                                                 |
|-------------------------------------------------|
| Baseboard Management Controller (OpenBMC)       |
| Dual-image firmware with local rollback support |
| Console support, CLI/SSH based                  |
| Serial-over-Lan and Redfish REST API            |

Table 2.3 Lights-out management[](#id4 "Permalink to this table") {#id4}

## 2.3. Technical specifications[](#technical-specifications "Permalink to this headline")

|  |  |
|----|----|
| IPU processors | 4x Bow IPU processors (IPU frequency 1.85 GHz) |
|  | 5,888 IPU-Cores™ with independent code execution on 35,328 worker threads |
| AI compute | 1.394 petaFLOPS AI (FP16.16) compute |
|  | 0.349 petaFLOPS FP32 compute |
| Memory | Up to ~260 GB memory (3.6 GB In-Processor Memory™ plus up to 256 GB Streaming Memory™) |
|  | 261 TB/s memory bandwidth |
| Streaming Memory | 2x DDR4-2400 DIMM DRAM |
|  | Options: 2x 64 GB (default SKU in Bow-2000 Founder’s Edition) or 2x 128 GB (contact sales) |
| IPU-Gateway | 1x IPU-Gateway chip with integrated Arm Cortex quad-core A-series SoC |
| Internal SSD | 32 GB eMMC |
|  | 1 TB M.2 SSD |
| NIC | RoCEv2 NIC (1 PCIe G4 x16 FH¾L slot) |
|  | Standard QSFP ports |
| Mechanical | 1U 19 inch chassis (Open Compute compliant) |
|  | 440 mm (width) x 728 mm (depth) x 1U (height) |
|  | Weight: 16.395 kg (36.14 lbs) |
| Lights-out management | OpenBMC AST2520 |
|  | 2x 1 GbE RJ45 management ports |

Table 2.4 Bow-2000 IPU-Machine[](#id5 "Permalink to this table") {#id5}

|  |  |
|----|----|
| IPU-Links | 8x IPU-Links supporting 2 Tbps bi-directional bandwidth |
|  | 8x OSFP ports |
|  | Switch-less scalability |
|  | Up to 8 Bow-2000s in directly connected stacked systems |
|  | Up to 16 Bow-2000s in Bow Pod systems |
| GW-Links | 2x GW-Links (IPU-Link extension over 100 GbE) |
|  | 2 QSFP28 ports |
|  | Switch or switch-less scalability supporting 400 Gbp bi-directional bandwidth |
|  | Up to 1024 Bow-2000s connected |

Table 2.5 Bow-2000 IPU-Fabric[](#id6 "Permalink to this table") {#id6}

|  |  |
|----|----|
| Air cooled | Built-in N+1 hot-plug fan cooling system in each of the individual components (Bow-2000s, servers and switches) |
| Rack airflow | All Bow Pod₆₄ components (Bow-2000 IPU-Machines, server(s) and switches) are mounted for airflow direction front of rack (single door, cold aisle side) to back of rack (split door, hot aisle side) |
| Airflow rate | 103 CFM (measured) per Bow-2000 (1648 CFM total in Bow Pod₆₄) |

Table 2.6 Bow-2000 thermal characteristics[](#id7 "Permalink to this table") {#id7}

|  |  |
|----|----|
| PSU | 2x 1500 W hot-plug PSUs (standard SSI slim type 54mm) |
| Input power (V_(ac)) | 200 - 240 V |
| Input power (V_(dc)) | 240-310 V for GC-ADA2-30W and GC-ADA2-3EW models |
| Power cap | 1700 W with programmable power cap |
| Redundancy | 1+1 redundancy (with power cap set to 1500W) |

Table 2.7 Bow-2000 power[](#id8 "Permalink to this table") {#id8}

## 2.4. Environmental characteristics[](#environmental-characteristics "Permalink to this headline")

|  |  |
|----|----|
| Operating temperature and humidity (inlet air) | 10-32° C (50 to 90° F) at 20%-80% RH (\*) |
| Operating altitude | 0 to 3,048 m (0-10,000ft) (\*\*) |

Table 2.8 Environmental characteristics for the Bow Pod₆₄[](#id9 "Permalink to this table") {#id9}

- (\*) Altitude less than 900 m/3000 ft and non-condensing environment

- (\*\*) Max. ambient temperature is de-rated by 1° C per 300 m above 900 m

For power caps higher than 1700W per Bow-2000 please contact Graphcore sales for environmental guidance.

## 2.5. Standards compliance[](#standards-compliance "Permalink to this headline")

|  |  |
|----|----|
| EMC standards | Emissions: FCC CFR 47, ICES-003, EN55032, EN61000-3-2, EN61000-3-3, VCCI 32-1 |
|  | Immunity: EN55035, EN61000-4-2, EN61000-4-3, EN61000-4-4, EN61000-4-5, EN61000-4-6, EN61000-4-8, EN61000-4-11 |
| Safety standards | IEC62368-1 2nd Edition, IEC60950-1, UL62368-1 2nd Edition |
| Certifications | North America (FCC, UL), Europe (CE), UK (UKCA), Australia (RCM), Taiwan (BSMI), Japan (VCCI) |
|  | South Korea (KC), China (CQC) |
|  | CB-62368, CB-60950 |
| Environmental standards | EU 2011/65/EU RoHS Directive, XVII REACH 1907/2006, 2012/19/EU WEEE Directive |

Table 2.9 Bow-2000 standards compliance[](#id10 "Permalink to this table") {#id10}

The European Directive 2012/19/EU on Waste Electrical and Electronic Equipment (WEEE) states that these appliances should not be disposed of as part of the routine solid urban waste cycle, but collected separately in order to optimise the recovery and recycling flow of the materials they contain, while also preventing potential damage to human health and the environment arising from the presence of potentially hazardous substances.

The crossed-out bin symbol is printed on all products as a reminder, and must not be disposed of with your other household waste.

Owners of electrical and electronic equipment (EEE) should contact their local government agencies to identify local WEEE collection and treatment systems for the environmental recycling and /or disposal of their end of life computer products. For more information on proper disposal of these devices, refer to the public utility service.

[![](_images/WEEE-bin-plus-triman-logo.png)](_images/WEEE-bin-plus-triman-logo.png)

## 2.6. Ordering information[](#ordering-information "Permalink to this headline")

| Part number | Description                                          |
|-------------|------------------------------------------------------|
| GC-ADA2-00W | Bow-2000                                             |
| GC-ADA2-FEW | Bow-2000 Founder’s Edition                           |
| GC-ADA2-30W | Bow-2000 AC/DC capable power input                   |
| GC-ADA2-3EW | Bow-2000 AC/DC capable power input Founder’s Edition |

Table 2.10 Bow-2000 ordering information[](#id11 "Permalink to this table") {#id11}

Bow Pod systems are available to order from Graphcore channel partners – see [https://www.graphcore.ai/partners](https://www.graphcore.ai/partners) for details of your nearest Graphcore partner.
