docker stop owlvey-archon
docker rm owlvey-archon
#
docker run --name=owlvey-archon `
    --mount type=bind,source="/Users/Gregory/owlvey/archon/template",target="/workspace/metadata"  `
    --mount type=bind,source="/Users/Gregory/owlvey/archon/template",target="/workspace/data"  `
    --mount type=bind,source="/Users/Gregory/owlvey/archon/system_docker.yaml",target=/workspace/config.yaml  `
    -e "OWLVEY_CONFIG=/workspace/config.yaml"`
    -e "OWLVEY_LOGGING=ERROR"`
    owlvey-archon:latest