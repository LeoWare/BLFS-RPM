#	libffi-3.2.1.tar.gz
Summary:	The libffi library provides a portable, high level programming interface to various calling conventions.
Name:		libffi
Version:	3.2.1	
Release:	1
License:	Any
URL:		Any
Group:		BLFS/General_Libraries
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
Source0:	%{name}-%{version}.tar.gz
%description
	The libffi library provides a portable, high level programming interface to various calling conventions.
	This allows a programmer to call any function specified by a call interface description at run time. 

%prep
%setup -q -n %{NAME}-%{VERSION}
	sed -e '/^includesdir/ s/$(libdir).*$/$(includedir)/' -i include/Makefile.in
	sed -e '/^includedir/ s/=.*$/=@includedir@/' -e 's/^Cflags: -I${includedir}/Cflags:/' -i libffi.pc.in
%build
	./configure \
		--prefix=%{_prefix} \
		--disable-static
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
*	Tue Jan 09 2018 baho-utot <baho-utot@columbus.rr.com> -1
-	Initial build.	First version