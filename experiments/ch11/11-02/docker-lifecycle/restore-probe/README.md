# 最小Docker内存恢复诊断

2026-09-15在rtx-pro实际执行，Docker28.5.2、CRIU3.16.1、kernel6.8.0-138。不修改daemon，不使用GPU；只创建本实验带标签容器，单容器1CPU/128MiB、host网络，无应用socket。Python仅输出内存生成的随机nonce并sleep。

原始run.py两条件均成功捕获，default恢复进入CRIU后失败，unconfined条件在containerd上传检查点时遇到内容摘要already exists。日志观察线程首次因瞬时criu-root目录消失报错，因此该组日志捕获不完整，保留原件。

run_v2.py增加启动后等待并核验32字符nonce；观察器跳过criu-root/rootfs，容忍文件消失。第二组default在containerd内容上传失败，seccomp与AppArmor均unconfined条件进入CRIU但仍报RESTORE失败。四次捕获成功、零次恢复成功。两个安全机制一同放开属于诊断控制，不据此分别判断某一个机制的影响；至少说明放开二者没有修复这次最小进程恢复。

results与results-v2记录所有命令、返回码、完整容器ID、image ID、源码SHA、单调计时及捕获到的日志。运行时目录没有捕获到详细CRIU restore日志，不能推断CRIU内部根因。first run错误栈见会话执行记录，结果不能当成日志捕获成功。第二组程序exit0仅表示诊断已记录，不表示restore成功。

每次仅删除本次创建的容器；四个docker rm均返回0。运行后按book.experiment=restore-probe标签查询无残留容器。没有删除共享containerd内容来绕过冲突。checkpoint成功不能替代恢复后的内存、独立派生和首工具验收，原11-2内存派生缺口仍未完成。

下一步应在独立data-root/socket/runtime的Docker环境中获得详细恢复诊断或验证兼容组合，避免更改承载其他服务的系统daemon。当前证据已排除“必须有本实验控制socket才会触发失败”的解释。
