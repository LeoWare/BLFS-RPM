#	http://download.kde.org/stable/phonon/4.9.1/phonon-4.9.1.tar.xz
Summary:	The Extra Cmake Modules package contains extra CMake modules used by KDE Frameworks 5 and other packages
Name:		phonon
Version:	4.9.1
Release:	1
License:	Any
URL:		Any
Group:		BLFS/KDE
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
Requires:	cmake >= 3.9.1, extra-cmake-modules >= 5.37.0, glib >= 2.52.3, qt >= 5.9.1 
Source0:	%{name}-%{version}.tar.xz

%description
The Extra Cmake Modules package contains extra CMake modules used by KDE Frameworks 5 and other packages

%prep
%setup -q -n %{NAME}-%{VERSION}
	sed -i '/"lib64"/s/64//' kde-modules/KDEInstallDirs.cmake
%build
	mkdir build
	cd    build
	cmake -DCMAKE_INSTALL_PREFIX=/usr \
		-DCMAKE_BUILD_TYPE=Release \
		-DPHONON_BUILD_PHONON4QT5=ON \
		-Wno-dev ..
	make %{?_smp_mflags}

%install
	cd    build
	make DESTDIR=%{buildroot} install
	#	Copy license/copying file 
	#	install -D -m644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE
	#	Create file list
%files
	%defattr(-,root,root)
	%{_datarootdir}/ECM

%changelog
*	Wed Feb 14 2018 baho-utot <baho-utot@columbus.rr.com> phonon-4.9.1-1
-	Initial build.	First version