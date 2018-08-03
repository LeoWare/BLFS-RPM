#	
Summary:	Public Key Infrastructure (PKI) is a method to validate the authenticity of an otherwise unknown entity
Name:		Certificate-Authority-Certificates 
Version:	8.1
Release:	1
License:	Any
URL:		Any
Group:		BLFS/
Vendor:		Octothorpe
Distribution:	BLFS-8.1
ExclusiveArch:	x86_64
Requires:	OpenSSL >= 1.1.0f
Source0:	http://anduin.linuxfromscratch.org/BLFS/other/make-ca.sh-20170514
Source1:	http://anduin.linuxfromscratch.org/BLFS/other/certdata.txt
Source2:	http://www.cacert.org/certs/root.crt
%description
	Public Key Infrastructure (PKI) is a method to validate the authenticity of an 
	otherwise unknown entity across untrusted networks.
	PKI works by establishing a chain of trust, rather than trusting each individual
	host or entity explicitly. In order for a certificate presented by a remote entity
	to be trusted, that certificate must present a complete chain of certificates that
	can be validated using the root certificate of a Certificate Authority (CA) that is
	trusted by the local machine.

	Establishing trust with a CA involves validating things like company address, ownership,
	contact information, etc., and ensuring that the CA has followed best practices, such as
	undergoing periodic security audits by independent investigators and maintaining an always
	available certificate revocation list.
%prep
	install -vdm 755  %{_builddir}/%{name}-%{version}
%build
	#	Create CAcert_Class_1_root.pem file
	install -vdm755 %{buildroot}/etc/ssl/local
	cp %{_sourcedir}/root.crt .
	openssl x509 -in root.crt -text -fingerprint -setalias "CAcert Class 1 root" -addtrust serverAuth -addtrust emailProtection -addtrust codeSigning > %{buildroot}/etc/ssl/local/CAcert_Class_1_root.pem
	#	Install script
	install -vdm 755 %{buildroot}/usr/sbin/
	install -vm755 %{_sourcedir}/make-ca.sh-20170514 %{buildroot}/usr/sbin/make-ca.sh
	#	Make certs
	cp %{_sourcedir}/certdata.txt %{buildroot}/etc/ssl/local
	%{buildroot}/usr/sbin/make-ca.sh --certdata %{buildroot}/etc/ssl/local/certdata.txt --destdir %{buildroot}
%install
	#	Copy license/copying file 
	#	install -D -m644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE
	#	Create file list
	rm -rf %{buildroot}/usr/share/info/dir
	find %{buildroot} -name '*.la' -delete
	find "${RPM_BUILD_ROOT}" -not -type d -print > filelist.rpm
	sed -i "s|^${RPM_BUILD_ROOT}||" filelist.rpm
%files -f filelist.rpm
	%defattr(-,root,root)
%changelog
*	Tue Feb 13 2018 baho-utot <baho-utot@columbus.rr.com> Certificate-Authority-Certificates-8.1-1
-	Initial build.	First version