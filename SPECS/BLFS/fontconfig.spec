#	fontconfig-2.12.4.tar.bz2
Summary:	The Xorg libraries provide library routines that are used within all X Window applications.
Name:		fontconfig
Version:	2.12.4
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
	The Xorg libraries provide library routines that are used within all X Window applications.
%prep
%setup -q -n %{NAME}-%{VERSION}
rm -f src/fcobjshash.h
%build
	./configure --prefix=%{_prefix} \
		--sysconfdir=/etc \
		--localstatedir=/var \
		--disable-docs \
		--docdir=/usr/share/doc/fontconfig-2.12.4
	make %{?_smp_mflags}
%install
	make DESTDIR=%{buildroot} install
	install -v -dm755 %{buildroot}/usr/share/{man/man{1,3,5},doc/fontconfig-2.12.4/fontconfig-devel}
	install -v -m644 fc-*/*.1 %{buildroot}/usr/share/man/man1
	install -v -m644 doc/*.3 %{buildroot}/usr/share/man/man3
	install -v -m644 doc/fonts-conf.5 %{buildroot}/usr/share/man/man5
	install -v -m644 doc/fontconfig-devel/* %{buildroot}/usr/share/doc/fontconfig-2.12.4/fontconfig-devel
	install -v -m644 doc/*.{pdf,sgml,txt,html} %{buildroot}/usr/share/doc/fontconfig-2.12.4
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
*	Mon Feb 11 2018 baho-utot <baho-utot@columbus.rr.com> fontconfig-2.12.4-1
-	Initial build.	First version