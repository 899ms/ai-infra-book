# 隔离Docker daemon恢复诊断

2026-09-15在rtx-pro执行；使用已安装Docker28.5.2及CRIU3.16.1，没有修改系统daemon配置或重启系统服务。配置依据[Docker多daemon说明](https://docs.docker.com/reference/cli/dockerd/#run-multiple-daemons)：独立data-root、exec-root、PID、Unix socket、配置文件及containerd命名空间，禁用bridge、iptables、ip6tables、IP转发与masquerade。不开放TCP Docker API。

首次daemon启动失败：深层exec-root使libnetwork Unix socket超过长度限制，报bind invalid argument。原daemon.log、配置和退出记录保留。attempt2改用/run/book1102-iso2和/run/book1102-iso2.sock，成功启动独立daemon；基础镜像从系统Docker save，再load至独立存储，临时tar随后删除。

attempt2实际运行两个最小Python进程：default和seccomp/AppArmor unconfined。两者checkpoint create成功，但docker start --checkpoint均在containerd内容提交时遇到already exists，尚未进入成功的内存恢复。新data-root也能复现，说明冲突并非仅由原系统daemon旧实验残留内容引起；不能据此断言所有Docker版本都有同样问题。

两实验容器docker rm均成功。probe程序exit0表示结果已记录，不能当restore成功。独立daemon由父进程终止并wait，退出码0，PID3288386记录在attempt2/cleanup.json；首轮daemon启动失败也已回收。远端data-root保留，本地仅同步配置、脚本、命令、日志和结果，未复制镜像层。系统daemon未被停止。

源probe SHA及清理命令已核验。restore未完成，不修改历史11-2状态。下一步可在同样隔离方式下测试不同Docker/runtime版本，优先解决进入CRIU之前的内容提交冲突；不能通过删除系统daemon共享content store来修复本实验。

更正隔离边界：attempt2仅独立Docker data-root及命名空间，未显式指定containerd地址，不能证明独立content store；此前关于新content store的结论应以docker24-full的显式独立containerd实跑为依据。docker24与docker24-full保留不同隔离条件，不混为同组。
