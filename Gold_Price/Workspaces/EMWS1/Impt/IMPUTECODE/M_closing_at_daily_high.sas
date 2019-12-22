label M_closing_at_daily_high = "Imputation Indicator for closing_at_daily_high";
if missing(closing_at_daily_high) then M_closing_at_daily_high = 1;
else M_closing_at_daily_high= 0;
