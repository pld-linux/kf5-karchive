# TODO:
# - runtime Requires if any
%define		kdeframever	5.10
%define		qtver		5.3.2
%define		kfname		karchive

Summary:	Reading, creating, and manipulating file archives
Name:		kf5-%{kfname}
Version:	5.10.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	http://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	84b3bb7303f5438247db4e292d9f3cf0
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Test-devel >= %{qtver}
BuildRequires:	bzip2-devel
BuildRequires:	cmake >= 2.8.12
BuildRequires:	kf5-extra-cmake-modules >= 1.4.0
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	xz-devel
BuildRequires:	zlib-devel
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

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
install -d build
cd build
%cmake \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	..
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build/ install \
        DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README.md
%attr(755,root,root) %ghost %{_libdir}/libKF5Archive.so.5
%attr(755,root,root) %{_libdir}/libKF5Archive.so.*.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF5/KArchive
%{_includedir}/KF5/karchive_version.h
%attr(755,root,root) %{_libdir}/libKF5Archive.so
%{_libdir}/cmake/KF5Archive
%{qt5dir}/mkspecs/modules/qt_KArchive.pri
