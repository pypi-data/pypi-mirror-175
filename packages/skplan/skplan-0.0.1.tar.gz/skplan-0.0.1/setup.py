from setuptools import setup

setup_requires = []

install_requires = ["numpy", "matplotlib", "scipy", "robot_descriptions"]

setup(
    name="skplan",
    version="0.0.1",
    description="scipy based robot planning framework",
    author="Hirokazu Ishida",
    author_email="h-ishida@jsk.imi.i.u-tokyo.ac.jp",
    license="MIT",
    install_requires=install_requires,
    package_data={"skplan": ["py.typed"]},
)
