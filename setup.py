from setuptools import setup

setup(
    name='pygame_teleop',
    version='1.1',
    description='Tools for simple teleoperation examples/demos/experiments in PyGame.',
    url='https://github.com/cmower/pygame_teleop',
    author='Christopher E. Mower',
    author_email='chris.mower@ed.ac.uk',
    license='BSD 2-Clause License',
    packages=['pygame_teleop'],
    install_requires=[
        'numpy',
        'pygame',
    ],
    zip_safe=False
)
