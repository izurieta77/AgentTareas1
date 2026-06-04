# graphify

- **graphify** (`.claude/skills/graphify/SKILL.md`) — turns any input (code, docs, papers, images, videos) into a queryable knowledge graph. Trigger: `/graphify`

When the user types `/graphify`, invoke the Skill tool with `skill: "graphify"` before doing anything else.

The `graphify` CLI is provided by the `graphifyy` PyPI package. In ephemeral
environments it is (re)installed automatically by the SessionStart hook at
`.claude/hooks/install-graphify.sh`. To install manually: `uv tool install graphifyy`.
