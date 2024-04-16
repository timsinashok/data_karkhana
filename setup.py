from setuptools import setup, find_packages

setup(
    name='datakarkhana',  # Replace 'your_package' with the name of your package
    version='0.1.0',
    description='A peer-to-peer file sharing system',
    long_description='Datakarkhana is a peer-to-peer file sharing system which works on a hybrid peer-to-peer and client-server model. ',
    long_description_content_type='text/markdown',
    url='https://github.com/timsinashok/data_karkhana',  # Replace with the URL of your package repository
    author='Yaghyesh Ghimire, Manoj Dhakal, Mahmud Faisal , Ashok Timsina',  # List all authors separated by commas
    author_email='md5121@nyu.edu, yg2810@nyu.edu, fm2357@nyu.edu, ashoktimsina147181@gmail.com',  # List all author emails separated by commas
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='peer peer-to-peer file sharing alice bob',  # Replace with keywords relevant to your package
    packages=find_packages(),
    python_requires='>=3.6, <4',
    install_requires=[],  # Add any dependencies your package requires
    entry_points = {
        'console_scripts': ['datakarkhana=data_karkhana.main:main'],
    },
    project_urls={
        'Bug Reports': 'https://github.com/timsinashok/data_karkhana/issues',  # Replace with the URL for issue tracking
        'Source': 'https://github.com/timsinashok/data_karkhana',  # Replace with the URL of your package repository
    },
)
