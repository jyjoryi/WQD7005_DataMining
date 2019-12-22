format IMP_open_equals_closing BEST12.0;
label IMP_open_equals_closing = 'Imputed open_equals_closing';
IMP_open_equals_closing = open_equals_closing;
if missing(open_equals_closing) then IMP_open_equals_closing = 0;
