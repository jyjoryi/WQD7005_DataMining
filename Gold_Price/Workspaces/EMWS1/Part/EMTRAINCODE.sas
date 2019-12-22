*------------------------------------------------------------*;
* Part: Retrieving stratification variable(s) levels;
*------------------------------------------------------------*;
proc freq data=EMWS1.FIMPORT3_train noprint;
format
trend $8.
;
table
trend
/out=WORK.Part_FREQ(drop=percent);
run;
proc sort data=WORK.Part_FREQ;
by descending count;
run;
* Part: Retrieving levels that meet minimum requirement;
data WORK.Part_FREQ2(keep = count);
set WORK.Part_FREQ;
where (.01 * 50 * count) >= 3;
run;
*------------------------------------------------------------*;
* Part: Create stratified partitioning;
*------------------------------------------------------------*;
data
EMWS1.Part_TRAIN(label="")
EMWS1.Part_VALIDATE(label="")
;
retain _seed_ 12345;
drop _seed_ _genvalue_;
call ranuni(_seed_, _genvalue_);
label _dataobs_ = "%sysfunc(sasmsg(sashelp.dmine, sample_dataobs_vlabel, NOQUOTE))";
_dataobs_ = _N_;
drop _c00:;
set EMWS1.FIMPORT3_train;
length _Pformat1 $58;
drop _Pformat1;
_Pformat1 = strip(put(trend, $8.));
if
_Pformat1 = 'upward'
then do;
if (715+1-_C000003)*_genvalue_ <= (358 - _C000001) then do;
_C000001 + 1;
output EMWS1.Part_TRAIN;
end;
else do;
_C000002 + 1;
output EMWS1.Part_VALIDATE;
end;
_C000003+1;
end;
else if
_Pformat1 = 'downward'
then do;
if (712+1-_C000006)*_genvalue_ <= (356 - _C000004) then do;
_C000004 + 1;
output EMWS1.Part_TRAIN;
end;
else do;
_C000005 + 1;
output EMWS1.Part_VALIDATE;
end;
_C000006+1;
end;
else if
_Pformat1 = 'maintain'
then do;
if (396+1-_C000009)*_genvalue_ <= (198 - _C000007) then do;
_C000007 + 1;
output EMWS1.Part_TRAIN;
end;
else do;
_C000008 + 1;
output EMWS1.Part_VALIDATE;
end;
_C000009+1;
end;
run;
