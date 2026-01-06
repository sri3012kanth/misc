Below is a **clear, professional email** you can send to Microsoft support.
It explains the issue, the root cause you discovered, the corrective validation you performed, and asks the right technical question.

Hello Team,

We had raised a support case regarding a document count mismatch observed during vCore point-in-time restore (PITR) validation between the original and restored clusters.

Initially, the validation was performed on the **profile collection**, where document counts were compared using the `lastUpdatedTimestamp`. During further debugging, we identified that this timestamp is **application-managed** and gets updated whenever any changes are made to a profile document. As a result, even minor post-restore updates to profiles can lead to count mismatches when this field is used as the validation criterion.

To validate this hypothesis, we performed a deeper analysis and created additional scripts to compare document counts using the **audit collection** instead of the profile collection. Since audit documents are immutable and accurately reflect historical activity, the document counts between the original and restored clusters matched exactly, and the restore behavior appears to be working as expected.

Based on this, we wanted to confirm the following:

1. Is using an **application-populated field** like `lastUpdatedTimestamp` the only supported way to validate document counts for PITR?
2. Is there any **built-in or system-managed property** (for example, a server-side timestamp or internal metadata) that can be reliably used to validate document counts more accurately across original and restored clusters, without being affected by application-level updates?
3. Would Microsoft recommend validating PITR consistency using **immutable collections (such as audit data)** over mutable collections like profile data?

Please let us know the recommended and supported approach for PITR validation to avoid false mismatches caused by application-driven updates.

Thank you for your support and guidance.

Best regards,
Sri
