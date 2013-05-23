#!/bin/bash
set -o errexit	# exit if error
set -o nounset	# exit if variable not initalized
set +h		# disable hashall
shopt -s -o pipefail
export FAILURE="../FAILURE"
#	set correct file ownership
#	Start of build process
build=$(uname -m)

list="filesystem random.number.generator which b43-fwcutter broadcom-wl net-tools-CVS wireless_tools openssl openssh fcron" #perl-module-scandeps"

echo $list

die() {
	local msg=$1
	printf "BLFS build failed: ${msg}\n"
	touch ${FAILURE}
	exit 1
}
findpkg() {
	local pkg=$1
	RPM=$(find ../RPMS -name "${pkg}-[0-9]*.rpm" -print)
}
buildpkg() {
	local pkg=$1
	rm -rf ../BUILD/* ../BUILDROOT/* > /dev/null 2>&1
	rpmbuild -ba --target ${build} --nocheck ${pkg}.spec |& tee LOGS/${pkg} || die "buildpkg: ${pkg}: rpmbuild failure"
	rm -rf ../BUILD/* ../BUILDROOT/* > /dev/null 2>&1
}
installpkg() {
	# --noscripts - add to rpm to disable %post scripts
	local pkg=$1
	findpkg ${pkg}
	printf "installpkg: $RPM\n"
	[ -z $RPM ] && die "installation error: rpm package not found\n"
	rpm -Uvh ${RPM} || die "installation error: ${pkg} rpm barfed\n"
}
for i in ${list}; do
	[ -f ${FAILURE} ] && die "FAILURE: ${i}: detected exiting script\n"
	RPM="";findpkg ${i}
	[ -z $RPM ] && printf "Building --> ${i}\n" || printf "Skipping --> ${i}\n"
	[ -z $RPM ] && buildpkg ${i} || continue
	#installpkg ${i}
	findpkg ${i};rpm -qilp ${RPM} > INFO/${i} 2>&1 || true
	printf "RPM: $RPM\n"
	rpmlint ${RPM} > LINT/${i} 2>&1 || true
	rpm -qp --provides ${RPM} > PROVIDES/${i} 2>&1 || true
	rpm -qp --requires ${RPM} > REQUIRES/${i} 2>&1 || true
done
rm -rf ../BUILD/*
