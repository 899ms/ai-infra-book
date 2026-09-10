<!-- 从 b300-system-guide.html 迁移的资料快照；原始 HTML SHA-256: 22cd9101f2efab4e20fea85b49efb7111bb31a2e7197a051c827bdace645ebce。 -->

- [NVIDIA Docs Hub](https://docs.nvidia.com)
- [NVIDIA DGX Platform](https://docs.nvidia.com/dgx)
- [NVIDIA DGX Systems](https://docs.nvidia.com/dgx-systems)
- Introduction to NVIDIA DGX B300 Systems

[Is this page helpful?](https://surveys.hotjar.com/4904bf71-6484-47a7-83ff-4715cceabdb5)

<a id="introduction-to-nvidia-dgx-b300-systems"></a>

# Introduction to NVIDIA DGX B300 Systems
The NVIDIA DGX™ B300 system is a universal system purpose-built for all AI infrastructure and workloads from analytics to training to inference. The system is built on eight NVIDIA B300 Tensor Core GPUs.

![](_images/dgx-b300-with-bezel.png)

<a id="hardware-overview"></a>

## Hardware Overview
<a id="dgx-b300-physical-and-operational-specifications"></a>

### DGX B300 Physical and Operational Specifications
This section provides the physical specifications to install, power, and operate the system in a data center.

![](_images/dgx-b300-physical-specs.png)

[TABLE]

Physical and Operational Specifications[\#](#id2 "Link to this table") {#id2}

<a id="dgx-b300-feature-summary"></a>

### DGX B300 Feature Summary
The NVIDIA DGX B300 system includes the following features.

[TABLE]

Feature Summary[\#](#id3 "Link to this table") {#id3}

<a id="key-enhancements-over-previous-dgx-systems"></a>

### Key Enhancements Over Previous DGX Systems
The NVIDIA DGX B300 system introduces several key enhancements over previous DGX systems, including:

- Available in both AC/PDU and DC/busbar versions.

- Features fully redundant power:

  - N+N power supplies, or

  - Redundant in-rack power shelves connected to busbar.

- All I/O connectivity is moved to the front of the system.

- ConnectX-8 networking connects directly to GPUs via PCIe Gen6.

  - NICs, including cages for connectivity, are housed in the GPU tray.

- Power supplies are front-loaded with rear power connections.

- All cooling fans are accessible from the rear.

- Switched to E1.S cache drives from U.2 while maintaining the same capacity and configuration.

- A new, replaceable DC-SCM (Datacenter-ready Secure Control Module) contains the BMC.

- Supports up to 4 TB of RAM, configurable on-site with 128 GB DIMMs purchased from NVIDIA.

- The motherboard and GPU trays are installed on sliding rails for easy access.

- Features a new black front look with a distinguishing gold bezel.

<a id="dgx-b300-exploded-views"></a>

### DGX B300 Exploded Views
These exploded view diagrams depict the system components and their installations within the system. The front of the system provides access to the fans, drives, bezel, front cage, and power distribution board. The back of the system allows access to the GPU tray, motherboard tray, and power supplies.

![B300 Exploded View (AC)](_images/dgx-b300-ac-exploded-view.png)

Exploded View of DGX B300 with AC Power Components[\#](#id4 "Link to this image")

![B300 Exploded View (DC)](_images/dgx-b300-dc-exploded-view.png)

Exploded View of DGX B300 with DC Power Components[\#](#id5 "Link to this image")

<a id="power-specifications"></a>

### Power Specifications
The DGX B300 can be powered in two ways: using a busbar or a traditional data center power distribution unit (PDU) connected to the power supplies.

- Busbar version: Includes a clip at the back of the DGX B300 system to connect to a busbar-equipped rack. To energize the busbar, power shelves (not included with the DGX B300) need to be connected to it.

- Power supply version: Equipped with 12 power supplies for N+N power redundancy.

| Input            |                   | Specification for Each Power Supply |
|------------------|-------------------|-------------------------------------|
| 200-240 volts AC | 15 kW system max. | 3.3 kW @ 200-240 V, 16 A, 50-60 Hz  |
| 54 Volts DC      | 15 kW system max. | 300 A maximum current               |

Power Specifications[\#](#id6 "Link to this table") {#id6}

<a id="support-for-psu-redundancy-and-continuous-operation"></a>

#### Support for PSU Redundancy and Continuous Operation
The system includes 12 power supply units (PSU) configured for N+N redundancy, ensuring continuous operation and power reliability.

In an N+N redundancy configuration,

- The minimum number of required PSUs is six.

- If one PSU fails, troubleshoot the cause and replace the failed PSU immediately.

- The system only boots if at least three PSUs are operational. If fewer than three are operational, only the BMC is available.

- Do not operate the system with PSUs depopulated.

<a id="dgx-b300-locking-power-cord-specification"></a>

### DGX B300 Locking Power Cord Specification
The DGX B300 system is shipped with a set of twelve (12) locking power cords that have been qualified for use with the DGX B300 system to ensure regulatory compliance.

Warning

To avoid electric shock or fire, only use the NVIDIA-provided power cords to connect power to the DGX B300. For more information, refer to [Electrical Precautions](safety.html#electrical-precautions).

Important

Do not use the provided cables with any other product or for any other purpose.

Power Cord Specification

[TABLE]

<a id="using-the-locking-power-cords"></a>

### Using the Locking Power Cords
This section provides information about how to use the locking power cords.

Locking and Unlocking the PDU Side

Power Distribution Unit side

- To INSERT, push the cable into the PDU socket.

- To REMOVE, press the clips together and pull the cord out of the socket.

  ![](_images/locking-cord.png)

Locking/Unlocking the PSU Side (Cords with Twist-Lock Mechanism)

Power Supply (System) side - Twist locking

- To INSERT or REMOVE, ensure the cable is UNLOCKED and push/ pull into/out of the socket.

  ![](_images/cords.jpg)

<a id="front-panel-connections-and-controls"></a>

### Front Panel Connections and Controls
This section provides information about the front panel, connections, and controls of the DGX B300 system.

<a id="with-a-bezel"></a>

#### With a Bezel
This is an image of the DGX B300 system with a bezel.

![](_images/dgx-b300-with-bezel.png)

[TABLE]

<a id="without-a-bezel"></a>

#### Without a Bezel
The following images show the front views without the bezel of the DGX B300 system.

![B300 Front View (AC)](_images/dgx-b300-front-view-ac.png)

Front View of DGX B300 with AC Power Supplies[\#](#id7 "Link to this image")

![B300 Front View (DC)](_images/dgx-b300-front-view-dc.png)

Front View of DGX B300 (DC)[\#](#id8 "Link to this image")

Important

Refer to the section [First Boot Setup](first-boot-setup.html) for instructions on how to properly turn the system on or off.

<a id="rear-panel-modules"></a>

### Rear Panel Modules
The following images show the rear views including the AC power inlets and the DC power bus bar clip of the DGX B300 system.

![B300 Rear View (AC)](_images/dgx-b300-rear-view-ac.png)

Rear View of DGX B300 with AC Power Inlets[\#](#id9 "Link to this image")

![B300 Rear View (DC)](_images/dgx-b300-rear-view-dc.png)

Rear View of DGX B300 with DC Bus Bar Clip[\#](#id10 "Link to this image")

<a id="motherboard-connections-and-controls"></a>

### Motherboard Connections and Controls
The following image shows the motherboard connections and controls in a DGX B300 system.

![](_images/dgx-b300-port-view.png)

| Control | Description |
|----|----|
| Power button | Press to turn the system on or off. |
| UID (Unit identification) and LED | It blinks when the UID button is pressed from the front of the unit to help identify the unit that needs servicing. |
| BMC reset button | Press to manually reset the BMC. |

Motherboard Controls[\#](#id11 "Link to this table") {#id11}

See [Network Connections, Cables, and Adapters](#network-conn-cables-adapters) for details on the network connections.

<a id="motherboard-tray-components"></a>

### Motherboard Tray Components
The following image shows the motherboard tray components in the DGX B300 system.

![](_images/dgx-b300-mb-tray-comp.png)

<a id="gpu-tray-components"></a>

### GPU Tray Components
The following image shows the GPU tray components in the DGX B300 system.

![B300 GPU Tray (Side View)](_images/dgx-b300-gpu.png)

Side View of DGX B300 GPU Tray[\#](#id12 "Link to this image")

![B300 GPU Tray (Top View)](_images/dgx-b300-gpu-tray.png)

Top View of DGX B300 GPU Tray[\#](#id13 "Link to this image")

<a id="network-connections-cables-and-adapters"></a>

## Network Connections, Cables, and Adapters
This section provides information about network connections, cables, and adapters.

<a id="dgx-b300-port-description"></a>

### DGX B300 Port Description
This image shows the eight network ports located on the DGX B300 GPU tray.

![](_images/dgx-b300-osfpport-view.png)

This image shows the network ports on the DGX B300 system motherboard.

![](_images/dgx-b300-port-view.png)

This table provides an overview of the connectivity and configuration options available for each OSFP port and slot port.

[TABLE]

Port Designation[\#](#id14 "Link to this table") {#id14}

<a id="bmc-port-leds"></a>

### BMC Port LEDs
The BCM RJ-45 port has two LEDs.

The LED on the left indicates the speed. Solid green indicates the speed is 100M. Solid amber indicates the speed is 1G.

The LED on the right is green and flashes to indicate activity.

<a id="supported-network-cables-and-adapters"></a>

### Supported Network Cables and Adapters
The DGX B300 system is not shipped with network cables or adapters. You will need to purchase supported cables or adapters for your network.

The ConnectX-8 firmware determines which cables and adapters are supported. For a list of cables and adapters compatible with the NVIDIA ConnectX cards installed in the DGX B300 system,

1.  Visit the [NVIDIA Adapter Firmware Release](https://docs.nvidia.com/networking/category/adapterfw) page.

2.  Click the ConnectX model and select the corresponding firmware included in the DGX B300 system.

3.  From the left **Topics** pane, select the Validated and Supported Cables and Switches topic.

The default mode for BlueField-3 DPUs in DGX systems is NIC mode. To change a BlueField-3 DPU to DPU mode or return it to NIC mode, follow the instructions in [DOCA BlueField Modes of Operation](https://networking-docs.nvidia.com/doca/archive/3-5-0/bluefield-modes-of-operation).

<a id="dgx-b300-system-topology"></a>

## DGX B300 System Topology
The following figure shows the DGX B300 system topology.

[![](_images/dgx-b300-system-topology.png)](_images/dgx-b300-system-topology.png)

<a id="dgx-os-software"></a>

## DGX OS Software
The DGX B300 system comes pre-installed with a DGX software stack incorporating the following components:

- An Ubuntu server distribution using the optimized Linux kernel with supporting packages

- The following system management and monitoring software:

  - NVIDIA System Management (NVSM)

    Provides active health monitoring and system alerts for NVIDIA DGX nodes in a data center. It also provides simple commands for checking the health of the DGX B300 system from the command line.

  - Data Center GPU Management (DCGM)

    This software enables node-wide administration of GPUs and can be used for cluster and data-center level management.

- DGX B300 system support packages

- The NVIDIA GPU driver, including NVIDIA CUDA

- Docker Engine

- NVIDIA Container Toolkit

- NVIDIA Networking OpenFabrics Enterprise Distribution for Linux (DOCA-OFED)

- NVIDIA Networking Software Tools (MST)

- cachefilesd (daemon for managing cache data storage)

<a id="customer-support"></a>

## Customer Support
Contact NVIDIA Enterprise Support for assistance in reporting, troubleshooting, or diagnosing problems with your DGX B300 system. You can also contact NVIDIA Enterprise Support for help in moving the DGX B300 system.

- For contracted Enterprise Support questions, you can send an email to [enterprisesupport@nvidia.com](mailto:enterprisesupport%40nvidia.com).

- For more information on obtaining support, go to [NVIDIA Enterprise Support](https://www.nvidia.com/en-us/support/enterprise/).

Our support team can help collect appropriate information about your issue and involve internal resources as needed.

[](index.html "previous page")

previous

NVIDIA DGX B300 System User Guide

[](connect-dgx.html "next page")

next

Connecting to DGX B300

On this page

- [Hardware Overview](#hardware-overview)
  - [DGX B300 Physical and Operational Specifications](#dgx-b300-physical-and-operational-specifications)
  - [DGX B300 Feature Summary](#dgx-b300-feature-summary)
  - [Key Enhancements Over Previous DGX Systems](#key-enhancements-over-previous-dgx-systems)
  - [DGX B300 Exploded Views](#dgx-b300-exploded-views)
  - [Power Specifications](#power-specifications)
    - [Support for PSU Redundancy and Continuous Operation](#support-for-psu-redundancy-and-continuous-operation)
  - [DGX B300 Locking Power Cord Specification](#dgx-b300-locking-power-cord-specification)
  - [Using the Locking Power Cords](#using-the-locking-power-cords)
  - [Front Panel Connections and Controls](#front-panel-connections-and-controls)
    - [With a Bezel](#with-a-bezel)
    - [Without a Bezel](#without-a-bezel)
  - [Rear Panel Modules](#rear-panel-modules)
  - [Motherboard Connections and Controls](#motherboard-connections-and-controls)
  - [Motherboard Tray Components](#motherboard-tray-components)
  - [GPU Tray Components](#gpu-tray-components)
- [Network Connections, Cables, and Adapters](#network-connections-cables-and-adapters)
  - [DGX B300 Port Description](#dgx-b300-port-description)
  - [BMC Port LEDs](#bmc-port-leds)
  - [Supported Network Cables and Adapters](#supported-network-cables-and-adapters)
- [DGX B300 System Topology](#dgx-b300-system-topology)
- [DGX OS Software](#dgx-os-software)
- [Customer Support](#customer-support)
