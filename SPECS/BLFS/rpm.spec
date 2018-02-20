Summary:	RPM package manager
Name:		rpm
Version:	4.14.0
Release:	2
License:	GPL
URL:		http://ftp.rpm.org/releases/rpm-4.14.x
Group:		LFS/BASE
Vendor:		Octothorpe
Distribution:	LFS-8.1
ExclusiveArch:	x86_64
BuildRoot:	%{buildroot}
Source0:	http://ftp.rpm.org/releases/rpm-4.14.x/%{name}-%{version}.tar.bz2
Source1:	http://download.oracle.com/berkeley-db/db-6.0.20.tar.gz
%description
	RPM package manager
%prep
%setup -q -n %{name}-%{version}
%setup -q -T -D -a 1 -n %{name}-%{version}
	sed -i 's/--srcdir=$db_dist/--srcdir=$db_dist --with-pic/' db3/configure
%build
	ln -vs db-6.0.20 db
	./configure \
		--prefix=%{_prefix} \
		--with-crypto=openssl \
		--without-external-db \
		--without-archive \
		--program-prefix= \
		--sysconfdir=/etc \
		--disable-dependency-tracking \
		--without-lua \
		--disable-silent-rules \
		--enable-python
	make %{?_smp_mflags}
%install
	make DESTDIR=%{buildroot} install
	#	Create file list
	%find_lang %{NAME}
	find %{buildroot} -name '*.la' -delete
#	find "${RPM_BUILD_ROOT}" -not -type d -print > filelist.rpm
#	sed -i "s|^${RPM_BUILD_ROOT}||" filelist.rpm
%clean
	rm -rf $RPM_BUILD_ROOT
%files -f %{NAME}.lang
	%defattr(-,root,root)
	%{_bindir}/*
	%{_includedir}/rpm
	%{_libdir}/*.so
	%{_libdir}/*.8
	%{_libdir}/*.so.8*.0
	%{_libdir}/pkgconfig/*.pc
	%{_libdir}/python2.7/site-packages/rpm
	%{_libdir}/rpm-plugins
	%{_libdir}/rpm
	%{_mandir}/fr/man8/rpm.8.gz
	%{_mandir}/ja/man8/*.gz
	%{_mandir}/ko/man8/*.gz
	%{_mandir}/man1/*.gz
	%{_mandir}/man8/*.gz
	%{_mandir}/pl/man1/*.gz
	%{_mandir}/pl/man8/*.gz
	%{_mandir}/ru/man8/*.gz
	%{_mandir}/sk/man8/rpm.8.gz
%changelog
*	Tue Feb 20 2018 baho-utot <baho-utot@columbus.rr.com> 4.14.0-2
-	Added python bindings for rpmlint
*	Mon Jan 01 2018 baho-utot <baho-utot@columbus.rr.com> 4.14.0-1
-	LFS-8.1
