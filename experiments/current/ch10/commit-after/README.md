# 10-6 提交后终止进程

rtx-pro上使用原10-7的CPU PyTorch DCP训练程序，保留1024×1024模型、Dropout、AdamW、两份RNG及第3／23步保存边界。唯一实验性变更是把第二份保存的故障屏障从metadata提交前移到提交完成后。父进程确认屏障及后续20步更新均完成，再SIGKILL该子进程。输出目录独立，不覆盖旧实验。

新故障路径退出−9，第23步checkpoint具有metadata并实际DCP加载成功，11项状态哈希与保存前记录完全相同；最新训练到第43步，恢复到23后要重做20步。旧提交前路径只有第3步可用，到43须重做40步。旧路径实际追赶更新的证据保存在原catch-up目录；本次验证提交后恢复状态，不声称再次完成20步追赶。

API返回并不等于提交完成。新记录含api、staging、数据写完、metadata提交、后续训练与SIGKILL时间；屏障等待是故障注入手段，不用于估计磁盘吞吐。两次实验均为同机CPU小模型进程终止，非断电、多rank、磁盘故障或远端存储证明；不同生命周期不拼接monotonic时间，也不比较单次计时性能。

运行：Linux专用环境中 `CUDA_VISIBLE_DEVICES= OMP_NUM_THREADS=1 /usr/bin/python3 run.py --output new-output`。已有目录会拒绝覆盖。`python3 verify.py`离线检查提交顺序、终止条件和恢复结果。formal-001保留真实checkpoint payload及metadata、事件、日志和结果。
