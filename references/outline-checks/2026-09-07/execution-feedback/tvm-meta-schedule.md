<!-- 从 tvm-meta-schedule.html 迁移的资料快照；原始 HTML SHA-256: 8e3982f816cdcc481e6d9193b40d8c83dbf8bf19d6bce82f47fe84189679da93。 -->

- [ Repository](https://github.com/apache/tvm "Source repository")
- [ Show source](https://github.com/apache/tvm/blob/main/docs/deep_dive/tensor_ir/tutorials/meta_schedule.rst?plain=1 "Show source")
- [ Suggest edit](https://github.com/apache/tvm/edit/main/docs/deep_dive/tensor_ir/tutorials/meta_schedule.rst "Suggest edit")
- [ Open issue](https://github.com/apache/tvm/issues/new?title=Issue%20on%20page%20%2Fdeep_dive/tensor_ir/tutorials/meta_schedule.html&body=Your%20issue%20content%20here. "Open an issue")

- [ .rst](../../../_sources/deep_dive/tensor_ir/tutorials/meta_schedule.rst "Download source file")
-  .pdf

# MetaSchedule: Search-Based Auto-Tuning

## Contents

- [Architecture Overview](#architecture-overview)
- [Prepare a Model](#prepare-a-model)
- [User-Facing Entry Points](#user-facing-entry-points)
  - [Transform-Based API (Recommended)](#transform-based-api-recommended)
- [Inspecting Tunable Tasks](#inspecting-tunable-tasks)
- [Selective Operator Tuning](#selective-operator-tuning)
- [Database](#database)
  - [Resumption Semantics](#resumption-semantics)
  - [Database Implementations](#database-implementations)
- [Cross-Model Database Reuse](#cross-model-database-reuse)
  - [module_equality Options](#module-equality-options)
- [Key Parameters Reference](#key-parameters-reference)
- [Summary](#summary)

Note

You can click [here](#sphx-glr-download-deep-dive-tensor-ir-tutorials-meta-schedule-py) to run the Jupyter notebook locally.

<a id="metaschedule-search-based-auto-tuning"></a>

# MetaSchedule: Search-Based Auto-Tuning
MetaSchedule is TVM’s search-based auto-tuning framework, located in `python/tvm/s_tir/meta_schedule/`. It explores different TIR schedules (loop tiling, vectorization, thread binding, etc.) and measures them on real hardware to find the fastest implementation for each operator.

While **DLight** (see [DLight: Rule-Based GPU Scheduling](dlight_gpu_scheduling.html#dlight-gpu-scheduling)) provides rule-based scheduling with zero search time, MetaSchedule trades compilation time for better performance by searching over the space of possible schedules.

Table of Contents

- [Architecture Overview](#architecture-overview)

- [Prepare a Model](#prepare-a-model)

- [User-Facing Entry Points](#user-facing-entry-points)

- [Inspecting Tunable Tasks](#inspecting-tunable-tasks)

- [Selective Operator Tuning](#selective-operator-tuning)

- [Database](#database)

- [Cross-Model Database Reuse](#cross-model-database-reuse)

- [Key Parameters Reference](#key-parameters-reference)

- [Summary](#summary)

<a id="architecture-overview"></a>

## [Architecture Overview](#id1)
A MetaSchedule tuning session involves the following components:

- **ExtractedTask**: A unique TIR workload extracted from a Relax IRModule, with a `task_name` and `weight` (call frequency in the graph).

- **TuneContext**: Container holding all resources for a single tuning task (module, target, space generator, search strategy, etc.).

- **SpaceGenerator** (default: `PostOrderApply`): Generates the design space of possible schedules by applying `ScheduleRule` instances to each block.

- **SearchStrategy** (default: `EvolutionarySearch`): Explores the design space using an evolutionary algorithm guided by a cost model.

- **CostModel** (default: `XGBModel`): Predicts schedule performance using XGBoost, reducing the number of actual hardware measurements needed. Alternatives include `MLPModel` (neural network) and `RandomModel` (baseline).

- **Builder** / **Runner**: Compile and execute candidates on real hardware to obtain measured run times.

- **Database** (default: `JSONDatabase`): Persistently stores tuning records (schedule traces + measured run times) for later retrieval.

- **TaskScheduler** (default: `GradientBasedScheduler`): Allocates tuning budget across multiple tasks based on their weights and estimated improvement potential.

The tuning loop works as follows:

1.  The **TaskScheduler** picks a task to tune.

2.  The **SpaceGenerator** produces candidate schedules from the design space.

3.  The **SearchStrategy** selects candidates (guided by the **CostModel**), sends them to the **Builder** and **Runner** for measurement.

4.  Measured results are committed to the **Database** and used to update the **CostModel** for the next iteration.

5.  Repeat until the trial budget is exhausted.

<a id="prepare-a-model"></a>

## [Prepare a Model](#id2)
We reuse a simple model to demonstrate MetaSchedule APIs.

    import os
    import tempfile

    import tvm
    from tvm import relax
    from tvm.relax.frontend import nn


    class DemoModel(nn.Module):
        def __init__(self):
            super().__init__()
            self.fc1 = nn.Linear(784, 256)
            self.relu = nn.ReLU()
            self.fc2 = nn.Linear(256, 10, bias=False)

        def forward(self, x):
            x = self.fc1(x)
            x = self.relu(x)
            x = self.fc2(x)
            return x


    input_shape = (1, 784)
    mod, params = DemoModel().export_tvm({"forward": {"x": nn.spec.Tensor(input_shape, "float32")}})

    device = tvm.cuda(0)
    target = tvm.target.Target.from_device(device)

<a id="user-facing-entry-points"></a>

## [User-Facing Entry Points](#id3)
MetaSchedule provides several levels of API, from high-level transforms to low-level tuning functions.

<a id="transform-based-api-recommended"></a>

### Transform-Based API (Recommended)
These are Relax passes that can be composed into a `Sequential` pipeline:

- **MetaScheduleTuneIRMod**: Tunes an entire IRModule. Supports `op_names` for selective operator tuning.

- **MetaScheduleTuneTIR**: Tunes all TIR functions individually (no `op_names` filtering).

- **MetaScheduleApplyDatabase**: Applies the best schedules from the tuning database. Only replaces functions that have records; the rest are left unchanged.

Here is a typical tune-and-apply pipeline:

Note

To save CI time and avoid flakiness, we skip the tuning process in CI.

    if os.getenv("CI", "") != "true":
        with target, tempfile.TemporaryDirectory() as tmp_dir:
            tuned_mod = tvm.ir.transform.Sequential(
                [
                    relax.get_pipeline("zero"),
                    relax.transform.MetaScheduleTuneTIR(
                        work_dir=tmp_dir,
                        max_trials_global=300,
                    ),
                    relax.transform.MetaScheduleApplyDatabase(work_dir=tmp_dir),
                ]
            )(mod)

        tuned_mod.show()

<a id="inspecting-tunable-tasks"></a>

## [Inspecting Tunable Tasks](#id4)
Before tuning, use `extract_tasks` to see what MetaSchedule will tune:

    from tvm.s_tir.meta_schedule.relax_integration import extract_tasks

    with target:
        legalized_mod = relax.get_pipeline("zero")(mod)

    tasks = extract_tasks(legalized_mod, target)
    for i, task in enumerate(tasks):
        print(f"Task {i}: {task.task_name}  (weight={task.weight})")

    Task 0: matmul1  (weight=1)
    Task 1: transpose1  (weight=1)
    Task 2: fused_matmul_add_relu  (weight=1)
    Task 3: transpose  (weight=1)

Each `ExtractedTask` has:

- `task_name`: Derived from the PrimFunc name (e.g., `"fused_matmul_add_relu"`).

- `weight`: How many `call_tir` sites invoke this workload. The task scheduler uses weights to allocate more budget to frequently-called operators.

- `dispatched`: List of candidate TIR modules for this workload.

<a id="selective-operator-tuning"></a>

## [Selective Operator Tuning](#id5)
`MetaScheduleTuneIRMod` accepts an `op_names` parameter to tune only operators whose task name contains any of the given strings:

    with target:
        mod = tvm.ir.transform.Sequential([
            relax.transform.MetaScheduleTuneIRMod(
                params={},
                work_dir="./tuning_logs",
                max_trials_global=300,
                op_names=["matmul"],  # Only tune matmul-related operators
            ),
            relax.transform.MetaScheduleApplyDatabase(work_dir="./tuning_logs"),
        ])(mod)

Operators without tuning records are left unscheduled – you can apply DLight or other rule-based schedules to cover them afterward.

Note

`MetaScheduleTuneTIR` does not support `op_names` filtering. Use `MetaScheduleTuneIRMod` when you need selective tuning.

<a id="database"></a>

## [Database](#id6)
When using a fixed `work_dir`, tuning results are persisted in two newline-delimited JSON files:

- `database_workload.json`: One line per unique workload (structural hash + serialized IRModule).

- `database_tuning_record.json`: One line per tuning record (workload index + schedule trace + measured run times).

Records are appended incrementally as tuning progresses.

<a id="resumption-semantics"></a>

### Resumption Semantics
When you re-run tuning with the same `work_dir`, existing records are loaded and used as warm-start seeds for the evolutionary search. The tuner does **not** skip already-seen workloads entirely – it starts from a better initial population, so re-runs are faster than starting from scratch but still consume trials.

Once tuning is done, subsequent compilations only need `MetaScheduleApplyDatabase`:

    with target:
        mod = relax.transform.MetaScheduleApplyDatabase(
            work_dir="./tuning_logs"
        )(mod)

<a id="database-implementations"></a>

### Database Implementations
MetaSchedule ships several database backends:

- **JSONDatabase**: Persistent file-based storage (default). Created automatically when you pass `work_dir`.

- **MemoryDatabase**: In-memory, non-persistent. Useful for testing.

- **UnionDatabase**: Queries all sub-databases and returns the globally best record.

- **OrderedUnionDatabase**: Queries sub-databases in order; returns from the first one that has a match.

- **ScheduleFnDatabase**: Wraps a user-provided scheduling function.

<a id="cross-model-database-reuse"></a>

## [Cross-Model Database Reuse](#id7)
MetaSchedule identifies workloads by their structural hash. If two models contain operators with the same shape, dtype, and computation, they share the same hash and can reuse tuning records.

<a id="module-equality-options"></a>

### module_equality Options
- `"structural"` (default): Exact structural match. Safe but strict.

- `"anchor-block"`: Match based on the dominant compute block, ignoring surrounding context. More permissive – enables sharing across fused operators that have the same core computation but different fusion boundaries.

`OrderedUnionDatabase` enables a layered lookup strategy: check a local database first, then fall back to a shared team database:

    from tvm.s_tir.meta_schedule.database import JSONDatabase, OrderedUnionDatabase

    local_db = JSONDatabase(work_dir="./my_tuning_logs")
    shared_db = JSONDatabase(work_dir="/shared/tuning_db")
    combined_db = OrderedUnionDatabase(local_db, shared_db)

    with target, combined_db:
        mod = relax.transform.MetaScheduleApplyDatabase()(mod)

<a id="key-parameters-reference"></a>

## [Key Parameters Reference](#id8)
| Parameter | Description |
|----|----|
| `max_trials_global` | Total trial budget shared across all tasks. Set proportional to the number of tasks (e.g., 200-500 trials per task for good results). |
| `max_trials_per_task` | Per-task trial cap. Defaults to `max_trials_global` if not set. |
| `op_names` | List of strings to filter tasks by name (substring match). `MetaScheduleTuneIRMod` only. |
| `work_dir` | Directory for database files and logs. Use a fixed path to enable persistence and resumption. |
| `cost_model` | `"xgb"` (XGBoost, default), `"mlp"` (neural network), or `"random"` (baseline). Only available via `tune_relax`. |
| `runner` | `"local"` (default) or an `RPCRunner` instance for remote devices. Only available via `tune_relax`. |
| `module_equality` | `"structural"` (default) or `"anchor-block"` for more permissive cross-model matching. Only available via `tune_relax`. |

<a id="summary"></a>

## [Summary](#id9)
- **MetaSchedule** finds high-quality TIR schedules by searching over the design space and measuring on real hardware.

- Use `MetaScheduleTuneTIR` for full-module tuning, or `MetaScheduleTuneIRMod` with `op_names` for selective tuning.

- Tuning records persist in `work_dir` and can be reused across runs and models with the same operator shapes.

- Combine with DLight: use DLight for fast baseline coverage, then MetaSchedule for hot-spot tuning (see [DLight: Rule-Based GPU Scheduling](dlight_gpu_scheduling.html#dlight-gpu-scheduling)).

[`Download`` ``Jupyter`` ``notebook:`` ``meta_schedule.ipynb`](../../../_downloads/d9ca2296a776aca29d1e43826b298e0d/meta_schedule.ipynb)

[`Download`` ``Python`` ``source`` ``code:`` ``meta_schedule.py`](../../../_downloads/607a699cdbbe2ddb8febc2c10e687b63/meta_schedule.py)

[`Download`` ``zipped:`` ``meta_schedule.zip`](../../../_downloads/249a4acaa182fd00b9c381b53025777d/meta_schedule.zip)

[](dlight_gpu_scheduling.html "previous page")

previous

DLight: Rule-Based GPU Scheduling

[](../../relax/index.html "next page")

next

Relax

Contents

- [Architecture Overview](#architecture-overview)
- [Prepare a Model](#prepare-a-model)
- [User-Facing Entry Points](#user-facing-entry-points)
  - [Transform-Based API (Recommended)](#transform-based-api-recommended)
- [Inspecting Tunable Tasks](#inspecting-tunable-tasks)
- [Selective Operator Tuning](#selective-operator-tuning)
- [Database](#database)
  - [Resumption Semantics](#resumption-semantics)
  - [Database Implementations](#database-implementations)
- [Cross-Model Database Reuse](#cross-model-database-reuse)
  - [module_equality Options](#module-equality-options)
- [Key Parameters Reference](#key-parameters-reference)
- [Summary](#summary)

By Apache Software Foundation

© Copyright 2020 - 2026, Apache Software Foundation.  

ASF

- [Apache Homepage](https://apache.org/)
- [License](https://www.apache.org/licenses/)
- [Sponsorship](https://www.apache.org/foundation/sponsorship.html)
- [Security](https://tvm.apache.org/docs/reference/security.html)
- [Thanks](https://www.apache.org/foundation/thanks.html)
- [Events](https://www.apache.org/events/current-event)

Copyright © 2026 The Apache Software Foundation. Apache TVM, Apache, the Apache feather, and the Apache TVM project logo are either trademarks or registered trademarks of the Apache Software Foundation.
