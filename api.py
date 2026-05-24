from main import BuildTarget, PackageMetadata


BASE_URL = "https://packages.ecosyste.ms/api/v1"

# when version=None
# https://packages.ecosyste.ms/api/v1/registries/pypi.org/packages/django/latest_version

# when specificied specific version
# https://packages.ecosyste.ms/api/v1/registries/pypi.org/packages/django/versions/5.0.4

def fetch_package_metadata(target: BuildTarget) -> PackageMetadata:
    pass
