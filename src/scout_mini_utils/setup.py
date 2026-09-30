from setuptools import find_packages, setup

package_name = 'scout_mini_utils'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='takuto',
    maintainer_email='takuto.ii29.mail@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'lidar_stamp_fix = scout_mini_utils.lidar_stamp_fix:main',
            'gt_odom_tf = scout_mini_utils.gt_odom_tf:main',
        ],
    },
)
