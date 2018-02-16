* Gerhard O
*2/2/2018
* Reshape data long

global excel "H:\CALDER\CALDER Data Visualizations\Data\Teacher Labor Shortage"
import excel "$excel\Aggregated Number of Degrees in Education.xlsx", sheet("Sheet1") firstrow clear

//1: Reshape long. Will need to reshape again. 

	*A. Prepare for reshape
		drop A
		ren statetotal state_total
		ren aggtotal agg_total
		ren state shortname
		ren statename longname
	
	*B. Reshape
		reshape long stem sped elem other agg ba ma phd state, ///
			i(year shortname longname) j(x) string
			
//1.2: Reshape long again. 

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
		

export excel using "$excel\Aggregated Number of Degrees in Education (Reshaped long long).xlsx", firstrow(variables) replace	
