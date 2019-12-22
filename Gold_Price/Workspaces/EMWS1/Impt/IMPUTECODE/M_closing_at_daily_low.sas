label M_closing_at_daily_low = "Imputation Indicator for closing_at_daily_low";
if missing(closing_at_daily_low) then M_closing_at_daily_low = 1;
else M_closing_at_daily_low= 0;
