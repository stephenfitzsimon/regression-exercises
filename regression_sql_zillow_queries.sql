use zillow;

SELECT * FROM propertylandusetype;

DESCRIBE properties_2017;

SELECT parcelid, bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, yearbuilt, fips, taxvaluedollarcnt, taxamount, fireplacecnt, garagecarcnt, garagetotalsqft, latitude, longitude, lotsizesquarefeet, unitcnt, numberofstories, propertylandusetypeid, propertylandusedesc
	FROM properties_2017
		JOIN propertylandusetype USING (propertylandusetypeid)
    WHERE propertylandusedesc = 'Single Family Residential';
    
SELECT properties_2017.*, propertylandusedesc, storydesc, typeconstructiondesc, architecturalstyledesc
	FROM properties_2017
		JOIN propertylandusetype USING (propertylandusetypeid)
        LEFT JOIN storytype USING (storytypeid)
        LEFT JOIN typeconstructiontype USING (typeconstructiontypeid)
        LEFT JOIN architecturalstyletype USING (architecturalstyletypeid)
    WHERE propertylandusedesc = 'Single Family Residential';
    
SELECT * FROM architecturalstyletype;