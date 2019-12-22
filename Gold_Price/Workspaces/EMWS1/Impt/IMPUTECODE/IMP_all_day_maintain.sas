format IMP_all_day_maintain BEST12.0;
label IMP_all_day_maintain = 'Imputed all_day_maintain';
IMP_all_day_maintain = all_day_maintain;
if missing(all_day_maintain) then IMP_all_day_maintain = 0;
