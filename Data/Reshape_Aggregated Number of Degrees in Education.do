* Gerhard O
*2/2/2018
*1. Add national data by year, award and degree type
*2. Reshape data long and then long again

********************************************************************************
********************************************************************************

global excel "H:\CALDER\CALDER Data Visualizations\Data\Teacher Labor Shortage"
global national "H:\Teacher Labor MRKT Shortage\IPEDS\Completions_CIP codes\New CIP data\Data files used for graphs"

import excel "$excel\Aggregated Number of Degrees in Education.xlsx", sheet("Sheet1") firstrow clear

//1: Create a national data set (Will not match national data in plotly data viz
//	since this will not include Puerto Rico or other territories.

preserve
	
	*A. Collapse data by year
		collapse (rawsum) statetotal ba_total ma_total phd_total sped_total ///
			stem_total elem_total other_total, by(year)
			
	*B. Create variable to indicate that this is the national data
		gen state = "NAT"
		gen statename = "National"
		
	*C. Create Temp file
		tempfile national
		save "`national'"
		
restore

	*D. Append to current data set
		append using "`national'"

//2: Reshape long. Will need to reshape again. 

	*A. Prepare for reshape
		drop A
		ren statetotal state_total
		ren aggtotal agg_total
		ren state shortname
		ren statename longname
	
	*B. Reshape
		reshape long stem sped elem other agg ba ma phd state, ///
			i(year shortname longname) j(x) string
			
//2.2: Reshape long again. 

	*A. Prepare for second reshape
		replace x = subinstr(x, "_" , "", .)
		foreach var of varlist stem state sped phd other ma  elem ba agg {
			ren `var' y_`var'
			}
			
	*B. Reshape
		reshape long y_, i(year shortname longname x) j(z) string
		
	*C. Clean for export
		gen indicator = z + " " + x
		ren y_ value
		drop x z 
		drop if value==. 
		ren shortname state_short
		ren longname state_long
		order year state_short state_long indicator value
		
		

export delimited using "$excel\Aggregated Number of Degrees in Education (Reshaped long long) (Add National).csv", replace
