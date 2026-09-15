# 绕过私有content重复后的CRIU诊断

2026-09-15实际执行，Docker24.0.9和显式独立containerd，使用本目录data/root及/run/book1102-bypass系列路径。仅default案例运行到恢复，未执行unconfined后续案例；不可算两次完成。

首次恢复遇到already exists后，脚本从本次错误提取唯一sha256，先在私有containerd的book1102 namespace content ls中确认，再仅删除该digest，保留Docker本地checkpoint目录，重试同容器恢复。系统containerd未操作。此为诊断干预，不是未经修改Docker的成功实验，也不是生产修复方案。

重试进入CRIU，保存的restore-live.log第810行报告restorer PID3308074被SIGSEGV(signal11)终止，最后Restoring FAILED。shim log.json另报type NOTIFY失败。由此确认内容提交与后续CRIU恢复存在两个不同失败边界；未证明SIGSEGV根因。

docker start重试45秒超时，docker rm -f亦45秒超时，probe退出1，完整异常在probe-output.json；没有result.json。父进程正常终止dockerd与containerd，两者退出0。残留shim PID3308050由后续清理检查完整命令行、目标容器ID、私有socket且无子进程后SIGTERM，/proc确认gone，见shim-cleanup.json。不能声称docker rm成功；远端私有容器元数据／rootfs挂载可能仍留存，保留作诊断证据，不再运行任务。

相应v28.5.2来源位于../../content-diagnosis/client-v28.go，writeContent在Commit返回already exists时直接失败；这是代码观察，与本组运行版本v24应分开解释。下一步需固定CRIU/runtime组合并检查restorer崩溃，而非重复当前配置。11-2内存派生仍未完成。
