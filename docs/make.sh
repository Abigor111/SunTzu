#!/bin/bash

# Command file for Sphinx documentation

# Set the current directory to the directory of the script
cd "$(dirname "$0")"

# Check if SPHINXBUILD variable is set, otherwise set it to the default value
if [ -z "$SPHINXBUILD" ]; then
    SPHINXBUILD=sphinx-build
fi

SOURCEDIR=.
BUILDDIR=_build

if [ -z "$1" ]; then
    echo "Usage: $0 <target> [options]"
    exit 1
fi

"$SPHINXBUILD" >/dev/null 2>&1
if [ $? -eq 127 ]; then
    echo ""
    echo "The 'sphinx-build' command was not found. Make sure you have Sphinx"
    echo "installed, then set the SPHINXBUILD environment variable to point"
    echo "to the full path of the 'sphinx-build' executable. Alternatively you"
    echo "may add the Sphinx directory to PATH."
    echo ""
    echo "If you don't have Sphinx installed, grab it from"
    echo "https://www.sphinx-doc.org/"
    exit 1
fi

"$SPHINXBUILD" -M "$1" "$SOURCEDIR" "$BUILDDIR" "${@:2}"

