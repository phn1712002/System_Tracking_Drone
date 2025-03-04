# Start docker
ENV_NAME="$(basename $PWD)"
docker run -it \
        -p 1712:80 \
        -p 9090:9090 \
        -p 8765:8765 \
        -p 11311:11311 \
        -v=.:/root/$ENV_NAME \
        --device=/dev \
        --privileged \
        --name $ENV_NAME \
	ros_full:noetic_tracking_drone_ws
