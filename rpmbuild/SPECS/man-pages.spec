Summary:	Man pages
Name:		man-pages
Version:	3.51
Release:	3
License:	GPLv2
URL:		http://www.kernel.org/doc/man-pages
Group:		System Environment/Base
Vendor:		Bildanet
Distribution:	Octothorpe
Source:		%{name}-%{version}.tar.xz
BuildArch:	noarch
%description
The Man-pages package contains over 1,900 man pages.
%prep
%setup -q
%build
%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
rm -vf %{buildroot}%{_mandir}/man3/getspnam.3
rm -vf %{buildroot}%{_mandir}/man5/passwd.5
#	remove conflicting man pages attr
rm -vf %{buildroot}%{_mandir}/man2/*xattr*


%clean
rm -rf %{buildroot} %{_builddir}/*
%files
%defattr(-,root,root)
%{_mandir}/man1/*
%{_mandir}/man2/*
%{_mandir}/man3/*
%{_mandir}/man4/*
%{_mandir}/man5/*
%{_mandir}/man6/*
%{_mandir}/man7/*
%{_mandir}/man8/*
%changelog
*	Fri May 24 2013 baho-utot <baho-utot@columbus.rr.com> 3.51-2
-	Remove conflicting man pages
*	Fri May 10 2013 baho-utot <baho-utot@columbus.rr.com> 3.51-1
-	Update version to 3.51
*	Sun Mar 24 2013 baho-utot <baho-utot@columbus.rr.com> 3.50-1
-	Update version to 3.50
*	Sun Mar 21 2013 baho-utot <baho-utot@columbus.rr.com> 3.47-1
-	Update version
*	Wed Jan 30 2013 baho-utot <baho-utot@columbus.rr.com> 3.42-1
-	Initial build.	First version


