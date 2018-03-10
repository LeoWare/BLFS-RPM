#	libgcrypt-1.8.0.tar.bz2
Summary:	The libgcrypt package contains a general purpose crypto library based on the code used in GnuPG
Name:		libgcrypt
Version:	1.8.0
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
Requires:	libgpg-error >= 1.27
Source0:	%{name}-%{version}.tar.bz2
%description
	The libgcrypt package contains a general purpose crypto library based on the code used in GnuPG.
	The library provides a high level interface to cryptographic building blocks using an extendable
	and flexible API. 
%prep
%setup -q -n %{NAME}-%{VERSION}
%build
	./configure \
		--prefix=%{_prefix}
	make %{?_smp_mflags}
%install
	make DESTDIR=%{buildroot} install
	install -v -dm755   %{buildroot}/usr/share/doc/libgcrypt-1.8.0
	install -v -m644    README doc/{README.apichanges,fips*,libgcrypt*} %{buildroot}/usr/share/doc/libgcrypt-1.8.0
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
*	Tue Feb 13 2018 baho-utot <baho-utot@columbus.rr.com> libgcrypt-1.8.0-1
-	Initial build.	First version