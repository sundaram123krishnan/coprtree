"""
Project wide constants
"""

ECOSYSTEMS_BASE_URL = "https://packages.ecosyste.ms/api/v1/registries"
LATEST_VERSION_URL = (
    f"{ECOSYSTEMS_BASE_URL}/{{provider}}/packages/{{name}}/latest_version"
)
VERSION_URL = (
    f"{ECOSYSTEMS_BASE_URL}/{{provider}}/packages/{{name}}/versions/{{version}}"
)
PACKAGE_VERSIONS_URL = (
    f"{ECOSYSTEMS_BASE_URL}/{{provider}}/packages/{{name}}/version_numbers"
)

METALINK_URL = "https://mirrors.fedoraproject.org/metalink"
FEDORA_METALINK = f"{METALINK_URL}?repo=fedora-{{release}}&arch={{arch}}"
UPDATES_METALINK = f"{METALINK_URL}?repo=updates-released-f{{release}}&arch={{arch}}"
OPENSUSE_DOWNLOAD = "https://download.opensuse.org"
_OSS_REPOMD = "/repo/oss/repodata/repomd.xml.metalink"
OPENSUSE_LEAP_METALINK = (
    f"{OPENSUSE_DOWNLOAD}/distribution/leap/{{release}}{_OSS_REPOMD}"
)
OPENSUSE_TUMBLEWEED_METALINK = f"{OPENSUSE_DOWNLOAD}/tumbleweed{_OSS_REPOMD}"
OPENSUSE_TUMBLEWEED_PORTS_METALINK = (
    f"{OPENSUSE_DOWNLOAD}/ports/{{port_arch}}/tumbleweed{_OSS_REPOMD}"
)
COPR_BASEURL = "https://download.copr.fedorainfracloud.org/results/{project}/{chroot}/"
CACHEDIR = "~/.cache/coprtree/{chroot}/{project}"

REGISTRY_BY_ALIAS = {"pypi": "pypi.org", "cpan": "metacpan.org"}

# make it configurable??
TIMEOUT = 120

MAX_WORKERS = 8
