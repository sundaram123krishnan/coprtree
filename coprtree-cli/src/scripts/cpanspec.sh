#!/usr/bin/env bash
set -e
work=$(mktemp -d)
cd "$work"
cpanspec --packager coprtree -v @PACKAGE@
cp -- *.spec *.tar.* "$COPR_RESULTDIR"

# Refer to copr docs for more info: https://docs.copr.fedorainfracloud.org/custom_source_method.html#custom-source-method
