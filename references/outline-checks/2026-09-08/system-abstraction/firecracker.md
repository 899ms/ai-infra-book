<!-- 从 firecracker.html 迁移的资料快照；原始 HTML SHA-256: e001391b533620bcd8bde5c8a01ad058a9a81e19a19f644ecc004a34e004e6bd。 -->

[![Firecracker logo](img/firecracker-logo@3x.png)](#home)

[![Firecracker logo](img/firecracker-13@3x.png)](#home) [Benefits](#benefits) [How it works](#how_it_works) [FAQs](#faq) [Learn more](#learn_more)

Secure and fast microVMs for serverless computing

Firecracker is an open source virtualization technology that is purpose-built for creating and managing secure, multi-tenant container and function-based services.

Open Source

### Firecracker VMM

Build your own microVM infrastructure. Full control, Apache 2.0 licensed.

[GitHub](https://github.com/firecracker-microvm/firecracker)

Fully Managed

### AWS Lambda MicroVMs

Serverless compute primitive with VM-level isolation, near-instant launch and resume speeds, and state preservation.

[Docs](https://aws.amazon.com/lambda/lambda-microvms/) [Workshop](https://s12d.com/mvmws)

[![](img/firecracker-13@3x.png)](#home)

[![](img/firecracker-13@3x.png)]() [Benefits](#benefits) [How it works](#how_it_works) [FAQs](#faq) [Learn more](#learn_more)

Firecracker

Firecracker is an open source virtualization technology purpose-built for creating and managing secure, multi-tenant container and function-based services. It enables you to deploy workloads in lightweight virtual machines (microVMs) that provide enhanced security and workload isolation over traditional VMs, while enabling the speed and resource efficiency of containers.

Open Source · Apache 2.0

AWS Lambda MicroVMs

For teams that want the capabilities of Firecracker without managing infrastructure, Lambda MicroVMs is a fully managed serverless compute primitive. Built on the same Firecracker virtualization powering 15 trillion+ monthly Lambda function invocations, it provides isolated sandboxes with near-instant launch, state persistence for up to 8 hours, and automatic suspend/resume. No capacity planning required.

Fully Managed · Serverless

Why Firecracker-based MicroVMs?

Firecracker (Open Source)

1

#### Security by Minimalism

Only 5 emulated devices. Minimal attack surface with KVM-based isolation.

2

#### Speed by Design

Boot in \<125ms. Create up to 150 microVMs per second per host.

3

#### Density and Efficiency

\<5 MiB overhead per VM. Pack thousands on a single server with built-in rate limiters.

AWS Lambda MicroVMs (Managed)

1

#### Zero Infrastructure

Start a MicroVM, connect over HTTP. No capacity planning, no isolation expertise needed.

2

#### Stateful and Persistent

Full memory and disk state preserved for up to 8 hours. Suspend when idle, resume on demand.

3

#### Elastic Scaling

Vertically scale up to 4x baseline during peak. Per-second billing, and no compute charges while suspended.

![Lambda MicroVMs](img/microvm@3x.png)

Lambda MicroVMs — isolated, stateful compute sandboxes built on Firecracker.

Purpose-built for AI agents, developer platforms, and multi-tenant workloads.

[Lambda MicroVM Documentation](https://aws.amazon.com/lambda/lambda-microvms/) [Lambda MicroVM Workshop](https://s12d.com/mvmws)

![](img/logo-icon@3x.png)

Firecracker is open-sourced under Apache License, version 2.0.

[![AWS Lambda](img/lambda-logo.svg)](https://aws.amazon.com/lambda/)

[ Join our GitHub Community](https://github.com/firecracker-microvm/firecracker) [ Chat about Firecracker on Slack](https://join.slack.com/t/firecracker-microvm/shared_invite/zt-3v81btcpe-usCf8Qk7k1gUlSAEKKdYMg)

How It Works

The following diagram depicts an example host running Firecracker microVMs.

![Firecracker diagram](img/diagram-desktop@3x.png) ![Firecracker diagram](img/graph-mobile@3x.png)

Firecracker runs in user space and uses the Linux Kernel-based Virtual Machine (KVM) to create microVMs. The fast startup time and low memory overhead of each microVM enables you to pack thousands of microVMs onto the same machine. This means that every function, container, or container group can be encapsulated with a virtual machine barrier, enabling workloads from different customers to run on the same machine, without any tradeoffs to security or efficiency. Firecracker is an [alternative to QEMU](https://www.redhat.com/en/blog/all-you-need-know-about-kvm-userspace) , an established VMM with a general purpose and broad feature set that allows it to host a variety of guest operating systems.

You can control the Firecracker process via a RESTful API that enables common actions such as configuring the number of vCPUs or starting the machine. It provides built-in rate limiters, which allows you to granularly control network and storage resources used by thousands of microVMs on the same machine. You can create and configure rate limiters via the Firecracker API and define flexible rate limiters that support bursts or specific bandwidth/operations limitations. Firecracker also provides a metadata service that securely shares configuration information between the host and guest operating system. You can set up and configure the metadata service using the Firecracker API. Each Firecracker microVM is further isolated with common Linux user-space security barriers by a companion program called "jailer". The jailer provides a second line of defense in case the virtualization barrier is ever compromised.

Firecracker is generally available on [64-bit Intel, AMD and Arm CPUs with support for hardware virtualization.](https://github.com/firecracker-microvm/firecracker#tested-platforms) Our latest roadmap can be found [here](https://github.com/orgs/firecracker-microvm/projects/42) .

FAQs

Who developed Firecracker?

Firecracker was built by developers at Amazon Web Services to enable services such as [AWS Lambda](https://aws.amazon.com/lambda/) to improve resource utilization and customer experience, while providing the security and isolation required of public cloud infrastructure. Firecracker started from Chromium OS's Virtual Machine Monitor, [crosvm](https://chromium.googlesource.com/chromiumos/platform/crosvm/) , an open source VMM written in Rust. Today, crosvm and Firecracker have diverged to serve very different customer needs. [Rust-vmm](https://github.com/rust-vmm) is an open source community where we collaborate with crosvm and other groups and individuals to build and share quality Rust virtualization components.

Why did you develop Firecracker?

When we launched Lambda in November of 2014, we were focused on providing a secure [serverless](https://aws.amazon.com/serverless/) experience. At launch we used per-customer EC2 instances to provide strong security and isolation between customers. As Lambda grew, we saw the need for technology to provide a highly secure, flexible, and efficient runtime environment for services like Lambda. Using our experience building isolated EC2 instances with hardware virtualization technology, we started an effort to build a VMM that was tailored to run serverless functions and integrate with container ecosystems.

What processors does Firecracker support?

The Firecracker VMM is built to be processor agnostic. 64-bit Intel, AMD and Arm CPUs with hardware virtualization support are generally available for production workloads.

What language is Firecracker written in?

Firecracker is written in Rust.

Can Firecracker be used within the container ecosystem?

Yes. Firecracker is used by/integrated with (in alphabetical order): containerd via [firecracker-containerd](https://github.com/firecracker-microvm/firecracker-containerd), [E2B](https://e2b.dev), [Fly.io](https://fly.io), [Kata Containers](https://github.com/kata-containers/kata-containers/blob/main/docs/hypervisors.md), [Koyeb](https://www.koyeb.com), [Northflank](https://northflank.com), [OpenNebula](https://opennebula.io/firecracker/), [PandastackAI](https://www.pandastack.ai), [Qovery](https://www.qovery.com), [UniK](https://github.com/solo-io/unik), [webapp.io](https://webapp.io), and [microvm.nix](https://github.com/astro/microvm.nix).

What is the difference between Firecracker and QEMU?

Firecracker is an [alternative to QEMU](https://www.redhat.com/en/blog/all-you-need-know-about-kvm-userspace) that is purpose-built for running serverless functions and containers safely and efficiently, and nothing more. Firecracker is written in Rust, provides a minimal required device model to the guest operating system while excluding non-essential functionality (only 5 emulated devices are available: virtio-net, virtio-block, virtio-vsock, serial console, and a minimal keyboard controller used only to stop the microVM). This, along with a streamlined kernel loading process enables a \< 125 ms startup time and a \< 5 MiB memory footprint. The Firecracker process also provides a RESTful control API, handles resource rate limiting for microVMs, and provides a microVM metadata service to enable the sharing of configuration data between the host and guest.

What operating systems are supported by Firecracker?

Firecracker supports Linux host and guest operating systems with kernel versions 4.14 and above, as well as [OSv](http://blog.osv.io/blog/2019/04/19/making-OSv-run-on-firecraker/) guests. The long-term support plan is still under discussion.

What is the open source license for Firecracker?

Firecracker is [licensed](https://github.com/firecracker-microvm/firecracker/blob/master/LICENSE) under Apache License, version 2.0, allowing you to freely use, copy, and distribute your changes under the terms of your choice. Read more about the [Apache 2.0 license](https://www.apache.org/licenses/LICENSE-2.0) . Crosvm code sections are licensed under a [BSD-3-Clause license](https://opensource.org/licenses/BSD-3-Clause) that also allows you to use, copy, and distribute your changes under the terms of your choice.

How can I contribute?

Firecracker is an AWS open source project that encourages contributions from customers and the developer community. Any contribution is welcome as long as it aligns with our [charter](https://github.com/firecracker-microvm/firecracker/blob/master/CHARTER.md) . You can learn more about how to contribute in [CONTRIBUTING.md](https://github.com/firecracker-microvm/firecracker/blob/master/CONTRIBUTING.md) . You can chat with others in the community on the [Firecracker Slack workspace](https://join.slack.com/t/firecracker-microvm/shared_invite/zt-3v81btcpe-usCf8Qk7k1gUlSAEKKdYMg) .

Still didn’t find your answer?

[Contact us](mailto:firecracker-maintainers@amazon.com)

Learn More

[](https://aws.amazon.com/blogs/aws/firecracker-lightweight-virtualization-for-serverless-computing)

JEFF BARR BLOG Firecracker – Lightweight Virtualization for Serverless Computing

Read about why AWS decided to build Firecracker, and how it improves security and efficiency.

Read more

[](https://aws.amazon.com/blogs/opensource/firecracker-open-source-secure-fast-microvm-serverless/)

OPEN SOURCE BLOG Announcing the Firecracker Open Source Technology

Read about how to get started with Firecracker, where the project is headed, and how you can join, contribute, and collaborate.

Read more

Get Involved

[ Join our GitHub Community](https://github.com/firecracker-microvm/firecracker) [ Chat about Firecracker on Slack](https://join.slack.com/t/firecracker-microvm/shared_invite/zt-3v81btcpe-usCf8Qk7k1gUlSAEKKdYMg)

[![Firecracker logo](img/firecracker-logo@3x.png)](#home)

©2018-2026, Amazon Web Services, Inc. or its affiliates. All rights reserved.
