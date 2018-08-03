#	libxml2-2.9.4.tar.gz
Summary:	The libxml2 package contains libraries and utilities used for parsing XML files. 	
Name:		libxml2
Version:	2.9.4
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
Requires:	Python >= 3.6.2
Source0:	%{name}-%{version}.tar.gz
%description
	The libxml2 package contains libraries and utilities used for parsing XML files. 
%prep
%setup -q -n %{NAME}-%{VERSION}
sed -i '/_PyVerify_fd/,+1d' python/types.c
%build
	./configure \
		--prefix=%{_prefix} \
		--disable-static \
		--with-history
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
*	Tue Feb 13 2018 baho-utot <baho-utot@columbus.rr.com> libxml2-2.9.4-1
-	Initial build.	First version