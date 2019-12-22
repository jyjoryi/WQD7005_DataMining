format IMP_closing_at_daily_high BEST12.0;
label IMP_closing_at_daily_high = 'Imputed closing_at_daily_high';
IMP_closing_at_daily_high = closing_at_daily_high;
if missing(closing_at_daily_high) then IMP_closing_at_daily_high = 0;
