import logging
import os
import posixpath
import types

from material.plugins.blog.plugin import BlogPlugin
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import PrefixedLogger
from mkdocs.structure.files import InclusionLevel


def on_config(config: MkDocsConfig):
    blog_plugins = [(name, p) for name, p in config.plugins.items() if isinstance(p, BlogPlugin)]

    for blog_name, blog in blog_plugins:
        for i, event in enumerate(config.plugins.events['files']):
            if hasattr(event, "__self__"):
                if event.__self__ is blog:
                    config.plugins.events['files'][i] = types.MethodType(patch_on_files, blog)
                    print(f'sort_posts_latest: Patching {blog_name}')


def patch_on_files(self: BlogPlugin, files, *, config):
    print(f'sort_posts_latest Running patch_on_files {self}')
    if not self.config.enabled:
        return

    # Resolve path to entrypoint and site directory
    root = posixpath.normpath(self.config.blog_dir)
    site = config.site_dir

    # Compute and normalize path to posts directory
    path = self.config.post_dir.format(blog=root)
    path = posixpath.normpath(path)

    # Adjust destination paths for media files
    for file in files.media_files():
        if not file.src_uri.startswith(path):
            continue

        # We need to adjust destination paths for assets to remove the
        # purely functional posts directory prefix when building
        file.dest_uri = file.dest_uri.replace(path, root)
        file.abs_dest_path = os.path.join(site, file.dest_path)
        file.url = file.url.replace(path, root)

    # Resolve entrypoint and posts sorted by descending date - if the posts
    # directory or entrypoint do not exist, they are automatically created
    self.blog = self._resolve(files, config)
    self.blog.posts = sorted(
        self._resolve_posts(files, config),
        key=lambda post: post.config.date.created,
        # reverse=True # @CHANGE: Disable sorting in reverse order
    )

    # Generate views for archive
    if self.config.archive:
        self.blog.views.extend(
            self._generate_archive(config, files)
        )

    # Generate views for categories
    if self.config.categories:
        self.blog.views.extend(sorted(
            self._generate_categories(config, files),
            key=lambda view: view.name,
            reverse=False
        ))

    # Generate pages for views
    if self.config.pagination:
        for view in self._resolve_views(self.blog):
            for page in self._generate_pages(view, config, files):
                view.pages.append(page)

    # Ensure that entrypoint is always included in navigation
    self.blog.file.inclusion = InclusionLevel.INCLUDED


HOOK_NAME: str = "sort_posts_latest"
"""Name of this hook. Used in logging."""

LOG: PrefixedLogger = PrefixedLogger(HOOK_NAME, logging.getLogger(f"mkdocs.hooks.{HOOK_NAME}"))
"""Logger instance for this hook."""
