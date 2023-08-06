from setuptools import setup

setup(name='papai_public',
      version='0.1.6',
      description="Public papAI minio writer/reader",
      author="Datategy",
      py_modules=['papai_minio', 'object_storage_client'],
      package_dir={'': 'src'},
      install_requires=["pyarrow==2.0.0", "minio==7.1.9", "loguru==0.5.3", "azure-storage-blob==12.14.0", "google-cloud-storage"]
)