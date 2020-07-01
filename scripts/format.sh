set -x

# Sort imports one per line, so autoflake can remove unused imports
isort --recursive  --force-single-line-imports --force-alphabetical-sort-within-sections --apply brl

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place brl --exclude=__init__.py
black brl --line-length 88
isort --recursive --apply brl
