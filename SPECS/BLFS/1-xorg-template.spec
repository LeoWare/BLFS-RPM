#	
Summary:	
Name:		
Version:	
Release:	1
License:	Any
URL:		Any
Group:		BLFS/Xorg
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
Requires:	xorg-protocol-headers
Source0:	%{name}-%{version}.tar.bz2
%description
	
%define		XORG_CONFIG	--prefix=%{_prefix} --sysconfdir=/etc --localstatedir=/var --disable-static
%prep
%setup -q -n %{NAME}-%{VERSION}
%build
	./configure %{XORG_CONFIG}
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
	/sbin/ldconfig
	pushd /usr/share/info
		rm -v dir
		for f in *;do install-info $f dir 2>/dev/null;done
	popd
%postun
	/sbin/ldconfig
%files -f filelist.rpm
	%defattr(-,root,root)
%changelog
*	Fri Feb 16 2018 baho-utot <baho-utot@columbus.rr.com> -1
-	Initial build.	First version