/* Parallelle analyser ift Python */

%let current_path=%substr(&_SASPROGRAMFILE, 1, %length(&_SASPROGRAMFILE) - %length(%scan(&_SASPROGRAMFILE, -1, /)));

/* Ja, man skal lige hive csv-filen ned */
proc import datafile="&current_path.PD_portefoelje.csv"
    out=pdport
    dbms=csv
    replace;
    getnames=yes;
run;

/* Rangordning med ROC-kurve */

ods graphics on;
proc logistic data=pdport;
    model default(Event = '1') = p_def ;
    roc;
run;
ods graphics off;

/* Beregn Somers' D. Jeg forstår ikke, hvorfor jeg ikke både kan så en ROC kurve og en assoc tabel, men such is life.  */
proc logistic data=pdport;
    model default(Event = '1') = p_def ;
    ods output Association=assoc;
run;

proc print data=assoc;
run;

/* Så er det PROC FREQ */

/* Det her kører ikke færdigt i endelig tid, så der kal lige arbejdes med noget binning */

proc freq data=pdport;
  tables default*p_def / measures;
run;