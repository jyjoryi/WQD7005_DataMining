if NAME="all_day_maintain" then do;
ROLE="INPUT";
LEVEL="BINARY";
ORDER="";
end;
if NAME="closing_at_daily_high" then do;
ROLE="INPUT";
LEVEL="BINARY";
ORDER="";
end;
if NAME="closing_at_daily_low" then do;
ROLE="INPUT";
LEVEL="BINARY";
ORDER="";
end;
if NAME="closing_price" then do;
ROLE="REJECTED";
LEVEL="INTERVAL";
ORDER="";
end;
if NAME="daily_high" then do;
ROLE="REJECTED";
LEVEL="INTERVAL";
ORDER="";
end;
if NAME="daily_low" then do;
ROLE="REJECTED";
LEVEL="INTERVAL";
ORDER="";
end;
if NAME="day_no" then do;
ROLE="REJECTED";
LEVEL="ORDINAL";
ORDER="";
end;
if NAME="open_equals_closing" then do;
ROLE="INPUT";
LEVEL="BINARY";
ORDER="";
end;
if NAME="open_price" then do;
ROLE="REJECTED";
LEVEL="INTERVAL";
ORDER="";
end;
if NAME="trend" then do;
ROLE="TARGET";
LEVEL="NOMINAL";
ORDER="";
end;
if NAME="year" then do;
ROLE="REJECTED";
LEVEL="NOMINAL";
ORDER="";
end;
drop DROP;
