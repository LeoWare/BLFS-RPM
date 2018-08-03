#	xorg-server-1.19.3.tar.bz2
Summary:	The Xorg Server is the core of the X Window system
Name:		xorg-server
Version:	1.19.3
Release:	1
License:	Any
URL:		Any
Group:		BLFS/Xorg
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
Requires:	xorg-protocol-headers
Requires:	openssl >= 1.1.0f, pixman >= 0.34.0,
Source0:	%{name}-%{version}.tar.bz2
%description
	The Xorg Server is the core of the X Window system
%define		XORG_CONFIG	--prefix=%{_prefix} --sysconfdir=/etc --localstatedir=/var --disable-static
%prep
%setup -q -n %{NAME}-%{VERSION}
%build
	./configure %{XORG_CONFIG} \
		--enable-glamor \
		--enable-suid-wrapper \
		--disable-systemd-logind \
		--with-xkb-output=/var/lib/xkb \
		--disable-install-setuid
	#	--enable-install-setuid \
	make %{?_smp_mflags}
%install
	make DESTDIR=%{buildroot} install
	install -vdm 755 %{buildroot}/etc/X11/xorg.conf.d
	#	Copy license/copying file 
	#	install -D -m644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE
	#	Create file list
	rm -rf %{buildroot}/usr/share/info/dir
	find %{buildroot} -name '*.la' -delete
	find "${RPM_BUILD_ROOT}" -not -type d -print > filelist.rpm
	sed -i "s|^${RPM_BUILD_ROOT}||" filelist.rpm
%post
	cat >> %{buildroot}/etc/sysconfig/createfiles <<- "EOF"
		/tmp/.ICE-unix dir 1777 root root
		/tmp/.X11-unix dir 1777 root root
	EOF
	chmod u+s /usr/libexec/Xorg
	chmod u+s /usr/bin/Xorg
%files -f filelist.rpm
	%defattr(-,root,root)
%changelog
*	Wed Feb 14 2018 baho-utot <baho-utot@columbus.rr.com> xorg-server-1.19.3-1
-	Initial build.	First version