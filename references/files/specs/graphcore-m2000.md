<!-- 从 graphcore-m2000.html 迁移的资料快照；原始 HTML SHA-256: 6e761899d76b52433f4501f3be4bef26eccfd221190e8615caa0296ad3708f52。 -->

# 2. Product description[](#product-description "Permalink to this headline")

## 2.1. IPU-M2000 in IPU-POD systems[](#ipu-m2000-in-ipu-pod-systems "Permalink to this headline")

Graphcore’s IPU-M2000 IPU-Machine is designed to support scale-up and scale-out machine intelligence compute. The IPU-POD reference designs, based on the IPU-M2000, deliver scalable building blocks for IPU-POD systems.

Virtualization and provisioning software allow the AI compute resources to be elastically allocated to users and be grouped for both model-parallel and data-parallel AI compute in all IPU-POD systems, supporting multiple users and mixed workloads as well as single systems for large models.

IPU-POD system level products, including IPU-M2000 machines, host servers and network switches, are available from Graphcore channel partners globally. Customers can select their preferred server brand from a range of leading server vendors. There are multiple host servers from different vendors approved for use in IPU-POD systems, see the [approved server list](https://docs.graphcore.ai/projects/graphcore-approved-server-list/en/latest/index.html) for details. The disaggregated host architecture allows for different server requirements based on workload.

The “Founder’s Edition” IPU-M2000 comes complete with all the cables required for installation in IPU-POD systems.

## 2.2. IPU‑POD₄ Direct Attach[](#pod4-direct-attach "Permalink to this headline")

The single IPU-M2000 blade in an IPU‑POD₄ Direct Attach system is pre-configured with Virtual-IPU (V-IPU) management software ensuring easy installation and integration with pre-existing infrastructure. The host server required to run the Poplar SDK is not included. In this datasheet we use the Dell R6525 server with dual-socket AMD Epyc2 CPUs as the default offering. Default number of servers is 1, however up to 4 host servers can be required depending on workload - please speak to Graphcore sales.

[![](_images/POD4.png)](_images/POD4.png)

## 2.3. Software[](#software "Permalink to this headline")

IPU-POD systems are fully supported by Graphcore’s Poplar® software development environment, providing a complete and mature platform for ML development and deployment. Standard ML frameworks including TensorFlow, Keras, ONNX, Halo, PaddlePaddle, HuggingFace, PyTorch and PyTorch Lightning are fully supported along with access to PopLibs through our Poplar C++ API. Note that PopLibs, PopART and TensorFlow are available as open source in the Graphcore GitHub repo [https://github.com/graphcore](https://github.com/graphcore). PopTorch provides a simple wrapper around PyTorch programs to enable the programs to run seamlessly on IPUs. The Poplar SDK also includes the PopVision™ visualisation and analysis tools which provide performance monitoring for IPUs - the graphical analysis enables detailed inspection of all processing activities.

In addition to these Poplar development tools, IPU-POD systems are enabled with software support for industry standard converged infrastructure management tools including OpenBMC, Redfish, Docker containers, and orchestration with Slurm and Kubernetes.

[![](_images/software.png)](_images/software.png)

Fig. 2.1 IPU-POD software[](#id1 "Permalink to this image")

[TABLE]

Table 2.1 Poplar SDK[](#id2 "Permalink to this table") {#id2}

To see a full list of supported OS, VM and container options go to the Graphcore support portal [https://www.graphcore.ai/support](https://www.graphcore.ai/support)

| IPU-Fabric topology discovery and validation |  |
|----|----|
| Provisioning | gRPC and SSH/CLI for IPU allocation/de-allocation into isolated domains (vPods) |
|  | Plug-ins for SLURM and Kubernetes (K8) |
| Resource monitoring | gRPC and SSH/CLI for accessing the IPU-M2000 monitoring service |
|  | Prometheus node exporter and Grafana (visualization) support |

Table 2.2 Graphcore Virtual IPU SW[](#id3 "Permalink to this table") {#id3}

|                                                 |
|-------------------------------------------------|
| Baseboard Management Controller (OpenBMC)       |
| Dual-image firmware with local rollback support |
| Console support, CLI/SSH based                  |
| Serial-over-Lan and Redfish REST API            |

Table 2.3 Lights-out management[](#id4 "Permalink to this table") {#id4}

## 2.4. Technical specifications[](#technical-specifications "Permalink to this headline")

|  |  |
|----|----|
| IPU processors | 4 GC200 IPU processors |
|  | 5,888 IPU-Cores™ with independent code execution on 35,328 worker threads |
| AI compute | 0.999 petaFLOPS AI (FP16.16) compute |
|  | 0.2497 petaFLOPS FP32 compute |
| Memory | Up to ~260GB memory (3.6GB In-Processor Memory™ plus up to 256GB Streaming Memory™) |
|  | 180TB/s memory bandwidth |
| Streaming Memory | 2 DDR4-2400 DIMM DRAM |
|  | Options: 2x 64GB (default SKU in IPU-M2000 Founder’s Edition) or 2x 128GB (contact sales) |
| IPU-Gateway | 1x IPU-Gateway chip with integrated Arm Cortex quad-core A-series SoC |
| Internal SSD | 32GB eMMC |
|  | 1TB M.2 SSD |
| NIC | RoCEv2 NIC (1 PCIe G4 x16 FH¾L slot) |
|  | Standard QSFP ports |
| Mechanical | 1U 19inch chassis (Open Compute compliant) |
|  | 440mm (width) x 728mm (depth) x 1U (height) |
|  | Weight: 16.395kg (36.14lbs) |
| Lights-out management | OpenBMC AST2520 |
|  | 2x1GbE RJ45 management ports |

Table 2.4 IPU-M2000 IPU-Machine[](#id5 "Permalink to this table") {#id5}

|  |  |
|----|----|
| IPU-Links | 8x IPU-Links supporting 2Tbps bi-directional bandwidth |
|  | 8x OSFP ports |
|  | Switch-less scalability |
|  | Up to 8 IPU-M2000s in directly connected stacked systems |
|  | Up to 16 IPU-M2000s in IPU-POD systems |
| GW-Links | 2x GW-Links (IPU-Link extension over 100GbE) |
|  | 2 QSFP28 ports |
|  | Switch or switch-less scalability supporting 400Gbp bi-directional bandwidth |
|  | Up to 1024 IPU-M2000s connected |

Table 2.5 IPU-M2000 IPU-Fabric[](#id6 "Permalink to this table") {#id6}

[TABLE]

Table 2.6 IPU-M2000 thermal characteristics[](#id7 "Permalink to this table") {#id7}

|  |  |
|----|----|
| PSU | 2x 1500 W hot-plug PSUs (standard SSI slim type 54mm) |
| Input power (V_(ac)) | 100 - 240 V_(ac) (115 - 230 V_(ac) nominal) |
| Power cap | 1500 W with programmable power cap |
| Redundancy | 1+1 redundancy |

Table 2.7 IPU-M2000 power[](#id8 "Permalink to this table") {#id8}

## 2.5. Environmental characteristics[](#environmental-characteristics "Permalink to this headline")

|  |  |
|----|----|
| Operating temperature and humidity (inlet air) | 10-32C (50 to 90F) at 20%-80% RH (\*) |
| Operating altitude | 0 to 3,048m (0-10,000ft) (\*\*) |

Table 2.8 IPU-M2000 environmental characteristics[](#id9 "Permalink to this table") {#id9}

- (\*) Altitude less than 900m/3000ft and non-condensing environment

- (\*\*) Max. ambient temperature is de-rated by 1°C per 300m above 900m

For power caps higher than 1700W per IPU-M2000 please contact Graphcore sales for environmental guidance.

## 2.6. Standards compliance[](#standards-compliance "Permalink to this headline")

|  |  |
|----|----|
| EMC standards | Emissions: FCC CFR 47, ICES-003, EN55032, EN61000-3-2, EN61000-3-3, VCCI 32-1 |
|  | Immunity: EN55035, EN61000-4-2, EN61000-4-3, EN61000-4-4, EN61000-4-5, EN61000-4-6, EN61000-4-8, EN61000-4-11 |
| Safety standards | IEC62368-1 2nd Edition, IEC60950-1, UL62368-1 2nd Edition |
| Certifications | North America (FCC, UL), Europe (CE), UK (UKCA), Australia (RCM), Taiwan (BSMI), Japan (VCCI) |
|  | South Korea (KC), China (CQC) |
|  | CB-62368, CB-60950 |
| Environmental standards | EU 2011/65/EU RoHS Directive, XVII REACH 1907/2006, 2012/19/EU WEEE Directive |

Table 2.9 IPU-M2000 standards compliance[](#id10 "Permalink to this table") {#id10}

The European Directive 2012/19/EU on Waste Electrical and Electronic Equipment (WEEE) states that these appliances should not be disposed of as part of the routine solid urban waste cycle, but collected separately in order to optimise the recovery and recycling flow of the materials they contain, while also preventing potential damage to human health and the environment arising from the presence of potentially hazardous substances.

The crossed-out bin symbol is printed on all products as a reminder, and must not be disposed of with your other household waste.

Owners of electrical and electronic equipment (EEE) should contact their local government agencies to identify local WEEE collection and treatment systems for the environmental recycling and /or disposal of their end of life computer products. For more information on proper disposal of these devices, refer to the public utility service.

[![](_images/WEEE-bin-plus-triman-logo.png)](_images/WEEE-bin-plus-triman-logo.png)

## 2.7. Ordering information[](#ordering-information "Permalink to this headline")

| Part number | Description                 |
|-------------|-----------------------------|
| GC-ADA2-00  | IPU-M2000                   |
| GC-ADA2-FE  | IPU-M2000 Founder’s Edition |

Table 2.10 IPU-M2000 ordering information[](#id11 "Permalink to this table") {#id11}

IPU-POD systems are available to order from Graphcore channel partners – see [https://www.graphcore.ai/partners](https://www.graphcore.ai/partners) for details of your nearest Graphcore partner.
