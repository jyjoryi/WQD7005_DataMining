label M_closing_price = "Imputation Indicator for closing_price";
if missing(closing_price) then M_closing_price = 1;
else M_closing_price= 0;
