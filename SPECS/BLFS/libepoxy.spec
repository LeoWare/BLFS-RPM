#	libepoxy-1.4.3.tar.xz
Summary:	libepoxy is a library for handling OpenGL function pointer management. 
Name:		libepoxy
Version:	1.4.3
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
Requires:	mesa >= 17.1.6
Source0:	%{name}-%{version}.tar.xz
%description
	libepoxy is a library for handling OpenGL function pointer management. 
%prep
%setup -q -n %{NAME}-%{VERSION}
%build
	./configure \
		--prefix=%{_prefix}
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
*	Fri Feb 16 2018 baho-utot <baho-utot@columbus.rr.com> libepoxy-1.4.3-1
-	Initial build.	First version