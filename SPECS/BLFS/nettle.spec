#	nettle-3.3.tar.gz
Summary:	The Nettle package contains a low-level cryptographic library that is designed to fit easily in many contexts
Name:		nettle
Version:	3.3
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
Requires:	openssl >= 1.1.0f
Source0:	%{name}-%{version}.tar.gz
%description
	The Nettle package contains a low-level cryptographic library that is designed to fit easily in many contexts

%prep
%setup -q -n %{NAME}-%{VERSION}
%build
	./configure \
		--prefix=%{_prefix} \
		--disable-static
	make %{?_smp_mflags}
%install
	make DESTDIR=%{buildroot} install
	chmod   -v   755 %{buildroot}/usr/lib/lib{hogweed,nettle}.so
	install -v -m755 -d %{buildroot}/usr/share/doc/nettle-3.3
	install -v -m644 nettle.html %{buildroot}/usr/share/doc/nettle-3.3
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
*	Tue Jan 09 2018 baho-utot <baho-utot@columbus.rr.com> nettle-3.3-1
-	Initial build.	First version