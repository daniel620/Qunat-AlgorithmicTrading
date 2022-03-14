// read data file: df_AH.xlsx
import excel "/Users/kuzaowuwei/Documents/GitHub/QunatPlayground/data/df_AH.xlsx", sheet("Sheet1") firstrow

//group by day
by date: gen n = _n
by date: keep if n == 1
drop n

//cal week number 
gen year=int(date/10000)
gen month=int((date-year*10000)/100)
gen day=int((date-year*10000-month*100))
gen t=mdy(month,day,year)
format t %td

gen week_num = week(t)

keep date week_num

//save data
export excel using "/Users/kuzaowuwei/Documents/GitHub/QunatPlayground/data/date2week.xlsx", firstrow(variables) replace
