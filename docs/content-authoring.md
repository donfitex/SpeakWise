# Content authoring

Use `/admin/` with a staff account and explicit model permissions; never share a superuser account. Content authors need add/change lesson-version and activity permissions. Reviewers need `curriculum.publish_content` plus change/view review permission. Production operators should assign least-privilege groups.

Create course/unit/lesson metadata, then a draft lesson version, skills, rubric, and ordered activities. Every activity requires a reference, model, hint, and supported type. Preview the draft and its activities in the admin change forms. Put submission notes in the version's review notes, select “Submit drafts with review notes”, and ask a different reviewer to inspect content, accessibility, answer keys, and pronunciation variety before approving. Submitted/published activities cannot be changed, even through stale instances.

To update published content, use “Clone selected versions as new drafts”. Approval archives the previous published version; historical sessions retain their original content/rubric. Archive removes a version from new starts. Audit records retain requester, reviewer, decision, and notes. Feedback reports are available to authorized staff in admin.

Sample content is synthetic and not a completed educational review. A working review workflow does not establish that a qualified educator reviewed the content. Do not publish uncalibrated speech scoring as a proficiency measure.
