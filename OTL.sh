#!/bin/bash
#
#	Quick-and-dirty utility script for extract Houdini .otl files to ascii and vice versa.
#
#


# TODO: check if parameter 1 exists


echo "otl.sh: \"$1\""

pushd .


case "$1" in

	clean_built|cb|clean)
		echo "*** CLEAN: DELETING BUILT OTLS ***"
		find . -name "*.otl" -exec rm -rf {} \;
	;;
	#;& # (fallthru)



	build|b)
		echo "*** BUILDING OTLS ***"
		find . -name "*_OTL" | awk '{ d=$0; sub(/_OTL$/, ".otl", d); print "hotl -C " $0 " " d }' | bash
		find . -name "*.bkp*" -exec rm {} \; # delete backups created by otl building
	;;

	buildmime|bm)
		echo "*** BUILDING OTLS (MIME) ***"
		find . -name "*_OTL" | awk '{ d=$0; sub(/_OTL$/, ".otl", d); print "hotl -l " $0 " " d }' | bash
		find . -name "*.bkp*" -exec rm {} \; # delete backups created by otl building
	;;



	clean_extracted|cx)
		echo "*** DELETING EXTRACTED OTLS ***"
		find . -name "*_OTL" -exec rm -rf {} \;
	;;
	#;& # (fallthru)



	extract|x)
		echo "*** EXTRACTING OTLS ***"
		find . -name "*.otl" | awk '{ d=$0; sub(/\.otl$/, "_OTL", d); print "hotl -X " d " " $0 }' | bash
	;;

	extractmime|xm)
		echo "*** EXTRACTING OTLS (MIME) ***"
		find . -name "*.otl" | awk '{ d=$0; sub(/\.otl$/, "_OTL", d); print "hotl -p -t " d " " $0 }' | bash
	;;


	*)
		echo "unknown command: \"$1\""
	;;

esac

popd

echo "done."

