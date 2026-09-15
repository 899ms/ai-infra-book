# CRIU4.2.1最小进程恢复成功

rtx-pro实际执行两条件，default与seccomp/AppArmor unconfined均checkpoint create返回0、restore返回0，随后Docker inspect Running=true。恢复后日志与捕获前完全相同，未再次打印启动nonce。两个容器已rm成功，独立dockerd和containerd均退出0。本测试没有GPU。

CRIU固定v4.2.1 commit9539417f3e3cfa4eb84c319cd71f4d52f1f08645，从官方仓库在tools/criu-4.2.1以make -j8 criu编译，没有make install。toolchain.txt保存实际版本与二进制SHA。Docker仍24.0.9，独立containerd、data-root、运行时路径；仅该进程树PATH优先新CRIU，系统CRIU3.16.1未替换。

仍存在首次上传content already exists时重试的诊断逻辑：列出私有store，若本次错误digest仍存在才删除它，再从本地checkpoint重试；若已被失败路径清除则直接重试。commands.json保留具体分支，不称为原Docker无需干预的一次成功。前一criu421组因digest已被清除而触发过严assert，结果保留，不能并入本组成功率。

这是最小sleep进程的同容器恢复，不是原11-2完整状态合同。Running及无重复nonce输出不足以验证任意内存值、两派生实例独立性和活动连接；下一步使用worker_unix状态探针，逐一验证内存nonce/counter、文件marker、外部事件账本、重新连接及两实例修改互不影响。历史11-2尚未关闭。

同机旧CRIU3.16.1诊断记录restorer SIGSEGV，而本组合成功，支持新版CRIU兼容性有所改善；尚未定位或二分到具体修复提交，因此不指定rseq/vDSO为已证实根因。
