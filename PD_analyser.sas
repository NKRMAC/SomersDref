/* Parallelle analyser i.f.t. Python */

%let current_path=%substr(&_SASPROGRAMFILE, 1, %length(&_SASPROGRAMFILE) - %length(%scan(&_SASPROGRAMFILE, -1, /)));

/* Ja, man skal lige hive csv-filen ned */
proc import datafile="&current_path.PD_portefoelje.csv"
    out=pdport
    dbms=csv
    replace;
    getnames=yes;
run;

/* Beregn Somers' D med PROC LOGISTIC.*/

* En resultattabel;
proc sql;
create table somersdtable (somersd num, auc num, auc_lower num, auc_upper num);
;quit;

* Beregn Somers' D;
proc logistic data=pdport;
    model default(Event = '1') = p_def ;
    roc;
    ods output ROCAssociation=ROCassoc;
run;

* Læg det i resultattabellen;
proc sql;
insert into somersdtable
select SomersD, Area, LowerArea, UpperArea from ROCassoc
where ROCModel = 'Model'
;quit;


/* Beregn med PROC FREQ */

/*
Principielt bør det her virke:

proc freq data=pdport;
  tables default*p_def / measures;
run;

Det skalerer imidlertid *meget* dårligt, så man er nødt til at gruppere.
*/

* Format til gruppering;
proc format;
  value proc_bins
    0 - 0.05 = '1'
    0.05 <- 0.1 = '2'
    0.1 <- 0.2 = '3'
    0.2 <- 0.3 = '4'
    0.3 <- 0.4 = '5'
    0.4 <- 0.5 = '6'
    0.5 <- 0.6 = '7'
    0.6 <- 0.7 = '8'
    0.7 <- 0.8 = '9'
    0.8 <- 0.9 = '10'
    0.9 <- 1   = '11'
    1 <- high  = '12';
run;

* Grupperer;
data pdport_binned;
set pdport;
p_def_binned = input(put(p_def,proc_bins.),8.);
keep default p_def_binned;
run;

* Resultattabel;
proc sql;
create table somersdtable2 (somersd num);
;quit;

* Beregner Somers' D (Og en masse andet hejs);
ods output measures=SomersD_Out;
proc freq data=pdport_binned;
  tables default*p_def_binned / measures;
run;

* Skriver til resultattabellen;
proc sql;
insert into somersdtable2
select value from SomersD_Out where statistic = "Somers' D C|R"
;quit;