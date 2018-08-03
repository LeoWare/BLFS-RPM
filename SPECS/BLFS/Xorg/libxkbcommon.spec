#	
Summary:	libxkbcommon is a keymap compiler and support library which processes a reduced subset of keymaps as defined by the XKB specification
Name:		libxkbcommon
Version:	0.7.2
Release:	1
License:	Any
URL:		Any
Group:		BLFS/Xorg
Vendor:		Octothorpe
Distribution:	BLFS-8.1
Requires:	xkeyboard-config libxcb
Source0:	%{name}-%{version}.tar.xz
%description
	libxkbcommon is a keymap compiler and support library which processes a reduced subset of keymaps as defined by the XKB specification
%define		XORG_CONFIG	--prefix=%{_prefix} --sysconfdir=/etc --localstatedir=/var --disable-static
%prep
%setup -q -n %{NAME}-%{VERSION}
%build
	./configure %{XORG_CONFIG} \
		--docdir=/usr/share/doc/%{name}-%{version}
	make %{?_smp_mflags}
%install
	make DESTDIR=%{buildroot} install
	#	Copy license/copying file 
	#	install -D -m644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE
	#	Create file list
	rm -rf %{buildroot}/usr/share/info/dir
	find %{buildroot} -name '*.la' -delete
%postun
	/sbin/ldconfig
%files
	%defattr(-,root,root)
	%{_includedir}/xkbcommon
	%{_libdir}/*.so
	%{_libdir}/*.0
	%{_libdir}/pkgconfig/*.pc
%changelog
*	Fri Feb 16 2018 baho-utot <baho-utot@columbus.rr.com> 0.7.2-1
-	Initial build.	First version