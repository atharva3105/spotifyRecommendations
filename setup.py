from setuptools import setup, find_packages

requires = [
    'flask',
    'spotipy',
    'html5lib',
    'requests',
    'requests_html',
    'beautifulsoup4',
    'youtube_dl',
    'pathlib',
    'pandas'
]

setup(
    name='StatForSpotify',
    version='1.0',
    description='An application that analyze your spotify liked songs',
    author='Atharva Tidke',
    author_email='atharvatidk321@gmail.com',
    keywords='web flask',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires
)