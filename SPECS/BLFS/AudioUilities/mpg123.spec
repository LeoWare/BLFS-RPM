#		 https://downloads.sourceforge.net/mpg123/mpg123-1.25.6.tar.bz2
Summary:	The mpg123 package contains a console-based MP3 player.
Name:		mpg123
Version:	1.25.6
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
Source0:	%{name}-%{version}.tar.bz2
%description
	The mpg123 package contains a console-based MP3 player.
%prep
%setup -q -n %{NAME}-%{VERSION}
%build
	./configure \
		--prefix=%{_prefix}
	make %{?_smp_mflags}
%install
	make DESTDIR=%{buildroot} install
	#	Copy license/copying file 
	#	install -D -m644 LICENSE %{buildroot}%{_datarootdir}/licenses/%{name}/LICENSE
	#	Create file list
	rm -rf %{buildroot}/usr/share/info/dir
	find %{buildroot} -name '*.la' -delete
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
	%defattr(-,root,root)
#	%%{buildroot}%%{_datarootdir}/licenses/%%{name}/LICENSE
	%{_bindir}/mpg123
	%{_bindir}/mpg123-id3dump
	%{_bindir}/mpg123-strip
	%{_bindir}/out123
	%{_includedir}/*.h
	%{_libdir}/*.so
	%{_libdir}/*.0
	%{_libdir}/*.1
	%{_libdir}/*.5
	%{_libdir}/mpg123
	%{_libdir}/pkgconfig/*.pc
	%{_mandir}/man1/*.gz
%changelog
*	Wed Mar 07 2018 baho-utot <baho-utot@columbus.rr.com> 1.25.6-1
-	Initial build.	First version