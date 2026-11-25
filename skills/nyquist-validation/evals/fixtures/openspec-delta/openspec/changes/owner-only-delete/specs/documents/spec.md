## MODIFIED Requirements

### Requirement: Delete document
The system SHALL allow only owners to delete a document.

#### Scenario: Owner deletes
- WHEN an owner requests deletion
- THEN deletion is allowed

#### Scenario: Member denied
- WHEN a member requests deletion
- THEN deletion is denied

## RENAMED Requirements
- FROM: `### Requirement: Read document`
- TO: `### Requirement: View document`
