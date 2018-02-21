#!/bin/bash
#################################################
#	Title:	10-KDE.sh			#
#        Date:	2018-02-10			#
#     Version:	1.1				#
#      Author:	baho-utot@columbus.rr.com	#
#     Options:					#
#################################################
set -o errexit	# exit if error...insurance ;)
set -o nounset		# exit if variable not initalized
set +h			# disable hashall
PRGNAME=${0##*/}	# script name minus the path
TOPDIR=${PWD}
	#	Build variables
LC_ALL=POSIX
PATH=/bin:/usr/bin:/sbin:/usr/sbin:/tools/bin
export LC_ALL PATH
#
PARENT=/usr/src/Octothorpe
LOGPATH=${TOPDIR}/LOGS/BLFS
INFOPATH=${TOPDIR}/INFO/BLFS
SPECPATH=${TOPDIR}/SPECS/BLFS
PROVIDESPATH=${TOPDIR}/PROVIDES/BLFS
REQUIRESPATH=${TOPDIR}/REQUIRES/BLFS
RPMPATH=${TOPDIR}/RPMS
#
#	Build functions
#
die() {	
	local _red="\\033[1;31m"
	local _normal="\\033[0;39m"
	[ -n "$*" ] && printf "${_red}$*${_normal}\n"
	exit 1
}
msg() {
	printf "%s\n" "${1}"
}
msg_line() {
	printf "%s" "${1}"
}
msg_failure() {
	local _red="\\033[1;31m"
	local _normal="\\033[0;39m"
	printf "${_red}%s${_normal}\n" "FAILURE"
	exit 2
}
msg_success() {
	local _green="\\033[1;32m"
	local _normal="\\033[0;39m"
	printf "${_green}%s${_normal}\n" "SUCCESS"
	return 0
}
end-run() {
	local _green="\\033[1;32m"
	local _normal="\\033[0;39m"
	printf "${_green}%s${_normal}\n" "Run Complete"
	return
}

maker(){	#	$1:	name of package
	local _log="${LOGPATH}/${1}"
	local _pkg=$(find ${RPMPATH} -name "${1}-[0-9]*.rpm" -print 2>/dev/null)
	local _filespec=${SPECPATH}/${1}.spec
	#
	#	Build
	#
	msg_line "	Building: ${1}: "
	if [ -z ${_pkg} ]; then
		rm ${_log}.installed > ${_log} 2>&1	|| true
		rm ${INFOPATH}/${1} > ${_log} 2>&1	|| true
		rpmbuild -ba \
			${_filespec} >> ${_log} 2>&1 && msg_success || msg_failure
		_pkg=$(find ${RPMPATH} -name "${1}-[0-9]*.rpm" -print)
	else
		msg "Skipped"
		#	return
	fi
}
info(){		#	$1:	Name of package
	local _log="${LOGPATH}/${1}"
	local _pkg=$(find ${RPMPATH} -name "${1}-[0-9]*.rpm" -print 2>/dev/null)
	#
	#	Info
	#
	msg_line "	Info: ${1}: "
	[ -z ${_pkg} ] && die "ERROR: rpm package not found"
	if [ ! -e ${INFOPATH}/${1} ]; then
		rpm -qilp \
			${_pkg} > ${INFOPATH}/${1} 2>&1 || true
		rpm -qp --provides \
			${_pkg} > ${PROVIDESPATH}/${1} 2>&1 || true
		rpm -qp --requires \
			${_pkg} > ${REQUIRESPATH}/${1} 2>&1 || true
		msg_success
	else
		 msg "Skipped"
	fi
}
installer(){	#	$1:	name of package
	local _log="${LOGPATH}/${1}"
	local _pkg=$(find ${RPMPATH} -name "${1}-[0-9]*.rpm" -print 2>/dev/null)
	#
	#	Install
	#
	msg_line "	Installing: ${1}: "
	[ -z ${_pkg} ] && die "ERROR: rpm package not found"
	if [ ! -e ${_log}.installed ]; then
		su -c "rpm -Uvh --nodeps ${_pkg}" >> "${_log}" 2>&1  && msg_success || msg_failure
		mv ${_log} ${_log}.installed
	else
		msg "Skipped"
	fi
}
_prepare() {
	local _log="${LOGPATH}/${1}"
	_wget_list	#	Create wget list
	_md5sum_list	#	Create md5sum list
	#	Fetch source packages
	local DESTDIR=""
	local INPUTFILE=""
	msg_line "	Fetching source: "
		[ -d SOURCES ] || install -vdm 755 ${DESTDIR}
		#	LFS sources
		DESTDIR=${TOPDIR}/SOURCES
		INPUTFILE=${TOPDIR}/SOURCES/kde.wget
		wget --no-clobber --no-check-certificate --input-file=${INPUTFILE} --directory-prefix=${DESTDIR} > /dev/null 2>&1
	msg_success
	msg_line "	Checking source: "
		md5sum -c ${TOPDIR}/SOURCES/kde.md5sum >> ${_log}
	msg_success
	return
}
_post() {
	return
	local _log="${LOGPATH}/${1}"
	msg "	Post processing:"
	return
}
_wget_list() {
	msg_line "	Creating wget-list: "
		cat > ${PARENT}/SOURCES/kde.wget <<- EOF
			http://download.kde.org/stable/phonon/4.9.1/phonon-4.9.1.tar.xz
		EOF
		#	dependencies
		cat >> ${PARENT}/SOURCES/kde.wget <<- EOF
			http://download.kde.org/stable/frameworks/5.37/extra-cmake-modules-5.37.0.tar.xz
		EOF
	msg_success
	return
}
_md5sum_list(){
	msg_line "	Creating wget-list: "
		cat > ${PARENT}/SOURCES/kde.md5sum <<- EOF
			7896a560f5da345a626e782610c8e71e	SOURCES/phonon-4.9.1.tar.xz
		EOF
		#	Dependencies
		cat >> ${PARENT}/SOURCES/kde.md5sum <<- EOF
			29883c1580c5b9e4c736a138fc832e1a	SOURCES/extra-cmake-modules-5.37.0.tar.xz
		EOF
	msg_success
	return
}
#
#	Main line
#
[ -z ${PARENT} ]	&& die "${PRGNAME}: Variable: PARENT not set: FAILURE"
#
#	BLFS Desktop system
#
msg "Building KDE"
LIST=""
LIST+="prepare "
#	KDE
LIST+="extra-cmake-modules "
#	depens for QT
#alsa-lib-1.1.4.1
#Cups-2.2.4
#gst-plugins-base-1.12.2
#HarfBuzz-1.4.8
#ICU-59.1
#JasPer-2.0.12
#libjpeg-turbo-1.5.2
#libmng-2.0.3
#libpng-1.6.31
#LibTIFF-4.0.8
#libxkbcommon-0.7.2
#OpenSSL-1.0.2l Libraries
#pcre2-10.30
#SQLite-3.20.0
# qt "
#phonon " - needs QT
LIST+="post"
for i in ${LIST};do
	rm -rf BUILD BUILDROOT
	case ${i} in
		prepare)	_prepare "kde.${i}"	;;
		post)		_post ${i}		;;
		*)		maker ${i}	
				info  ${i}
				installer ${i}		;;
	esac
done
end-run