REQ-DOC-1: Only the document owner may delete a document; other authenticated users receive a denial and the document remains intact.
REQ-DOC-2: Deleting a document and its attachments is atomic: partial storage failure must leave the pre-delete state recoverable.
REQ-DOC-3: Retrying the same authorized deletion must not affect any other document or attachments.
This is a design-only repository. No implementation or test infrastructure exists.
