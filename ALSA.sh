#!/bin/bash
#################################################
#	Title:	ALSA.sh				#
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
TITLE=${PRGNAME::-3}
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
	rsync -va  /home/lfs/BLFS-RPM/${TITLE}.sh .
	rsync -var /home/lfs/BLFS-RPM/SPECS/* SPECS/
	#	Fetch source packages
	local DESTDIR=""
	local INPUTFILE=""
	msg_line "	Fetching source: "
		[ -d SOURCES ] || install -vdm 755 ${DESTDIR}
		#	LFS sources
		DESTDIR=${TOPDIR}/SOURCES
		INPUTFILE=${TOPDIR}/SOURCES/${TITLE}.wget
		wget --no-clobber --no-check-certificate --input-file=${INPUTFILE} --directory-prefix=${DESTDIR} > /dev/null 2>&1
	msg_success
	msg_line "	Checking source: "
		md5sum -c ${TOPDIR}/SOURCES/${TITLE}.md5sum >> ${_log}
	msg_success
	cp config-4.12.7.graphics.patch		SOURCES
	cp config-4.12.7.sound.patch		SOURCES
	cp config-4.12.7.powersave.patch	SOURCES
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
		cat > ${PARENT}/SOURCES/${TITLE}.wget <<- EOF
			ftp://ftp.alsa-project.org/pub/lib/alsa-lib-1.1.4.1.tar.bz2
			ftp://ftp.alsa-project.org/pub/plugins/alsa-plugins-1.1.4.tar.bz2
			http://www.mega-nerd.com/SRC/libsamplerate-0.1.9.tar.gz
		EOF
	msg_success
	return
}
_md5sum_list(){
	msg_line "	Creating wget-list: "
		cat > ${PARENT}/SOURCES/${TITLE}.md5sum <<- EOF
			29fa3e69122d3cf3e8f0e01a0cb1d183	SOURCES/alsa-lib-1.1.4.1.tar.bz2
			de51130a7444b79b2dd3c25e28420754	SOURCES/alsa-plugins-1.1.4.tar.bz2
			2b78ae9fe63b36b9fbb6267fad93f259	SOURCES/libsamplerate-0.1.9.tar.gz
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
LIST+="prepare linux "
LIST+="Python2 "				#
LIST+="alsa-lib "				#	Python2
LIST+="libsamplerate "				#
LIST+=" "					#
LIST+=" "					#
LIST+=" "					#
LIST+=" "					#
LIST+=" "					#
#LIST+="alsa-plugins "				#

LIST+="post "
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