import httpx

MDAPI_URL = "https://mdapi.fedoraproject.org/{branch}/pkg/python3-{name}"
COPR_URL = "https://copr.fedorainfracloud.org/api_3/package"


def has_package_in_repository(name: str, chroot: str, project: str | None = None) -> bool:
    if _in_fedora(name, chroot):
        return True
    if project is not None and _in_copr(name, project):
        return True
    return False


def _in_fedora(name: str, chroot: str) -> bool:
    url = MDAPI_URL.format(branch=_branch(chroot), name=name)
    return httpx.get(url, timeout=120).status_code == 200


def _in_copr(name: str, project: str) -> bool:
    owner, projectname = project.split("/", 1)
    response = httpx.get(
        COPR_URL,
        timeout=120,
        params={
            "ownername": owner,
            "projectname": projectname,
            # for now when building the package follow the convention: `python-packagename`
            "packagename": f"python-{name}",
            "with_latest_build": "false",
            "with_latest_succeeded_build": "false" 
        },
    )
    return response.status_code == 200


def _branch(chroot: str) -> str:
    # handle rawhide naming as well here, for now skipping it
    return f"f{chroot.split("-")[1]}"
