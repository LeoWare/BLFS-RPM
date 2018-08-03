#		http://www.mega-nerd.com/SRC/libsamplerate-0.1.9.tar.gz
Summary:	libsamplerate is a sample rate converter for audio. 
Name:		libsamplerate
Version:	0.1.9
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
Source0:	%{name}-%{version}.tar.gz
%description
	libsamplerate is a sample rate converter for audio. 
%prep
%setup -q -n %{NAME}-%{VERSION}
%build
	./configure \
		--prefix=%{_prefix} \
		--disable-static
	make %{?_smp_mflags}
%install
	make htmldocdir=%{_datarootdir}/doc/%{name}-%{version} DESTDIR=%{buildroot} install
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
	%{_bindir}/sndfile-resample
	%{_includedir}/samplerate.h
	%{_libdir}/libsamplerate.so
	%{_libdir}/libsamplerate.so.0
	%{_libdir}/libsamplerate.so.0.1.8
	%{_libdir}/pkgconfig/samplerate.pc
	%{_datarootdir}/doc/%{name}-%{version}
%changelog
*	Fri Mar 09 2018 baho-utot <baho-utot@columbus.rr.com> 0.1.9-1
-	Initial build.	First version