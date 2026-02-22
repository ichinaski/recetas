#!/bin/bash
set -e

cd "$(dirname "$0")/../public"
python3 -m http.server 1313
