docker stop owlvey-archon
docker rm owlvey-archon
#
docker run --name=owlvey-archon `
    --mount type=bind,source="/workspace/gregory/owlvey/metadata",target="/workspace/metadata"  `
    --mount type=bind,source="/workspace/gregory/owlvey/data",target="/workspace/data"  `
    --mount type=bind,source="/workspace/gregory/owlvey/archon/system_docker.yaml",target=/workspace/config.yaml  `
    -e "OWLVEY_CONFIG=/workspace/config.yaml"`
    -e "OWLVEY_LOGGING=WARNING"`zzz
    owlvey-archon:latest