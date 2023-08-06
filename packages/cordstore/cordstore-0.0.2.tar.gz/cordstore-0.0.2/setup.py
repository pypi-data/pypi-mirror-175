from setuptools import setup

setup(
    name="cordstore",
    author="jxzper",
    url="https://github.com/jxzper/cordstore",
    license='MIT',
    description='Utilize discord to store files in textchannels using bots or webhooks',
    version="0.0.2",
    install_requires=[
        "discord.py",
        "aiohttp",
    ],
    packages=['cordstore'],
    python_requires='>=3.8.0',
)
