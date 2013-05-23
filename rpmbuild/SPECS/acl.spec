Summary:	Access control list utilities, libraries and headers
Name:		acl
Version:	2.2.51
Release:	1
License:	LGPL
URL:		http://savannah.nongnu.org/projects/acl
Group:		BLFS/Security
Vendor:		Bildanet
Distribution:	Octothorpe
Source0:	%{name}-%{version}.src.tar.gz
%description
The acl package contains utilities to administer Access Control Lists
which are used to define more fine-grained discretionary access 
rights for files and directories.
%prep
%setup -q -n %{name}-%{version}
sed -i -e 's|/@pkg_name@|&-@pkg_version@|' include/builddefs.in
%build
CFLAGS="%{optflags}" \
CXXFLAGS="%{optflags}" \
INSTALL_USER=root  \
INSTALL_GROUP=root \
./configure \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir}
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DIST_ROOT==%{buildroot} install install-lib install-dev
find %{buildroot}/ -name '*.a'  -delete
find %{buildroot}/ -name '*.la' -delete
#rm %{buildroot}/%{_infodir}
#%find_lang %{name}
%{_fixperms} %{buildroot}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
#%files -f %{name}.lang
%files
%defattr(-,root,root)
#%{_bindir}/*
#%{_libdir}/*
#%{_includedir}/*
#%{_datarootdir}/
#%{_docdir}/%{name}-%{version}/*
#%{_infodir}/*
#%{_mandir}/man1/*
#%{_mandir}/man2/*
#%{_mandir}/man3/*
#%{_mandir}/man4/*
#%{_mandir}/man5/*
#%{_mandir}/man6/*
#%{_mandir}/man7/*
#%{_mandir}/man8/*
%changelog
*	Thu May 23 2013 baho-utot <baho-utot@columbus.rr.com> 2.2.51-1
-	Initial build.	First version