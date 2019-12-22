if upcase(NAME) = "ALL_DAY_MAINTAIN" then do;
ROLE = "REJECTED";
end;
else 
if upcase(NAME) = "CLOSING_AT_DAILY_LOW" then do;
ROLE = "REJECTED";
end;
else 
if upcase(NAME) = "DAY" then do;
ROLE = "REJECTED";
end;
else 
if upcase(NAME) = "MONTH" then do;
ROLE = "REJECTED";
end;
else 
if upcase(NAME) = "Q_TRENDDOWNWARD" then do;
ROLE = "ASSESS";
end;
else 
if upcase(NAME) = "Q_TRENDMAINTAIN" then do;
ROLE = "ASSESS";
end;
else 
if upcase(NAME) = "Q_TRENDUPWARD" then do;
ROLE = "ASSESS";
end;
else 
if upcase(NAME) = "_NODE_" then do;
ROLE = "SEGMENT";
LEVEL = "NOMINAL";
end;
