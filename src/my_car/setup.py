from setuptools import setup

package_name = 'my_car'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='your_name',
    maintainer_email='your_email@example.com',
    description='Python-based ROS 2 package for controlling my_car',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'teensy_interface = my_car.teensy_interface:main',
        ],
    },
)
