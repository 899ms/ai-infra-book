# Short Chat remote prefetch sensitivity

Repeat the same four-turn Chat producer and fresh consumer replay in a new empty Mac store. All settings and inputs match cross-mac-traces-001 except backend extra config prefetch_threshold=16 rather than installed default256. This tests whether admitting short cache prefixes triggers real remote reads and its measured cost. Preserve one-token output limit, native-page publication barrier, immutable collision ledger, separate clock analysis and source hashes. Two engines, eight requests. No stable p95 or task-quality claim.
