"""
Release helper tasks
"""
from __future__ import print_function

from invoke import task, Failure


@task
def update_changelog(ctx, new_version):
    """
    Quick task to generate the new CHANGELOG using reno when releasing a minor
    version.
    """
    new_version_int = map(int, new_version.split("."))

    if len(new_version_int) != 3:
        print("Error: invalid version: {}".format(new_version_int))
        raise Exit(1)

    # let's check that the tag for the new version is present (needed by reno)
    try:
        ctx.run("git tag --list | grep {}".format(new_version))
    except Failure as e:
        print("Missing '{}' git tag: mandatory to use 'reno'".format(new_version))
        raise

    # removing releasenotes from bugfix on the old minor
    previous_minor = "%s.%s" % (new_version_int[0], new_version_int[1] - 1)
    ctx.run("git rm `git log {}.0...{}.x --name-only \
            | grep releasenotes/notes/`".format(previous_minor, previous_minor))

    # generate the new changelog
    ctx.run("reno report \
            --ignore-cache \
            --earliest-version {}.0 \
            --version {} \
            --no-show-source > /tmp/new_changelog.rst".format(previous_minor, new_version))

    # reseting git
    ctx.run("git reset --hard HEAD")

    # merging to CHANGELOG.rst
    ctx.run("cat CHANGELOG.rst >> /tmp/new_changelog.rst && mv /tmp/new_changelog.rst CHANGELOG.rst")

    # commit new CHANGELOG
    ctx.run("git add CHANGELOG.rst \
            && git commit -m \"Update CHANGELOG for {}\"".format(new_version))
