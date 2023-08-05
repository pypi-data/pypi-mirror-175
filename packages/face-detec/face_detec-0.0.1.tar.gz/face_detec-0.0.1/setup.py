from setuptools import setup, find_packages


setup(
    name='face_detec',
    version='0.0.1',
    author="Sontung",
    author_email='209tungns@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/209sontung/NEU-ID',
    keywords=['face_detection', 'face_alignment'],
    install_requires=[
          'scikit-learn',
          'opencv',
          'mediapipe',
          'numpy'
      ],

)