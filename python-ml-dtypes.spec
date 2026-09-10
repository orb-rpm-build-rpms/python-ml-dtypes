# scikit-build-core compiles the extension in its own out-of-tree build
# directory, so debug source extraction finds no files and the debugsource
# subpackage is empty (a fatal "Empty %%files" error). Disable the debug
# packages, as with the other scikit-build C++ extensions in this stack.
%global debug_package %{nil}

Name:           python-ml-dtypes
Version:        0.6.0
Release:        %autorelease
Summary:        Stand-alone NumPy dtype extensions used in machine learning

# The package itself is Apache-2.0. It bundles a subset of the Eigen headers
# (third_party/eigen), which are MPL-2.0, to implement bfloat16/float8 math.
License:        Apache-2.0 AND MPL-2.0
URL:            https://github.com/jax-ml/ml_dtypes
Source:         %{pypi_source ml_dtypes}

BuildRequires:  python3-devel
# The _ml_dtypes_ext extension is C++ built with CMake (Ninja generator).
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  ninja-build


%global _description %{expand:
ml_dtypes is a stand-alone implementation of several NumPy dtype extensions
used in machine learning, including bfloat16 and a range of float8 and
sub-byte integer types.}

%description %_description

%package -n     python3-ml-dtypes
Summary:        %{summary}
# A subset of the Eigen headers is compiled into the extension.
Provides:       bundled(eigen3)

%description -n python3-ml-dtypes %_description


%prep
%autosetup -p1 -n ml_dtypes-%{version}

# Upstream derives the version dynamically via scikit-build-core's regex metadata
# provider reading ml_dtypes/__init__.py. In this build environment that provider
# yields 0.0.0, which pyproject-rpm-macros rejects. Pin the version statically to
# the packaged release and drop the dynamic provider so the two agree.
sed -i 's/^dynamic = \["version"\].*/version = "%{version}"/' pyproject.toml
sed -i '/^\[\[tool.dynamic-metadata\]\]/,/^input = /d' pyproject.toml


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
# Automatically extracted from wheel
%pyproject_save_files -l ml_dtypes


%check
%pyproject_check_import


%files -n python3-ml-dtypes -f %{pyproject_files}


%changelog
%autochangelog
