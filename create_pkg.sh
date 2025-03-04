clear
# Create package
echo "Name of package?: "
read PKG_NAME
cd src
while true; do
read -p "C++ or Python, create package with C++ (y/n) ?: " yn
case $yn in 
	[yY] ) echo "Create package with C++";
		catkin_create_pkg $PKG_NAME roscpp
		break;;
	[nN] ) echo "Create package with Python";
		catkin_create_pkg $PKG_NAME rospy
		break;;
	* ) echo "Invalid response";;
esac
done
cd ..
