format IMP_closing_at_daily_low BEST12.0;
label IMP_closing_at_daily_low = 'Imputed closing_at_daily_low';
IMP_closing_at_daily_low = closing_at_daily_low;
if missing(closing_at_daily_low) then IMP_closing_at_daily_low = 0;
