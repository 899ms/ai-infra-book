# Docker24版本诊断

使用[Docker官方静态归档](https://download.docker.com/linux/static/stable/x86_64/docker-24.0.9.tgz)下载24.0.9，package.tgz SHA256为692ecfc28333485d184f628b74c25b2894cee9495a51a5418ba60ef95bf733ca，远端保留在tools/docker-24.0.9。未覆盖系统二进制。daemon.log确认version=24.0.9、commit=fca702d。

default与seccomp/AppArmor unconfined两条件均捕获成功，但restore仍content commit already exists。两容器清理、独立dockerd退出0。此组仅更换daemon/客户端PATH，未显式指定独立containerd地址，因此不能据其声称containerd版本及存储完全隔离。

后续docker24-full显式启动独立containerd进程及root/state/socket，继续验证此问题。上游[moby #47456](https://github.com/moby/moby/pull/47456)针对v25的digest编码问题，维护者明确无需v24回补；不把那个修复自动当成本次already exists错误的已证实根因。
