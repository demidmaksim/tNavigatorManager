inflowzo						
--	well	bore	segment	device_type	fully open size	
	101	1	1	head_valve	1*	        -- 1
	102	1	2	Bore_valve	0.0127	    -- 2
	102	2	3	Bore_valve	0.0127	    -- 3
	103	1	2	Bore_valve	0.0127	    -- 4
	103	2	3	Bore_valve	0.0127	    -- 5
	104	1	2	Bore_valve	0.0127	    -- 6
	104	2	3	Bore_valve	0.0127	    -- 7
	105	1	2	Bore_valve	0.0127	    -- 8
	105	2	3	Bore_valve	0.0127	    -- 9
	106	1	2	Bore_valve	0.0127	    -- 10
	106	2	3	Bore_valve	0.0127	    -- 11
	107	1	2	Bore_valve	0.0127	    -- 12
	107	2	3	Bore_valve	0.0127	    -- 13
	108	1	2	Bore_valve	0.0127	    -- 14
	108	2	3	Bore_valve	0.0127	    -- 15
	109	1	2	Bore_valve	0.0127	    -- 16
	109	2	3	Bore_valve	0.0127	    -- 17
	110	1	2	Bore_valve	0.0127	    -- 18
	110	2	3	Bore_valve	0.0127	    -- 19
	111	1	2	Bore_valve	0.0127	    -- 20
	111	2	3	Bore_valve	0.0127	    -- 21
	112	1	2	Bore_valve	0.0127	    -- 22
	112	2	3	Bore_valve	0.0127	    -- 23
	113	1	2	Bore_valve	0.0127	    -- 24
	113	2	3	Bore_valve	0.0127	    -- 25
end						

MakeGroupList						
---	Name	…	…	…	…	well
	Proba1	102	103	104	105	
	Proba2	110	111			
end						


BOUNDS									
--	Data	Field objects	…	…	…	Fluid	min liquid	max liquid	
									
	01.01.2020	101					Oil	0	10000
	01.01.2020	102					Oil	0	2000
	01.01.2020	103					Oil	0	2000
	01.01.2020	104					Oil	0	2000
	01.01.2020	105					Oil	0	2000
	01.01.2020	106					Oil	0	2000
	01.01.2020	107					Oil	0	2000
	01.01.2020	108					Oil	0	2000
	01.01.2020	109					Oil	0	2000
	01.01.2020	110					Oil	0	2000
	01.01.2020	111					Oil	0	2000
	01.01.2020	PROBA1				Oil	0	2000
	01.01.2020  FIELD               Oil 100   10000
end						
							
