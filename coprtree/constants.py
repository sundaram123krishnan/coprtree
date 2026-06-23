"""
Project wide constants
"""

BASE_URL = "https://packages.ecosyste.ms/api/v1"
LATEST_VERSION_URL = (
    f"{BASE_URL}/registries/{{provider}}/packages/{{name}}/latest_version"
)
VERSION_URL = (
    f"{BASE_URL}/registries/{{provider}}/packages/{{name}}/versions/{{version}}"
)

METALINK_URL = "https://mirrors.fedoraproject.org/metalink"
FEDORA_METALINK = f"{METALINK_URL}?repo=fedora-{{release}}&arch={{arch}}"
UPDATES_METALINK = f"{METALINK_URL}?repo=updates-released-f{{release}}&arch={{arch}}"
COPR_BASEURL = "https://download.copr.fedorainfracloud.org/results/{project}/{chroot}/"

REGISTRY_BY_ALIAS = {"pypi": "pypi.org", "cpan": "metacpan.org"}

# make it configurable??
TIMEOUT = 120
