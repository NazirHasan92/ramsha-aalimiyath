"""MkDocs hooks for Ramsha's eMahad notes site.

Two responsibilities:
1. Strip MarkText-specific <style> blocks at the top of each .md file (so
   they don't override Material's theme).
2. For each chapter's deep-notes.md, prepend a navigation banner linking
   to the sibling deliverables (teacher-notes.html, student-handout.html,
   slides.html) — only including files that actually exist on disk (so
   in-progress chapters that only have deep-notes don't show 404 links).
"""
import re
from pathlib import Path

_STYLE_BLOCK = re.compile(
    r'^\s*<style\b[^>]*>.*?</style>\s*',
    flags=re.DOTALL | re.IGNORECASE,
)

_DELIVERABLES = [
    ('Teacher view', 'teacher-notes.html'),
    ('Student handout', 'student-handout.html'),
    ('Slides', 'slides.html'),
]


def on_page_markdown(markdown, *, page, config, files):
    # Strip first <style> block if present at top of file
    markdown = _STYLE_BLOCK.sub('', markdown, count=1)

    src = page.file.src_path.replace('\\', '/')
    if not src.endswith('/deep-notes.md'):
        return markdown

    chapter_dir = Path(page.file.abs_src_path).parent
    available = [
        f'[{label}]({filename})'
        for label, filename in _DELIVERABLES
        if (chapter_dir / filename).exists()
    ]
    if not available:
        return markdown

    banner_links = ['**📖 Deep notes** (this page)'] + available
    banner = '!!! info "Chapter deliverables"\n    ' + ' · '.join(banner_links) + '\n\n'
    return banner + markdown
