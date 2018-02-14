#	cmake-3.9.1.tar.gz
Summary:	The CMake package contains a modern toolset used for generating Makefiles
Name:		cmake
Version:	3.9.1
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
Requires:	 curl >= 7.55.1, libarchive >= 3.3.2 
Source0:	%{name}-%{version}.tar.gz
%description
	The CMake package contains a modern toolset used for generating Makefiles.
	It is a successor of the auto-generated configure script and aims to be
	platform- and compiler-independent. A significant user of CMake is KDE since version 4. 
%prep
%setup -q -n %{NAME}-%{VERSION}
	sed -i '/CMAKE_USE_LIBUV 1/s/1/0/' CMakeLists.txt
	sed -i '/"lib64"/s/64//' Modules/GNUInstallDirs.cmake
%build
	./bootstrap --prefix=%{_prefix} \
		--system-libs \
		--mandir=/share/man \
		--no-system-jsoncpp \
		--no-system-librhash \
		--docdir=/share/doc/cmake-3.9.1
	make %{?_smp_mflags}
%install
	make DESTDIR=%{buildroot} install
	rm -rf %{buildroot}/usr/share/cmake-3.9/Help
	#	Copy license/copying file 
	#	install -D -m644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE
	#	Create file list
	rm -rf %{buildroot}/usr/share/info/dir
	find %{buildroot} -name '*.la' -delete
	find "${RPM_BUILD_ROOT}" -not -type d -print > filelist.rpm
	sed -i "s|^${RPM_BUILD_ROOT}||" filelist.rpm
%post
	pushd /usr/share/info
	rm -v dir
	for f in *
		do install-info $f dir 2>/dev/null
	done
	popd
%files -f filelist.rpm
	%defattr(-,root,root)
%changelog
*	Tue Feb 13 2018 baho-utot <baho-utot@columbus.rr.com> cmake-3.9.1-1
-	Initial build.	First version