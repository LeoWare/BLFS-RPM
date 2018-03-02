#	 https://ftp.gnu.org/gnu/libunistring/libunistring-0.9.7.tar.xz
Summary:	libunistring is a library that provides functions for manipulating Unicode strings and for manipulating C strings according to the Unicode standard
Name:		libunistring
Version:	0.9.7
Release:	1
License:	Any
URL:		Any
Group:		BLFS/Multimedia
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
Source0:	%{name}-%{version}.tar.xz
%description
	libunistring is a library that provides functions for manipulating Unicode strings and for manipulating C strings according to the Unicode standard
%prep
%setup -q -n %{NAME}-%{VERSION}
%build
	./configure \
		--prefix=%{_prefix} \
		--disable-static \
		--docdir=%{_datarootdir}/doc/%{name}-%{version}
	make %{?_smp_mflags}
%install
	make DESTDIR=%{buildroot} install
	#	Copy license/copying file 
	#	install -D -m644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE
	#	Create file list
	rm -rf %{buildroot}/usr/share/info/dir
	find %{buildroot} -name '*.la' -delete
	find "${RPM_BUILD_ROOT}" -not -type d -print > filelist.rpm
	sed -i "s|^${RPM_BUILD_ROOT}||" filelist.rpm
%post	-p /sbin/ldconfig
	pushd /usr/share/info
	rm -v dir
	for f in *
		do install-info $f dir 2>/dev/null
	done
	popd
%postun	-p /sbin/ldconfig
	pushd /usr/share/info
	rm -v dir
	for f in *
		do install-info $f dir 2>/dev/null
	done
	popd
%files
	%defattr(-,root,root)
	%{_includedir}/*.h
	%{_includedir}/unistring
	%{_libdir}/libunistring.so
	%{_libdir}/libunistring.so.2
	%{_libdir}/libunistring.so.2.0.0
	%{_datarootdir}/doc/%{name}-%{version}
	%{_infodir}/libunistring.info.gz
%changelog
*	Wed Feb 14 2018 baho-utot <baho-utot@columbus.rr.com> 0.9.7-1
-	Initial build.	First version