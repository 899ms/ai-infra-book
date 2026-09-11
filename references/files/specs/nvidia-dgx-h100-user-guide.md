<!-- 从 nvidia-dgx-h100-user-guide.html 迁移的资料快照；原始 HTML SHA-256: aa3dd7e72e910b03e697dfe7cfb76efc04bb9382f0c73cf620eba348eea6c945。 -->

<div id="main-content" class="bd-main" role="main">

<div class="bd-content">

<div class="bd-article-container">

<div class="bd-header-article d-print-none">

<div class="header-article-items header-article__inner">

<div class="header-article-items__start">

<div class="header-article-item">

- [NVIDIA Docs Hub](https://docs.nvidia.com)
- [NVIDIA DGX Platform](https://docs.nvidia.com/dgx)
- [NVIDIA DGX Systems](https://docs.nvidia.com/dgx-systems)
- [NVIDIA DGX H100/H200 User Guide](index.html)
- Introduction to NVIDIA DGX H100/H200 Systems

</div>

</div>

<div class="header-article-items__end">

<div class="header-article-item">

<div class="header-article-item">

<div class="d-flex justify-content-end w-100">

<a href="https://surveys.hotjar.com/4904bf71-6484-47a7-83ff-4715cceabdb5" id="openPopupButton">Is this page helpful?</a>

</div>

</div>

</div>

</div>

</div>

</div>

<div id="searchbox">

</div>

<div id="introduction-to-nvidia-dgx-h100-h200-systems" class="section">

<span id="introduction-to-dgxh100"></span>

# Introduction to NVIDIA DGX H100/H200 Systems<a href="#introduction-to-nvidia-dgx-h100-h200-systems" class="headerlink" title="Link to this heading">#</a>

The NVIDIA DGX™ H100/H200 Systems are the universal systems purpose-built for all AI infrastructure and workloads from analytics to training to inference. The DGX H100/H200 systems are built on eight NVIDIA H100 Tensor Core GPUs or eight NVIDIA H200 Tensor Core GPUs.

![](_images/dgx-h100-with-bezel.png)

<div id="hardware-overview" class="section">

<span id="hw-overview"></span>

## Hardware Overview<a href="#hardware-overview" class="headerlink" title="Link to this heading">#</a>

<div id="dgx-h100-h200-component-descriptions" class="section">

<span id="models-comp-desc-dgxh100"></span>

### DGX H100/H200 Component Descriptions<a href="#dgx-h100-h200-component-descriptions" class="headerlink" title="Link to this heading">#</a>

The NVIDIA DGX H100 (640 GB)/H200 (1,128 GB) systems include the following components.

<div class="pst-scrollable-table-container">

<table id="id2" class="table">
<caption><span class="caption-text">Table 1. Component Description</span><a href="#id2" class="headerlink" title="Link to this table">#</a></caption>
<colgroup>
<col style="width: 35%" />
<col style="width: 65%" />
</colgroup>
<thead>
<tr class="row-odd">
<th class="head"><p>Component</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even">
<td><p>GPU</p></td>
<td><div class="line">
For H100: 8 x NVIDIA H100 GPUs that provide 640 GB total GPU memory
</div>
<div class="line">
For H200: 8 x NVIDIA H200 GPUs that provide 1,128 GB total GPU memory
</div></td>
</tr>
<tr class="row-odd">
<td><p>CPU</p></td>
<td><p>2 x Intel Xeon 8480C PCIe Gen5 CPUs with 56 cores each 2.0/2.9/3.8 GHz (base/all core turbo/Max turbo)</p></td>
</tr>
<tr class="row-even">
<td><p>NVSwitch</p></td>
<td><p>4 x 4th generation NVLinks that provide 900 GB/s GPU-to-GPU bandwidth</p></td>
</tr>
<tr class="row-odd">
<td><p>Storage (OS)</p></td>
<td><p>2 x 1.92 TB NVMe M.2 SSD (ea) in RAID 1 array</p></td>
</tr>
<tr class="row-even">
<td><p>Storage (Data Cache)</p></td>
<td><p>8 x 3.84 TB NVMe U.2 SED (ea) in RAID 0 array</p></td>
</tr>
<tr class="row-odd">
<td><p>Network (Cluster) card</p></td>
<td><p>4 x OSFP ports for 8 x NVIDIA® ConnectX®-7 Single Port InfiniBand Cards</p>
<p>Each card provides the following speeds:</p>
<ul>
<li><p>InfiniBand (default): Up to 400Gbps</p></li>
<li><p>Ethernet: 400GbE, 200GbE, 100GbE, 50GbE, 40GbE, 25GbE, and 10GbE</p></li>
</ul></td>
</tr>
<tr class="row-even">
<td><p>Network (storage and in-band management) card</p></td>
<td><p>2 x NVIDIA® ConnectX®-7 Dual Port Ethernet Cards</p>
<p>Each card provides the following speeds:</p>
<ul>
<li><p>Ethernet (default): 400GbE, 200GbE, 100GbE, 50GbE, 40GbE, 25GbE, and 10GbE</p></li>
<li><p>InfiniBand: Up to 400Gbps</p></li>
</ul></td>
</tr>
<tr class="row-odd">
<td><p>System memory (DIMM)</p></td>
<td><p>2 TB using 32 x DIMMs</p></td>
</tr>
<tr class="row-even">
<td><p>BMC (out-of-band system management)</p></td>
<td><p>1 GbE RJ45 interface</p>
<p>Supports Redfish, IPMI, SNMP, KVM, and Web user interface</p></td>
</tr>
<tr class="row-odd">
<td><p>System management interfaces</p></td>
<td><p>Dual port 100GbE in slot 3 and 10 GbE RJ45 interface</p></td>
</tr>
<tr class="row-even">
<td><p>Power supply</p></td>
<td><p>6 x 3.3 kW</p></td>
</tr>
</tbody>
</table>

</div>

</div>

<div id="mechanical-specifications" class="section">

<span id="mech-specs"></span>

### Mechanical Specifications<a href="#mechanical-specifications" class="headerlink" title="Link to this heading">#</a>

<div class="pst-scrollable-table-container">

| Feature       | Description               |
|---------------|---------------------------|
| Form Factor   | 8U Rackmount              |
| Height        | 14” (356 mm)              |
| Width         | 19” (482.3 mm) max        |
| Depth         | 35.3” (897.1 mm) max      |
| System Weight | 287.6 lbs (130.45 kg) max |

<span class="caption-text">Table 2. Mechanical Specifications</span><a href="#id3" class="headerlink" title="Link to this table">#</a> {#id3}

</div>

</div>

<div id="power-specifications" class="section">

<span id="power-specs"></span>

### Power Specifications<a href="#power-specifications" class="headerlink" title="Link to this heading">#</a>

The DGX H100/H200 system contains six power supplies with balanced distribution of the power load.

<div class="pst-scrollable-table-container">

| Input            |              | Specification for Each Power Supply |
|------------------|--------------|-------------------------------------|
| 200-240 volts AC | 10.2 kW max. | 3300 W @ 200-240 V, 16 A, 50-60 Hz  |

<span class="caption-text">Table 3. Power Specifications</span><a href="#id4" class="headerlink" title="Link to this table">#</a> {#id4}

</div>

<div id="support-for-psu-redundancy-and-continuous-operation" class="section">

<span id="supp-nn-red"></span>

#### Support for PSU Redundancy and Continuous Operation<a href="#support-for-psu-redundancy-and-continuous-operation" class="headerlink" title="Link to this heading">#</a>

The system includes six power supply units (PSU) configured for 4+2 redundancy.

Refer to the following additional considerations:

- If a PSU fails, troubleshoot the cause and replace the failed PSU immediately.

- If three PSUs lose power as a result of a data center issue or power distribution unit failure, the system continues to function, but at a reduced performance level.

- If only three PSUs have power, shut down the system before replacing an operational PSU.

- The system only boots if at least three PSUs are operational. If fewer than three PSUs are operational, only the BMC is available.

- Do not operate the system with PSUs depopulated.

</div>

</div>

<div id="dgx-h100-h200-locking-power-cord-specification" class="section">

<span id="lock-power-cord-spec"></span>

### DGX H100/H200 Locking Power Cord Specification<a href="#dgx-h100-h200-locking-power-cord-specification" class="headerlink" title="Link to this heading">#</a>

The DGX H100/H200 system is shipped with a set of six (6) locking power cords that have been qualified for use with the DGX H100/H200 system to ensure regulatory compliance.

<div class="admonition warning">

Warning

To avoid electric shock or fire, only use the NVIDIA-provided power cords to connect power to the DGX H100/H200. For more details, refer to <a href="safety.html#electrical-precautions" class="reference internal"><span class="std std-ref">Electrical Precautions</span></a>.

</div>

<div class="admonition important">

Important

Do not use the provided cables with any other product or for any other purpose.

</div>

Power Cord Specification

<div class="pst-scrollable-table-container">

<table class="table">
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr class="row-odd">
<th class="head"><p>Power Cord Feature</p></th>
<th class="head"><p>Specification</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even">
<td><p>Electrical</p></td>
<td><p>250VAC, 20A</p></td>
</tr>
<tr class="row-odd">
<td><p>Plug Standard</p></td>
<td><p>C19/C20</p></td>
</tr>
<tr class="row-even">
<td><p>Dimension</p></td>
<td><p>1200mm length</p></td>
</tr>
<tr class="row-odd">
<td><p>Compliance</p></td>
<td><p>Cord: UL62, IEC60227</p>
<p>Connector/Plug: IEC60320-1</p></td>
</tr>
</tbody>
</table>

</div>

</div>

<div id="using-the-locking-power-cords" class="section">

<span id="use-lock-power-cords"></span>

### Using the Locking Power Cords<a href="#using-the-locking-power-cords" class="headerlink" title="Link to this heading">#</a>

This section provides information about how to use the locking power cords.

Locking and Unlocking the PDU Side

Power Distribution Unit side

- To INSERT, push the cable into the PDU socket.

- To REMOVE, press the clips together and pull the cord out of the socket.

  ![](_images/locking-cord.png)

Locking/Unlocking the PSU Side (Cords with Twist-Lock Mechanism)

Power Supply (System) side - Twist locking

- To INSERT or REMOVE make sure the cable is UNLOCKED and push/ pull into/out of the socket.

  ![](_images/cords.jpg)

</div>

<div id="environmental-specifications" class="section">

<span id="env-spec"></span>

### Environmental Specifications<a href="#environmental-specifications" class="headerlink" title="Link to this heading">#</a>

Here are the environmental specifications for your DGX H100/H200 system.

<div class="pst-scrollable-table-container">

| Feature               | Specification                        |
|-----------------------|--------------------------------------|
| Operating Temperature | 5° C to 30° C (41° F to 86° F)       |
| Relative Humidity     | 20% to 80% non-condensing            |
| Airflow               | 1105 CFM Front-to-Back @ 80% fan PWM |
| Heat Output           | 38,557 BTU/hr                        |

</div>

</div>

<div id="front-panel-connections-and-controls" class="section">

<span id="front-panel-conn-controls"></span>

### Front Panel Connections and Controls<a href="#front-panel-connections-and-controls" class="headerlink" title="Link to this heading">#</a>

This section provides information about the front panel, connections, and controls of the DGX H100/H200 system.

<div id="with-a-bezel" class="section">

<span id="with-bezel"></span>

#### With a Bezel<a href="#with-a-bezel" class="headerlink" title="Link to this heading">#</a>

Here is an image of the DGX H100/H200 system with a bezel.

![](_images/dgx-h100-with-bezel.png)

<div class="pst-scrollable-table-container">

<table class="table">
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr class="row-odd">
<th class="head"><p>Control</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even">
<td><p>Power Button</p></td>
<td><p>Press to turn the DGX H100/H200 system On or Off.</p>
<ul>
<li><p>Green flashing (1 Hz): Standby (BMC booted)</p></li>
<li><p>Green flashing (4 Hz): POST in progress</p></li>
<li><p>Green solid On: Power On</p></li>
</ul></td>
</tr>
<tr class="row-odd">
<td><p>ID Button</p></td>
<td><p>Press to have the blue LED turn On or blink (configurable through the BMC) as an identifier during servicing.</p>
<p>Also causes an LED on the back of the unit to flash as an identifier during servicing.</p></td>
</tr>
<tr class="row-even">
<td><p>Fault LED</p></td>
<td><p>Amber On: System or component faulted</p></td>
</tr>
</tbody>
</table>

</div>

</div>

<div id="with-the-bezel-removed" class="section">

<span id="dgxh100-no-bezel"></span>

#### With the Bezel Removed<a href="#with-the-bezel-removed" class="headerlink" title="Link to this heading">#</a>

Here is an image of the DGX H100/H200 system without a bezel.

![](_images/dgx-h100-front-view.png)

<div class="admonition important">

Important

Refer to the section <a href="first-boot-setup.html" class="reference internal"><span class="doc">First Boot Setup</span></a> for instructions on how to properly turn the system on or off.

</div>

</div>

</div>

<div id="rear-panel-modules" class="section">

### Rear Panel Modules<a href="#rear-panel-modules" class="headerlink" title="Link to this heading">#</a>

Here is an image that shows the real panel modules on DGX H100/H200.

![](_images/dgx-h100-rear-panel-modules.png)

</div>

<div id="motherboard-connections-and-controls" class="section">

### Motherboard Connections and Controls<a href="#motherboard-connections-and-controls" class="headerlink" title="Link to this heading">#</a>

Here is an image that shows the motherboard connections and controls in a DGX H100/H200 system.

![](_images/dgx-h100-port-view.png)

<div class="pst-scrollable-table-container">

| Control | Description |
|----|----|
| Power Button | Press to turn the system On or Off. |
| ID LED Button | Blinks when ID button is pressed from the front of the unit as an aid in identifying the unit needing servicing. |
| BMC Reset button | Press to manually reset the BMC. |

<span class="caption-text">Table 4. Motherboard Controls</span><a href="#id5" class="headerlink" title="Link to this table">#</a> {#id5}

</div>

See <a href="#network-conn-cables-adaptors" class="reference internal"><span class="std std-ref">Network Connections, Cables, and Adaptors</span></a> for details on the network connections.

</div>

<div id="motherboard-tray-components" class="section">

### Motherboard Tray Components<a href="#motherboard-tray-components" class="headerlink" title="Link to this heading">#</a>

Here is an image that shows the motherboard tray components in a DGX H100/H200 system.

![](_images/dgx-h100-mb-tray-comp.png)

</div>

<div id="gpu-tray-components" class="section">

### GPU Tray Components<a href="#gpu-tray-components" class="headerlink" title="Link to this heading">#</a>

Here is an image of the GPU tray components in a DGX H100/H200 system.

![](_images/dgx-h100-gpu-tray.png)

</div>

</div>

<div id="network-connections-cables-and-adaptors" class="section">

<span id="network-conn-cables-adaptors"></span>

## Network Connections, Cables, and Adaptors<a href="#network-connections-cables-and-adaptors" class="headerlink" title="Link to this heading">#</a>

This section provides information about network connections, cables, and adaptors.

<div id="network-ports" class="section">

### Network Ports<a href="#network-ports" class="headerlink" title="Link to this heading">#</a>

Here is an image that shows the network ports on a DGX H100/H200 system.

![](_images/dgx-h100-port-view.png)

<div class="pst-scrollable-table-container">

<table id="id6" class="table">
<caption><span class="caption-text">Table 5. Network Port Mapping</span><a href="#id6" class="headerlink" title="Link to this table">#</a></caption>
<thead>
<tr class="row-odd">
<th class="head"></th>
<th class="head"></th>
<th colspan="2" class="head"><p>Port Designation</p></th>
<th class="head"></th>
</tr>
<tr class="row-even">
<th class="head"><p>Port</p></th>
<th class="head"><p>PCI Bus</p></th>
<th class="head"><p>Default</p></th>
<th class="head"><p>Optional</p></th>
<th class="head"><p>RDMA</p></th>
</tr>
</thead>
<tbody>
<tr class="row-odd">
<td><p>OSFP1P1</p></td>
<td><p>dc:00.0</p></td>
<td><p>ibp220s0</p></td>
<td><p>enp220s0np0</p></td>
<td><p>mlx5_11</p></td>
</tr>
<tr class="row-even">
<td><p>OSFP1P2</p></td>
<td><p>9a:00.0</p></td>
<td><p>ibp154s0</p></td>
<td><p>enp154s0np0</p></td>
<td><p>mlx5_6</p></td>
</tr>
<tr class="row-odd">
<td><p>OSFP2P1</p></td>
<td><p>ce:00.0</p></td>
<td><p>ibp206s0</p></td>
<td><p>enp206s0np0</p></td>
<td><p>mlx5_10</p></td>
</tr>
<tr class="row-even">
<td><p>OSFP2P2</p></td>
<td><p>c0:00.0</p></td>
<td><p>ibp192s0</p></td>
<td><p>enp192s0np0</p></td>
<td><p>mlx5_9</p></td>
</tr>
<tr class="row-odd">
<td><p>OSFP3P1</p></td>
<td><p>4f:00.0</p></td>
<td><p>ibp79s0</p></td>
<td><p>enp79s0np0</p></td>
<td><p>mlx5_4</p></td>
</tr>
<tr class="row-even">
<td><p>OSFP3P2</p></td>
<td><p>40:00.0</p></td>
<td><p>ibp64s0</p></td>
<td><p>enp64s0np0</p></td>
<td><p>mlx5_3</p></td>
</tr>
<tr class="row-odd">
<td><p>OSFP4P1</p></td>
<td><p>5e:00.0</p></td>
<td><p>ibp94s0</p></td>
<td><p>enp94s0np0</p></td>
<td><p>mlx5_5</p></td>
</tr>
<tr class="row-even">
<td><p>OSFP4P2</p></td>
<td><p>18:00.0</p></td>
<td><p>ibp24s0</p></td>
<td><p>enp24s0np0</p></td>
<td><p>mlx5_0</p></td>
</tr>
<tr class="row-odd">
<td><p>Slot1 P1</p></td>
<td><p>aa:00.0</p></td>
<td><p>ibp170s0f0</p></td>
<td><p>enp170s0f0np0</p></td>
<td><p>mlx5_7</p></td>
</tr>
<tr class="row-even">
<td><p>Slot1 P2</p></td>
<td><p>aa:00.1</p></td>
<td><p>enp170s0f1np1</p></td>
<td><p>ibp170s0f1</p></td>
<td><p>mlx5_8</p></td>
</tr>
<tr class="row-odd">
<td><p>Slot2 P1</p></td>
<td><p>29:00.0</p></td>
<td><p>ibp41s0f0</p></td>
<td><p>enp41s0f0np0</p></td>
<td><p>mlx5_1</p></td>
</tr>
<tr class="row-even">
<td><p>Slot2 P2</p></td>
<td><p>29:00.1</p></td>
<td><p>enp41s0f1np1</p></td>
<td><p>ibp41s0f1</p></td>
<td><p>mlx5_2</p></td>
</tr>
<tr class="row-odd">
<td><p>Slot3 P1</p></td>
<td><p>82:00.0</p></td>
<td><p>ens6f0</p></td>
<td><p>N/A</p></td>
<td><p>irdma0</p></td>
</tr>
<tr class="row-even">
<td><p>Slot3 P2</p></td>
<td><p>82:00.1</p></td>
<td><p>ens6f1</p></td>
<td><p>N/A</p></td>
<td><p>irdma1</p></td>
</tr>
<tr class="row-odd">
<td><p>On-board</p></td>
<td><p>0b:00.0</p></td>
<td><p>eno3</p></td>
<td><p>N/A</p></td>
<td></td>
</tr>
</tbody>
</table>

</div>

</div>

<div id="compute-and-storage-networking" class="section">

### Compute and Storage Networking<a href="#compute-and-storage-networking" class="headerlink" title="Link to this heading">#</a>

![](_images/dgx-h100-storage-nw.png)

</div>

<div id="network-modules" class="section">

<span id="nw-modules"></span>

### Network Modules<a href="#network-modules" class="headerlink" title="Link to this heading">#</a>

- New form factor for aggregate PCIe network devices

- Consolidates four ConnectX-7 networking cards into a single device

- Two networking modules are installed on interposer board

- Interposer board connects to CPUs on one end and to GPU tray on the other

- DensiLink cables are used to go directly from ConnectX-7 networking cards to OSFP connectors at the back of the system

Each DensiLink cable has two ports, one from each ConnectX-7 card

<div class="pst-scrollable-table-container">

| Port    | ConnectX Device | Network Module/CPU | GPU | Default  | RDMA    |
|---------|-----------------|--------------------|-----|----------|---------|
| OSFP1P1 | CX0             | 1                  | 7   | ibp220s0 | mlx5_11 |
| OSFP1P2 | CX1             | 1                  | 4   | ibp154s0 | mlx5_6  |
| OSFP2P1 | CX2             | 1                  | 6   | ibp206s0 | mlx5_10 |
| OSFP2P2 | CX3             | 1                  | 5   | ibp192s0 | mlx5_9  |
| OSFP3P1 | CX2             | 0                  | 2   | ibp79s0  | mlx5_4  |
| OSFP3P2 | CX3             | 0                  | 1   | ibp64s0  | mlx5_3  |
| OSFP4P1 | CX0             | 0                  | 3   | ibp94s0  | mlx5_5  |
| OSFP4P2 | CX1             | 0                  | 0   | ibp24s0  | mlx5_0  |

<span class="caption-text">Table 6. Network Modules</span><a href="#id7" class="headerlink" title="Link to this table">#</a> {#id7}

</div>

![](_images/network-modules-2.png)

</div>

<div id="bmc-port-leds" class="section">

### BMC Port LEDs<a href="#bmc-port-leds" class="headerlink" title="Link to this heading">#</a>

The BCM RJ-45 port has two LEDs.

The LED on the left indicates the speed. Solid green indicates the speed is 100M. Solid amber indicates the speed is 1G.

The LED on the right is green and flashes to indicate activity.

</div>

<div id="supported-network-cables-and-adaptors" class="section">

<span id="supp-network-cables-adap"></span>

### Supported Network Cables and Adaptors<a href="#supported-network-cables-and-adaptors" class="headerlink" title="Link to this heading">#</a>

The DGX H100/H200 system is not shipped with network cables or adaptors. You will need to purchase supported cables or adaptors for your network.

The ConnectX-7 firmware determines which cables and adaptors are supported. For a list of cables and adaptors compatible with the NVIDIA ConnectX cards installed in the DGX H100/H200 system,

1.  Visit the <a href="https://docs.nvidia.com/networking/category/adapterfw" class="reference external">NVIDIA Adapter Firmware Release</a> page.

2.  Click the ConnectX model and select the corresponding firmware included in the DGX H100/H200 system.

3.  From the left **Topics** pane, select the Validated and Supported Cables and Switches topic.

</div>

</div>

<div id="dgx-h100-200-system-topology" class="section">

<span id="system-topology"></span>

## DGX H100/200 System Topology<a href="#dgx-h100-200-system-topology" class="headerlink" title="Link to this heading">#</a>

The following figure shows the DGX H100/H200 system topology.

<a href="_images/dgx-h100-system-topology.png" class="reference internal image-reference"><img src="_images/dgx-h100-system-topology.png" style="width: 700px;" alt="_images/dgx-h100-system-topology.png" /></a>

</div>

<div id="dgx-os-software" class="section">

<span id="id1"></span>

## DGX OS Software<a href="#dgx-os-software" class="headerlink" title="Link to this heading">#</a>

The DGX H100/H200 system comes pre-installed with a DGX software stack incorporating the following components:

- An Ubuntu server distribution with supporting packages.

- The following system management and monitoring software:

  - NVIDIA System Management (NVSM)

    Provides active health monitoring and system alerts for NVIDIA DGX nodes in a data center. It also provides simple commands for checking the health of the DGX H100/H200 system from the command line.

  - Data Center GPU Management (DCGM)

    This software enables node-wide administration of GPUs and can be used for cluster and data-center level management.

- DGX H100/H200 system support packages.

- The NVIDIA GPU driver

- Docker Engine

- NVIDIA Container Toolkit

- NVIDIA Networking OpenFabrics Enterprise Distribution for Linux (MOFED)

- NVIDIA Networking Software Tools (MST)

- cachefilesd (daemon for managing cache data storage)

</div>

<div id="customer-support" class="section">

## Customer Support<a href="#customer-support" class="headerlink" title="Link to this heading">#</a>

Contact NVIDIA Enterprise Support for assistance in reporting, troubleshooting, or diagnosing problems with your DGX H100/H200 system. Also contact NVIDIA Enterprise Support for assistance in moving the DGX H100/H200 system.

- For contracted Enterprise Support questions, you can send an email to <a href="mailto:enterprisesupport%40nvidia.com" class="reference external">enterprisesupport<span>@</span>nvidia<span>.</span>com</a>.

- For additional details about how to obtain support, go to <a href="https://www.nvidia.com/en-us/support/enterprise/" class="reference external">NVIDIA Enterprise Support</a>.

Our support team can help collect appropriate information about your issue and involve internal resources as needed.

</div>

</div>

<div class="prev-next-area">

<a href="index.html" class="left-prev" title="previous page"><em></em></a>

<div class="prev-next-info">

previous

NVIDIA DGX H100/H200 System User Guide

</div>

<a href="connect-dgx.html" class="right-next" title="next page"></a>

<div class="prev-next-info">

next

Connecting to DGX H100/H200

</div>

</div>

</div>

<div id="pst-secondary-sidebar" class="bd-sidebar-secondary bd-toc">

<div class="sidebar-secondary-items sidebar-secondary__inner">

<div class="sidebar-secondary-item">

<div id="pst-page-navigation-heading-2" class="page-toc tocsection onthispage">

On this page

</div>

- <a href="#hardware-overview" class="reference internal nav-link">Hardware Overview</a>
  - <a href="#dgx-h100-h200-component-descriptions" class="reference internal nav-link">DGX H100/H200 Component Descriptions</a>
  - <a href="#mechanical-specifications" class="reference internal nav-link">Mechanical Specifications</a>
  - <a href="#power-specifications" class="reference internal nav-link">Power Specifications</a>
    - <a href="#support-for-psu-redundancy-and-continuous-operation" class="reference internal nav-link">Support for PSU Redundancy and Continuous Operation</a>
  - <a href="#dgx-h100-h200-locking-power-cord-specification" class="reference internal nav-link">DGX H100/H200 Locking Power Cord Specification</a>
  - <a href="#using-the-locking-power-cords" class="reference internal nav-link">Using the Locking Power Cords</a>
  - <a href="#environmental-specifications" class="reference internal nav-link">Environmental Specifications</a>
  - <a href="#front-panel-connections-and-controls" class="reference internal nav-link">Front Panel Connections and Controls</a>
    - <a href="#with-a-bezel" class="reference internal nav-link">With a Bezel</a>
    - <a href="#with-the-bezel-removed" class="reference internal nav-link">With the Bezel Removed</a>
  - <a href="#rear-panel-modules" class="reference internal nav-link">Rear Panel Modules</a>
  - <a href="#motherboard-connections-and-controls" class="reference internal nav-link">Motherboard Connections and Controls</a>
  - <a href="#motherboard-tray-components" class="reference internal nav-link">Motherboard Tray Components</a>
  - <a href="#gpu-tray-components" class="reference internal nav-link">GPU Tray Components</a>
- <a href="#network-connections-cables-and-adaptors" class="reference internal nav-link">Network Connections, Cables, and Adaptors</a>
  - <a href="#network-ports" class="reference internal nav-link">Network Ports</a>
  - <a href="#compute-and-storage-networking" class="reference internal nav-link">Compute and Storage Networking</a>
  - <a href="#network-modules" class="reference internal nav-link">Network Modules</a>
  - <a href="#bmc-port-leds" class="reference internal nav-link">BMC Port LEDs</a>
  - <a href="#supported-network-cables-and-adaptors" class="reference internal nav-link">Supported Network Cables and Adaptors</a>
- <a href="#dgx-h100-200-system-topology" class="reference internal nav-link">DGX H100/200 System Topology</a>
- <a href="#dgx-os-software" class="reference internal nav-link">DGX OS Software</a>
- <a href="#customer-support" class="reference internal nav-link">Customer Support</a>

</div>

</div>

</div>

</div>

</div>
