-- tässä voi olla muutakin tekstiä

--email:matti.virtanen@centria.fi
select * from opiskelijat;
select etunimi, sukunimi, kotikunta from opiskelijat;
select DISTINCT kotikunta from opiskelijat;
select etunimi  ||  sukunimi as nimi from opiskelijat;
select * from opiskelijat order by linja, aloitusvuosi;
select * from opiskelijat where kotikunta = "Pietarsaari";
