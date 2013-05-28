Summary:	Scans potential modules used by perl programs
Name:		 perl-module-scandeps
Version:	1.10
Release:	1
License:	Artistic
URL:		http://www.cpan.org
Group:		Perl/Module
Vendor:		Bildanet
Distribution:	Octothorpe
BuildArch:	noarch
Source0:	Module-ScanDeps-%{version}.tar.gz
%description
An application of Module::ScanDeps is to generate executables from scripts
that contains necessary modules; this module supports two such projects,
PAR and App::Packer.  Please see their respective documentations on CPAN
for further information.
%prep
%setup -q -n Module-ScanDeps-%{version}
%build
%{__perl} Makefile.PL
# INSTALLDIRS=vendor
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
rm -rf inc
find . -name 'debug*'
#make DESTDIR=%{buildroot} install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;
%{_fixperms} %{buildroot}/*
%check
make -k test |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%clean
rm -rf %{buildroot}
%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_libdir}/perl5/site_perl/*
#%{perl_vendorlib}/*
%changelog
*	Thu May 16 2013 baho-utot <baho-utot@columbus.rr.com> 1.10-1
-	Initial build.	First version
