#
# Conditional build:
%bcond_with	tests		# build with tests
# TODO:
# - runtime Requires if any
%define		kdeframever	5.107
%define		qtver		5.15.2
%define		kfname		karchive

Summary:	Reading, creating, and manipulating file archives
Name:		kf5-%{kfname}
Version:	5.107.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	d26d850fb786b4269f6ddce56bccee33
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Network-devel >= %{qtver}
BuildRequires:	Qt5Test-devel >= %{qtver}
BuildRequires:	bzip2-devel
BuildRequires:	cmake >= 3.16
BuildRequires:	kf5-extra-cmake-modules >= %{version}
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	xz-devel
BuildRequires:	zlib-devel
BuildRequires:	zstd-devel
Requires:	Qt5Core >= %{qtver}
Requires:	kf5-dirs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt5dir		%{_libdir}/qt5

%description
KArchive provides classes for easy reading, creation and manipulation
of "archive" formats like ZIP and TAR.

If also provides transparent compression and decompression of data,
like the GZip format, via a subclass of QIODevice.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt5Core-devel >= %{qtver}
Requires:	cmake >= 3.16

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
install -d build
cd build
%cmake -G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	..
%ninja_build

%if %{with tests}
ctest
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README.md
%ghost %{_libdir}/libKF5Archive.so.5
%attr(755,root,root) %{_libdir}/libKF5Archive.so.*.*
%config(noreplace) %verify(not md5 mtime size) %{_datadir}/qlogging-categories5/karchive.categories
%{_datadir}/qlogging-categories5/karchive.renamecategories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF5/KArchive
%{_libdir}/libKF5Archive.so
%{_libdir}/cmake/KF5Archive
%{qt5dir}/mkspecs/modules/qt_KArchive.pri
