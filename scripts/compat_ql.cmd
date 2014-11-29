#
#       @file       compat_ql.cmd
#       @author     xy
#       @since      2013-09-28
#
#       @brief      Provide backwards-compatibility.
#
#

echo "[compat_ql.cmd] BEGIN"



# (OBJ) Reapply Xform was renamed to Alembic Reapply Xform.
#
opalias Object qLib::alembic_reapply_xform_ql::1 qLib::reapply_xform_ql::1



echo "[compat_ql.cmd] END"

