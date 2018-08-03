#		https://downloads.sourceforge.net/qpdf/qpdf-6.0.0.tar.gz
Summary:	The Qpdf package contains command-line programs and library that do structural, content-preserving transformations on PDF files
Name:		qpdf
Version:	6.0.0
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
Requires:	pcre
Source0:	%{name}-%{version}.tar.gz
%description
	The Qpdf package contains command-line programs and library that do structural, content-preserving transformations on PDF files
%prep
%setup -q -n %{NAME}-%{VERSION}
%build
	./configure \
		--prefix=%{_prefix} \
		 --disable-static \
		--docdir=%{_datarootdir}/doc/%{NAME}-%{VERSION}
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
	%{_bindir}/fix-qdf
	%{_bindir}/qpdf
	%{_bindir}/zlib-flate
	%{_includedir}/%{NAME}
	%{_libdir}/libqpdf.so
	%{_libdir}/libqpdf.so.17
	%{_libdir}/libqpdf.so.17.0.0
	%{_libdir}/pkgconfig/libqpdf.pc
	%{_datarootdir}/doc/qpdf-6.0.0
	%{_mandir}/man1/*.gz
%changelog
*	Tue Mar 06 2018 baho-utot <baho-utot@columbus.rr.com> 6.0.0-1
-	Initial build.	First version