# pylint: skip-file
from setuptools import setup
import os
from glob import glob
package_name = 'push_mapping'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
        (os.path.join('share', package_name, 'config'), glob(os.path.join('config', '*.yaml'))),
        (os.path.join('share', package_name, 'rviz'), glob(os.path.join('rviz', '*.rviz'))),
        (os.path.join('share', package_name, 'description'), glob(os.path.join('description', '*.xacro'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='team13',
    maintainer_email='team13@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        'bringup = push_mapping.JetsonBringup:main',
        ],
    },
)
