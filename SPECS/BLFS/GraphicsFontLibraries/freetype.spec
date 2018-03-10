#	freetype-2.8.tar.bz2
Summary:	The Xorg libraries provide library routines that are used within all X Window applications.
Name:		freetype
Version:	2.8
Release:	1
License:	Any
URL:		Any
Group:		BLFS/Xorg
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
Requires:	xorg-protocol-headers
Source0:	%{name}-%{version}.tar.bz2
Source1:	freetype-doc-2.8.tar.bz2
%description
	The Xorg libraries provide library routines that are used within all X Window applications.
%prep
%setup -q -n %{NAME}-%{VERSION}
%setup -q -T -D -a 1  -n %{name}-%{version}
ln -s freetype-doc-2.8 doc
sed -ri "s:.*(AUX_MODULES.*valid):\1:" modules.cfg
sed -r "s:.*(#.*SUBPIXEL_RENDERING) .*:\1:" -i include/freetype/config/ftoption.h
%build
	./configure --prefix=/usr --disable-static
	make %{?_smp_mflags}
%install
	make DESTDIR=%{buildroot} install
	install -v -m755 -d %{buildroot}/usr/share/doc/%{name}-%{version}
	cp -v -R docs/*     %{buildroot}/usr/share/doc/%{name}-%{version}
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
		for f in *;do install-info $f dir 2>/dev/null;done
	popd
%files -f filelist.rpm
	%defattr(-,root,root)
%changelog
*	Mon Feb 11 2018 baho-utot <baho-utot@columbus.rr.com> freetype-2.8-1
-	Initial build.	First version