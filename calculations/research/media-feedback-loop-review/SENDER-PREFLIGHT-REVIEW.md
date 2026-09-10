# Sender and application preflight independent review

This review executed `media-feedback-loop/check-sender.py` (18 checks and 14 historical full-math scenarios passed) and `check-application-validation.py` (31 checks passed). It then executed the separate `check-boundaries.py` here. It did not run a media network candidate or derive expectations from its output.

Two independent sender cases passed:

- Sending A:[0,100) and A:[200,300), then retransmitting [0,100), consumes connection stream credit300, while confirmed unique payload is200. The hole is not payload, but remains covered by highest-offset flow accounting. The repeated range adds no flow credit.
- A padded1200B packet containing960B DATAGRAM data consumes no STREAM credit. At PTO its1200B flight remains outstanding and its retransmittable frame list is empty. An explicit newPN empty-frame PING is used. The real ACK of that probe causes the earlier datagram to be declared lost; flight becomes0. Reusing the old datagram identity is rejected without state mutation. The payload transmission subtotal stays960B.

The recovery helper is intentionally a selector over already validated records; it does not itself schedule a probe or prove that the network will never accidentally requeue DATAGRAM data. That must be checked later in actual network traces. The public sender does already reject duplicate application datagram identity.

Independent malformed application cases are saved in `boundary-review.json`; each includes the full accepted-invalid input where applicable:

1. **Endpoint causality bypass**: a task with actual `endpoint='server'` and an extra `sender='client'` field can depend on a client-local task completion. Validation selects `record.get('sender', record.get('endpoint'))`, while task execution uses `endpoint`. Reject unexpected sender fields or choose consumer endpoint by actual message/task identity, and test this mismatch explicitly.
2. **Unknown playback message**: a TTS block can refer to `does-not-exist` while its overall completion dependencies stay valid. The observer block references must resolve to the intended endpoint and declared completion set; otherwise an input passes preflight with inconsistent quality/completion definitions.
3. **Cancellation target container**: a string in `on_delivery_cancel_tags` passes because the validator iterates characters and each character is a nonempty string. Require an actual list of tags; otherwise a single tag is silently transformed into unrelated character tags.
4. **Boolean schema version**: True compares equal to1 and is admitted. Require integer type as well as version value to avoid inconsistent schema typing.
5. A remote version-change endpoint was already rejected by the root's contemporaneous validator update when this independent script ran. The report records this as a passed rejection rather than an unresolved defect.

No candidate implementation was edited by this review. Re-run the local independent checker after repairs; its JSON records the exact observed hashes and current disposition. Do not replace a finding with an overall pass until the bad input is rejected at the same frozen hash used by integration.

## Repair recheck

The independent checker was actually rerun after the root fixes. All five invalid inputs are now rejected with ValueError, unchanged; both independent sender accounting cases still pass. The root preflight checker was also rerun and reports35 passing checks. The four originally accepted-invalid cases are retained in `boundary-review-before-fix.json`; the new report is `boundary-review-after-fix.json` (also the latest `boundary-review.json`).

Rechecked application validator SHA256: `d4ebb24bbfe734ebb696964f13c16f8ba18064ae306085ea25696adc452712a3`. Sender SHA256: `01b7de490da790111aa0cb1901bdc7597a0235d0a77a0d7202d47f828547afea`. This resolves the reported preflight findings at those hashes; it is not a full media-network or universal malformed-schema acceptance claim.
