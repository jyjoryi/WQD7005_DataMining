label M_daily_low = "Imputation Indicator for daily_low";
if missing(daily_low) then M_daily_low = 1;
else M_daily_low= 0;
