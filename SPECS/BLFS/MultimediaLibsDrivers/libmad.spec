#		https://downloads.sourceforge.net/mad/libmad-0.15.1b.tar.gz
Summary:	libmad is a high-quality MPEG audio decoder capable of 24-bit output
Name:		libmad
Version:	0.15.1b
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
Source0:	%{name}-%{version}.tar.gz
Patch0:		libmad-0.15.1b-fixes-1.patch
%description
	libmad is a high-quality MPEG audio decoder capable of 24-bit output
%prep
%setup -q -n %{NAME}-%{VERSION}
%patch0 -p1
sed "s@AM_CONFIG_HEADER@AC_CONFIG_HEADERS@g" -i configure.ac
touch NEWS AUTHORS ChangeLog
%build
	autoreconf -fi
	./configure \
		--prefix=%{_prefix} \
		--disable-static
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
	%{_includedir}/mad.h
	%{_libdir}/libmad.so
	%{_libdir}/libmad.so.0
	%{_libdir}/libmad.so.0.2.1
%changelog
*	Wed Mar 07 2018 baho-utot <baho-utot@columbus.rr.com> 0.15.1b-1
-	Initial build.	First version