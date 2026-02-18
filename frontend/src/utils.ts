/**
 * Remove YAML frontmatter (`--- ... ---`) from the start of a Markdown string.
 * @param content - Raw Markdown that may begin with a YAML front matter block.
 * @returns The content with frontmatter stripped and leading whitespace trimmed.
 */
export function stripFrontmatter(content: string): string {
  return content.replace(/^---\n[\s\S]*?\n---\n/, "").trimStart();
}

/**
 * Convert a doc filename to a human-readable title.
 * @param filename - e.g. `"getting-started.md"`
 * @returns Title-cased string, e.g. `"Getting Started"`.
 */
export function formatDocTitle(filename: string): string {
  return filename.replace(/\.md$/, "").replace(/[-_]/g, " ").replace(/\b\w/g, c => c.toUpperCase());
}
