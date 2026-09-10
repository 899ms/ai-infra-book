# 单场景完整结果 runner

`run-book.py` 一次只执行一个封存输入，避免同时持有多个大结果。输入锁 `run-book-inputs.lock.json` 固定四格、单图基线、计量和规范化来源锁；运行前后都校验。候选网络/application/validator/sender/runner、共享公共sender/controller源码及实际官方来源均记录前后SHA。执行期间输入或源码漂移使运行失败，不能生成成功验收结论。

```sh
# 已实际执行的小 pilot；不是原书工作量
python calculations/research/media-feedback-loop/run-book.py --case image-baseline --pilot

# 以下仅示例，本轮未执行；等待根代理完成小例验收和运行授权
python calculations/research/media-feedback-loop/run-book.py --case mixed-fifo-immediate
```

可选case为四个mixed-{fifo,priority}-{immediate,aggregate}和image-baseline。`--pilot`只允许image-baseline：保留1400业务块、原依赖、0.3s模型和网络参数，将每块25000B缩为250B，并重算应用offset、分片元数据和每流绝对额度。有效上传300KB、响应50KB，总350KB；不能称30MB/5MB原书工作量，也不以此证明多片业务块的完整大例性能。

每次输出到 `runs/`：有效输入、完整 `*-result.json`、`*-manifest.json`、小 `*-summary.json`。manifest包含输入锁、有效输入SHA、完整结果SHA/字节数、前后源码SHA及耗时；摘要只是索引，不替代完整trace。未完成结果使用partial文件；失败manifest明确FAILED或REJECTED，不冒充验收。成功状态也明确 `COMPLETE_STABLE_IDENTITY_NOT_INDEPENDENT_ACCEPTANCE`。

实际最终pilot耗时1.083076s，1400数据包+1400ACK，350000B唯一业务、1848000B线上；完整响应1.917206547s。`runner-pilot-check.json`另核完整结果SHA与这些小整数账。候选作者随后会继续修正priority排序等内容，此pilot仅证明记录的当时源码与runner路径可工作；后续正式运行必须重新取得并核当时源码身份。本轮没有运行任何完整大例。
