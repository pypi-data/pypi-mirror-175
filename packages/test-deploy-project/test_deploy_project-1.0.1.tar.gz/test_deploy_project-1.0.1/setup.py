from setuptools import setup, find_packages


setup(
    name='test_deploy_project',
    version='1.0.1',
    license='MIT',
    author="Mark",
    author_email='email@example.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/Markelii/deploy-project',
    keywords='example project',
    install_requires=[
      ],

)