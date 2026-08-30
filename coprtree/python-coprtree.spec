Name:           python-coprtree
Version:        0.1.2
Release:        %autorelease
Summary:        Resolve a package's dependency tree into parallel Fedora Copr build levels

License:        GPL-2.0-or-later
URL:            https://github.com/sundaram123krishnan/coprtree
Source:         %{pypi_source coprtree}

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-dnf

%global _description %{expand:
Coprtree resolves a package's transitive dependency graph,
prunes anything the target distribution or your Copr project already provides,
and topologically sorts the rest into parallel build levels}

%description %_description

%package -n     python3-coprtree
Summary:        %{summary}
Requires:       python3-dnf
Requires:       python3-hawkey

%description -n python3-coprtree %_description


%prep
%autosetup -p1 -n coprtree-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -L coprtree


%check
%pytest tests/unit


%files -n python3-coprtree -f %{pyproject_files}
%license LICENSE
%doc README.md


%changelog
%autochangelog
