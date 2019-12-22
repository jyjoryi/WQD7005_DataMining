label M_open_price = "Imputation Indicator for open_price";
if missing(open_price) then M_open_price = 1;
else M_open_price= 0;
