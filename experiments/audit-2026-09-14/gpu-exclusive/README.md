# Exclusive GPU preparation

The author explicitly authorized stopping all existing GPU sessions. Stopped the six GPU process groups and their launch wrappers: speaker identification, ASR/Whisper, word timings, Fish speech and the Qwen VL vLLM server. Full prior command lines are retained privately on rtx-pro at `audit-2026-09-14/gpu-exclusive/prior-processes.json` (mode 0600).

After the last GPU context exited, the old loaded 595.71.05 kernel module could not reinitialize because its firmware was no longer installed. The installed kernel module, firmware and user libraries were all 595.91.07. With no open GPU device handles, unloaded nvidia_drm/nvidia_uvm/nvidia_modeset/nvidia and loaded the installed nvidia and nvidia_uvm modules. No reboot or package change. The default nvidia-smi now works; **do not inject the previous 595.71.05 NVML workaround into new runs**.

Verified RTX PRO 6000 Blackwell, driver 595.91.07, 97,250 MiB free, no GPU applications; CUDA tensor sum returned 1024.0. Five abandoned LMCache shared-memory pools totaling 20 GiB had no live owner PID and no process mappings or open file descriptors (root /proc scan). Removed only those five named pools and retained a cleanup record on the server. CPU synthesis jobs were left running.
