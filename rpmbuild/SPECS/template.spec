Summary:	
Name:		
Version:	
Release:	1
License:
URL:		
Group:		
Vendor:		Bildanet
Distribution:	Octothorpe
Source0:	%{name}-%{version}.tar.gz
Patch0:		
%description

%prep
%setup -q
%patch0 -p0
%build
./configure \
	CFLAGS="%{optflags}" \
	CXXFLAGS="%{optflags}" \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--htmldir=%{_docdir}/%{name}-%{version} \
	--docdir=%{_docdir}/%{name}-%{version}

./configure CFLAGS="%{optflags}" CXXFLAGS="%{optflags}" \
	--prefix=%{_prefix} \
	--exec-prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--sbindir=%{_sbindir} \
	--sysconfdir=/etc \
	--datadir=/%{_datarootdir} \
	--includedir=%{_includedir} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--localstatedir=%{_localstatedir}
	--sharedstatedir=%{_sharedstatedir} \
	--mandir=%{_mandir} \
	--infodir=/%{_infodir}
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
#make PREFIX=%{buildroot}/usr install
find %{buildroot}/%{_libdir} -name '*.a'  -delete
find %{buildroot}/%{_libdir} -name '*.la' -delete
rm %{buildroot}/%{_infodir}
%find_lang %{name}
%{_fixperms} %{buildroot}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post /sbin/ldconfig
%postun /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*
%{_includedir}/*
%{_datarootdir}/
%{_docdir}/%{name}-%{version}/*
%{_infodir}/*
%{_mandir}/*/*
%changelog
*	Sun May 19 2013 baho-utot <baho-utot@columbus.rr.com> -1
-	Initial build.	First version