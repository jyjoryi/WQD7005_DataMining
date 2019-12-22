*------------------------------------------------------------*;
* Clus: Training;
*------------------------------------------------------------*;
*------------------------------------------------------------* ;
* Clus: DMDBClass Macro ;
*------------------------------------------------------------* ;
%macro DMDBClass;
    all_day_maintain(ASC) closing_at_daily_high(ASC) closing_at_daily_low(ASC)
   day(ASC) month(ASC) open_equals_closing(ASC)
%mend DMDBClass;
*------------------------------------------------------------* ;
* Clus: DMDBVar Macro ;
*------------------------------------------------------------* ;
%macro DMDBVar;

%mend DMDBVar;
*------------------------------------------------------------*;
* Clus: Create DMDB;
*------------------------------------------------------------*;
proc dmdb batch data=EMWS1.FIMPORT3_train
dmdbcat=WORK.Clus_DMDB
maxlevel = 513
out=WORK.Clus_DMDB
;
class %DMDBClass;
run;
quit;
*------------------------------------------------------------* ;
* Clus: Nominal Inputs Macro ;
*------------------------------------------------------------* ;
%macro DMVQNOMINAL;
    all_day_maintain closing_at_daily_high closing_at_daily_low day month
   open_equals_closing
%mend DMVQNOMINAL;
*------------------------------------------------------------*;
* Clus: Run DMVQ procedure;
*------------------------------------------------------------*;
title;
options nodate;
proc dmvq data=WORK.Clus_DMDB dmdbcat=WORK.Clus_DMDB std=STD nominal=GLM ordinal=RANK
;
input %DMVQNOMINAL / level=nominal;
VQ maxc = 4 clusname=_SEGMENT_ CLUSLABEL="Segment Id" DISTLABEL="Distance";
MAKE outvar=EMWS1.Clus_OUTVAR;
INITIAL radius=0
;
TRAIN tech=FORGY
;
SAVE outstat=EMWS1.Clus_OUTSTAT outmean=EMWS1.Clus_OUTMEAN;
code file="C:\Users\tan.joryi\Desktop\p\data_mining\03_explore_data\Gold_Price\Workspaces\EMWS1\Clus\DMVQSCORECODE.sas"
group=Clus
;
run;
quit;
*------------------------------------------------------------* ;
* Clus: DMVQ Variables;
*------------------------------------------------------------* ;
%macro dmvqvars;
    all_day_maintain0 all_day_maintain1 closing_at_daily_high0
   closing_at_daily_high1 closing_at_daily_low0 closing_at_daily_low1 dayFriday
   dayMonday daySaturday daySunday dayThursday dayTuesday dayWednesday monthApril
   monthAugust monthDecember monthFebruary monthJanuary monthJuly monthJune
   monthMarch monthMay monthNovember monthOctober monthSeptember
   open_equals_closing0 open_equals_closing1
%mend ;
