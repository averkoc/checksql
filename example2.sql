-- email:kalevi.kallio@centria.fi
select * from opiskelijat;
-- tässä on opiskelijan muuta tekstiä
select etunimi, sukunimi,
       kotikunta from opiskelijat;
-- tässä on kommenttirivi
select DISTINCT kotikuntta
from opiskelijat;
select etunimi  ||  sukunimi as nimi from opiskelijat;

-- tässä on opiskelijan muuta tekstiä

select * from opiskelijat order by linja, aloitusvuosi;
select * from opiskelijat where kotikunta = "Pietarsaari";

select * from opiskelijat where kotikunta = "Pietarsaari";
