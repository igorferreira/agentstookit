# Obsidian Vault — Direct Note Management

Use for filesystem-first Obsidian vault work: reading notes, listing notes, searching note files, creating notes, appending content, and adding wikilinks. This is for direct vault CRUD without the full llm-wiki construction workflow.

## Vault Path

Use the `OBSIDIAN_VAULT_PATH` environment variable (set in `${HERMES_HOME:-~/.hermes}/.env`). If unset, default to `~/Documents/Obsidian Vault`.

**File tools do not expand shell variables.** Resolve the vault path first and pass a concrete absolute path. Paths may contain spaces — prefer file tools over shell commands.

## Read a Note
```python
read_file("/absolute/path/to/vault/Note Name.md")
```

## List Notes
```python
search_files(pattern="*.md", target="files", path="/absolute/vault/path")
# List a subfolder:
search_files(pattern="*.md", target="files", path="/absolute/vault/path/subfolder")
```

## Search Notes
```python
# Search by content:
search_files(pattern="your search term", target="content", path="/vault", file_glob="*.md")
# Search by filename:
search_files(pattern="*meeting*", target="files", path="/vault")
```

## Create a Note
```python
write_file("/absolute/vault/path/New Note.md", content="---\ntitle: New Note\n---\n\n# New Note\n\nContent here.")
```

## Append to a Note
1. `read_file` the target note
2. Use `patch` for anchored append (stable context like a heading)
3. Use `write_file` when rewriting whole note is clearer
4. `terminal` for simple line-append when no stable anchor

## Targeted Edits
Use `patch` for focused changes with stable context.

## Wikilinks
Obsidian links notes with `[[Note Name]]` syntax. When creating or editing notes, use these to link related content.

## Notes
- Works naturally with the `llm-wiki` skill if `WIKI_PATH` and `OBSIDIAN_VAULT_PATH` point to the same directory
- For the Obsidian Sync / headless server approach, see the llm-wiki skill body (§ Obsidian Headless)
