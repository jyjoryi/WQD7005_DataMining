label M_daily_high = "Imputation Indicator for daily_high";
if missing(daily_high) then M_daily_high = 1;
else M_daily_high= 0;
