#		https://sqlite.org/2017/sqlite-autoconf-3200000.tar.gz
Summary:	The SQLite package is a software library that implements a self-contained, serverless, zero-configuration, transactional SQL database engine
Name:		sqlite-autoconf
Version:	3200000
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
Source0:	%{name}-%{version}.tar.gz
%description
	The SQLite package is a software library that implements a self-contained, serverless, zero-configuration, transactional SQL database engine
%prep
%setup -q -n %{NAME}-%{VERSION}
%build
	./configure \
		--prefix=%{_prefix} \
		--disable-static \
		CFLAGS="-g -O2 -DSQLITE_ENABLE_FTS3=1 \
		-DSQLITE_ENABLE_COLUMN_METADATA=1 \
		-DSQLITE_ENABLE_UNLOCK_NOTIFY=1 \
		-DSQLITE_SECURE_DELETE=1 \
		-DSQLITE_ENABLE_DBSTAT_VTAB=1" 
	make %{?_smp_mflags}
%install
	make DESTDIR=%{buildroot} install
	#	Copy license/copying file 
	#	install -D -m644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE
	#	Create file list
	rm -rf %{buildroot}/usr/share/info/dir
	find %{buildroot} -name '*.la' -delete
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
	%defattr(-,root,root)
	%{_bindir}/sqlite3
	%{_includedir}/*.h
	%{_libdir}/libsqlite3.so
	%{_libdir}/libsqlite3.so.0
	%{_libdir}/libsqlite3.so.0.8.6
	%{_libdir}/pkgconfig/sqlite3.pc
	%{_mandir}/man1/*.gz
%changelog
*	Tue Mar 06 2018 baho-utot <baho-utot@columbus.rr.com> 3200000-1
-	Initial build.	First version