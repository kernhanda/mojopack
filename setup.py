from setuptools import setup, find_packages

setup(
    name='mojopack',
    version='0.1',
    author='Kern Handa',
    author_email='kern.handa@gmail.com',
    description='mojopack is a tool for managing packages for the Mojo programming language.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/kernhanda/mojopack',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.8',
    install_requires=[
        'requests>=2.26.0',
        'tqdm>=4.62.0',
    ],
    setup_requires=['setuptools_scm'],
    use_scm_version=True,
)
