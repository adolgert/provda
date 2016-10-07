from setuptools import setup


setup(name="provda",
      version=0.1,
      description="Settings and provenance tracking",
      long_description="""Responsible for presenting per-module
      settings from settings files or command line arguments
      and for tracking what is read or written.""",
      classifiers=[
          "Development Status :: 2 - Pre-Alpha",
          "Environment :: Console",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: Apache Software License",
          "Natural Language :: English",
          "Topic :: System :: Logging",
      ],
      keywords="settings provenance",
      url="https://github.com/adolgert/provda",
      author="Andrew Dolgert",
      author_email="adolgert@uw.edu",
      license="Apache",
      packages=["provda"],
      install_requires = [
          "GitPython",
          "h5py",
          "PyPDF2",
          "wrapt"
      ],
      dependency_links = [
        "https://github.com/trungdong/prov.git"
      ],
      zip_safe=True,
      scripts=[]
      )
