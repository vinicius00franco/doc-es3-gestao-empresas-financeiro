#!/usr/bin/env bash
set -euo pipefail

# Render PlantUML diagrams to PNG using Docker (fixed workspace path as requested)
docker run --rm \
  -v /home/vinicius/Downloads/estudo/es3:/data \
  plantuml/plantuml:latest \
  -tpng \
  docs/geral/data-flow-diagram.puml \
  docs/geral/entity-relationship-diagram.puml \
  docs/geral/idef0-level0.puml \
  docs/geral/idef0-level1.puml \
  docs/geral/use-case-diagram.puml
