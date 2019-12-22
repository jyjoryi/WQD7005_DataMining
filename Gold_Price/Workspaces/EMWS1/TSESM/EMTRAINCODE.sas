
%macro EM_TSESM_MAIN;

   filename temp catalog 'sashelp.emtsdm.tsesm_macros.source';
   %include temp;
   filename temp catalog 'sashelp.emtsdm.tsutility_macros.source';
   %include temp;
   filename temp;

   %if %upcase(&EM_ACTION) = CREATE %then %do;
       filename temp catalog 'sashelp.emtsdm.tsesm_create.source';
       %include temp;
       filename temp;
       %EM_TSESM_CREATE;
   %end;
   %else
   %if %upcase(&EM_ACTION) = TRAIN %then %do;
        filename temp catalog 'sashelp.emtsdm.tsesm_train.source';
           %include temp;
           filename temp;
        %EM_TSESM_TRAIN;
   %end;
   %else
   %if %upcase(&EM_ACTION) = SCORE %then %do;
           filename temp catalog 'sashelp.emtsdm.tsesm_score.source';
           %include temp;
           filename temp;
         %EM_TSESM_SCORE;
   %end;
   %else
   %if %upcase(&EM_ACTION) = REPORT %then %do;
           filename temp catalog 'sashelp.emtsdm.tsesm_report.source';
           %include temp;
           filename temp;
          %EM_TSESM_REPORT;
   %end;
%mend EM_TSESM_MAIN;
%EM_TSESM_MAIN;


