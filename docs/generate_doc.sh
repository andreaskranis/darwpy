#!/bin/bash
##############################################
# Generates the doc, including the auto-API
#
# USAGE
#	./generate_doc.sh
#
# NOTE
#	Assumes that user has run sphinx-quickstart
#   
##############################################

sphinx-apidoc -f -o source ../src/darwpy
make html

