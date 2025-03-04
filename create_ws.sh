## Install packages
sudo apt-get install ros-$ROS_DISTRO-rosserial-arduino -y
sudo apt-get install ros-$ROS_DISTRO-rosserial -y
sudo apt-get install ros-$ROS_DISTRO-rosbridge-server -y
sudo apt install ros-$ROS_DISTRO-foxglove-bridge -y

# Build ROS
rosdep update
catkin_make
catkin_make install

# Add bashrc
#PATH_BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

#echo "export TRACKING_DRONE_WS=$PATH_BASE" >> ~/.bashrc
#echo "source \$TRACKING_DRONE_WS/devel/setup.sh" >> ~/.bashrc

## Install pip env
python3 ./install_packages.py
