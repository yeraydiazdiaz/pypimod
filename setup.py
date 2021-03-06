import codecs
import os
import re

from setuptools import find_packages, setup


HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    """
    Build an absolute path from *parts* and and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    with codecs.open(os.path.join(HERE, *parts), "rb", "utf-8") as f:
        return f.read()


def read_requirements_file(*parts):
    return [
        parse_requirement_line(line)
        for line in read(*parts).strip().split("\n")
        if line and not line.startswith("#")
    ]


def parse_requirement_line(line):
    if line.startswith("git+https"):
        return line[line.find("#egg=") + 5 :]
    return line[: line.find(" ")] if " " in line else line


def find_meta(meta):
    """
    Extract __*meta*__ from META_FILE.
    """
    meta_match = re.search(
        r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta), META_FILE, re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError("Unable to find __{meta}__ string.".format(meta=meta))


NAME = "pypimod"
META_PATH = os.path.join("src", "pypimod", "__init__.py")
META_FILE = read(META_PATH)
PACKAGES = find_packages(where="src")
KEYWORDS = ["pypi", "moderators"]
PROJECT_URLS: dict = {}
CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: Implementation :: CPython",
    "Topic :: Software Development :: Libraries :: Python Modules",
]
INSTALL_REQUIRES = read_requirements_file("requirements", "main.txt")
EXTRAS_REQUIRE = {"tests": read_requirements_file("requirements", "test.txt")[1:]}
EXTRAS_REQUIRE["dev"] = EXTRAS_REQUIRE["tests"]
VERSION = find_meta("version")
URL = find_meta("url")
LONG = read("README.md")


if __name__ == "__main__":
    setup(
        name=NAME,
        description=find_meta("description"),
        license=find_meta("license"),
        url=URL,
        project_urls=PROJECT_URLS,
        version=VERSION,
        author=find_meta("author"),
        author_email=find_meta("email"),
        maintainer=find_meta("author"),
        maintainer_email=find_meta("email"),
        keywords=KEYWORDS,
        long_description=LONG,
        long_description_content_type="text/markdown",
        packages=PACKAGES,
        package_dir={"": "src"},
        python_requires=">=3.7.*",
        zip_safe=False,
        classifiers=CLASSIFIERS,
        install_requires=INSTALL_REQUIRES,
        extras_require=EXTRAS_REQUIRE,
        include_package_data=True,
        entry_points={"console_scripts": ["pypimod = pypimod.cli:cli"]},
    )
