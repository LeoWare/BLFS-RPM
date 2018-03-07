#		http://www.tortall.net/projects/yasm/releases/yasm-1.3.0.tar.gz
Summary:	libjpeg-turbo is a fork of the original IJG libjpeg which uses SIMD to accelerate baseline JPEG compression and decompression.
Name:		yasm
Version:	1.3.0
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
Source0:	%{name}-%{version}.tar.gz
%description
	libjpeg-turbo is a fork of the original IJG libjpeg which uses SIMD to accelerate baseline
	JPEG compression and decompression. libjpeg is a library that implements JPEG image encoding,
	decoding and transcoding.
%prep
%setup -q -n %{NAME}-%{VERSION}
sed -i 's#) ytasm.*#)#' Makefile.in
%build
	./configure \
		--prefix=%{_prefix}
	make %{?_smp_mflags}
%install
	make DESTDIR=%{buildroot} install
	#	Copy license/copying file 
	#	install -D -m644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE
	#	Create file list
	rm -rf %{buildroot}/usr/share/info/dir
	find %{buildroot} -name '*.la' -delete
%files
	%defattr(-,root,root)
	%{_bindir}/yasm
	%{_includedir}/*.h
	%{_includedir}/libyasm/*.h
	%{_libdir}/libyasm.a
	%{_mandir}/man1/*.gz
	%{_mandir}/man7/*.gz
%changelog
*	Tue Mar 06 2018 baho-utot <baho-utot@columbus.rr.com> 1.3.0-1
-	Initial build.	First version