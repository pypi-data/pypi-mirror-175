from setuptools import setup, find_packages


setup(
    name='face_detec',
    version='0.0.6',
    author="st",
    author_email='209tungns@gmail.com',
    packages=find_packages(),
    # package_dir={},
    url='https://github.com/209sontung/NEU-ID',
    keywords=['face_detection', 'face_alignment'],
    install_requires=[
          'scikit-learn',
          'opencv-python',
          'mediapipe',
          'numpy'
      ],

)