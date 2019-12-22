****************************************************************;
******             DECISION TREE SCORING CODE             ******;
****************************************************************;
 
******         LENGTHS OF NEW CHARACTER VARIABLES         ******;
LENGTH F_trend  $    8;
LENGTH I_trend  $    8;
LENGTH U_trend  $    8;
LENGTH _WARN_  $    4;
 
******              LABELS FOR NEW VARIABLES              ******;
label _NODE_ = 'Node' ;
label _LEAF_ = 'Leaf' ;
label P_trendupward = 'Predicted: trend=upward' ;
label P_trenddownward = 'Predicted: trend=downward' ;
label P_trendmaintain = 'Predicted: trend=maintain' ;
label Q_trendupward = 'Unadjusted P: trend=upward' ;
label Q_trenddownward = 'Unadjusted P: trend=downward' ;
label Q_trendmaintain = 'Unadjusted P: trend=maintain' ;
label V_trendupward = 'Validated: trend=upward' ;
label V_trenddownward = 'Validated: trend=downward' ;
label V_trendmaintain = 'Validated: trend=maintain' ;
label R_trendupward = 'Residual: trend=upward' ;
label R_trenddownward = 'Residual: trend=downward' ;
label R_trendmaintain = 'Residual: trend=maintain' ;
label F_trend = 'From: trend' ;
label I_trend = 'Into: trend' ;
label U_trend = 'Unnormalized Into: trend' ;
label _WARN_ = 'Warnings' ;
 
 
******      TEMPORARY VARIABLES FOR FORMATTED VALUES      ******;
LENGTH _ARBFMT_8 $      8; DROP _ARBFMT_8;
_ARBFMT_8 = ' '; /* Initialize to avoid warning. */
LENGTH _ARBFMT_12 $     12; DROP _ARBFMT_12;
_ARBFMT_12 = ' '; /* Initialize to avoid warning. */
 
 
_ARBFMT_8 = PUT( trend , $8.);
 %DMNORMCP( _ARBFMT_8, F_trend );
 
******             ASSIGN OBSERVATION TO NODE             ******;
_ARBFMT_12 = PUT( open_equals_closing , BEST12.);
 %DMNORMIP( _ARBFMT_12);
IF _ARBFMT_12 IN ('1' ) THEN DO;
  _NODE_  =                    2;
  _LEAF_  =                    1;
  P_trendupward  =     0.13618677042801;
  P_trenddownward  =     0.11284046692607;
  P_trendmaintain  =     0.75097276264591;
  Q_trendupward  =     0.13618677042801;
  Q_trenddownward  =     0.11284046692607;
  Q_trendmaintain  =     0.75097276264591;
  V_trendupward  =     0.15969581749049;
  V_trenddownward  =     0.10646387832699;
  V_trendmaintain  =      0.7338403041825;
  I_trend  = 'MAINTAIN' ;
  U_trend  = 'maintain' ;
  END;
ELSE DO;
  _ARBFMT_12 = PUT( closing_at_daily_high , BEST12.);
   %DMNORMIP( _ARBFMT_12);
  IF _ARBFMT_12 IN ('1' ) THEN DO;
    _NODE_  =                    6;
    _LEAF_  =                    2;
    P_trendupward  =     0.86206896551724;
    P_trenddownward  =     0.06896551724137;
    P_trendmaintain  =     0.06896551724137;
    Q_trendupward  =     0.86206896551724;
    Q_trenddownward  =     0.06896551724137;
    Q_trendmaintain  =     0.06896551724137;
    V_trendupward  =      0.9078947368421;
    V_trenddownward  =     0.07894736842105;
    V_trendmaintain  =     0.01315789473684;
    I_trend  = 'UPWARD' ;
    U_trend  = 'upward' ;
    END;
  ELSE DO;
    _NODE_  =                    7;
    _LEAF_  =                    3;
    P_trendupward  =     0.45791245791245;
    P_trenddownward  =     0.54208754208754;
    P_trendmaintain  =                    0;
    Q_trendupward  =     0.45791245791245;
    Q_trenddownward  =     0.54208754208754;
    Q_trendmaintain  =                    0;
    V_trendupward  =      0.4295652173913;
    V_trenddownward  =     0.56173913043478;
    V_trendmaintain  =     0.00869565217391;
    I_trend  = 'DOWNWARD' ;
    U_trend  = 'downward' ;
    END;
  END;
 
*****  RESIDUALS R_ *************;
IF  F_trend  NE 'UPWARD'
AND F_trend  NE 'DOWNWARD'
AND F_trend  NE 'MAINTAIN'  THEN DO;
        R_trendupward  = .;
        R_trenddownward  = .;
        R_trendmaintain  = .;
 END;
 ELSE DO;
       R_trendupward  =  -P_trendupward ;
       R_trenddownward  =  -P_trenddownward ;
       R_trendmaintain  =  -P_trendmaintain ;
       SELECT( F_trend  );
          WHEN( 'UPWARD'  ) R_trendupward  = R_trendupward  +1;
          WHEN( 'DOWNWARD'  ) R_trenddownward  = R_trenddownward  +1;
          WHEN( 'MAINTAIN'  ) R_trendmaintain  = R_trendmaintain  +1;
       END;
 END;
 
****************************************************************;
******          END OF DECISION TREE SCORING CODE         ******;
****************************************************************;
 
drop _LEAF_;
