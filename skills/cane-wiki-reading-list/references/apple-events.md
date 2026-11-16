# Apple Events MCP: Reminders reference

This skill uses `mcp-server-apple-events` tools exposed by the active host:
`reminders_lists` and `reminders_tasks`. The host must have the MCP server configured
and the process running it must be permitted to access Reminders on macOS.

The field subset and tag behavior below were checked against `mcp-server-apple-events`
v1.5.0. If the connected version differs, trust the live MCP tool schema and verify
write behavior before relying on tag updates.

## Preflight

Before reading or writing reminders:

1. Confirm both tools are callable. If they are not, stop and tell the user to configure
   the Apple Events MCP server for the current host (Codex, OpenCode, or Claude Code).
   Do not assume one host's MCP configuration syntax applies to another.
2. Call `reminders_lists` with `action: read`. If macOS denies access, ask the user to
   grant Reminders access to the host process running the MCP server in
   **System Settings → Privacy & Security → Reminders**, then retry only after permission
   is granted.
3. A newly configured server may require a new conversation or host-session restart
   before its tools are available.

The original Claude Code registration pattern for this server is:

```bash
claude mcp add --scope project apple-events -- npx -y mcp-server-apple-events
```

Use the active host's own MCP setup mechanism for Codex and OpenCode; do not run this
Claude Code command in those hosts.

## Tool fields used by this skill

### `reminders_lists`

| Field | Use |
|---|---|
| `action` | `read` to list Reminders lists |

### `reminders_tasks`

| Field | Use |
|---|---|
| `action` | `read` to retrieve reminders; `update` only after a successful wiki import |
| `id` | Existing reminder ID, required for update |
| `filterList` | Restrict reads to the selected list |
| `showCompleted` | Set `true` to include completed reminders |
| `title` | Reminder title |
| `note` | Free-text notes; may also contain MCP-managed tag markers |
| `completed` | Read-only for this skill; never update it |
| `addTags` | Add `KB` after successful wiki ingest without replacing existing tags |

Read all reminders in the chosen list before filtering locally. A `KB` marker may occur
in the returned `tags` field or in `note` as `[#KB]` or `#KB`.

## Tag behavior and write safety

In the `mcp-server-apple-events` implementation this skill was based on, tag updates are
encoded as markers in the reminder's `note`, rather than native Apple Reminders tag chips.
An `addTags` update may therefore alter the displayed note. Explain this when relevant,
preserve the user's existing note, and never write tags before the wiki ingest succeeds.
Read back the reminder when supported to verify the marker.

Tool schemas can change across server versions. If the live tool schema differs from
these fields, follow the live schema and do not guess at unsupported arguments.
