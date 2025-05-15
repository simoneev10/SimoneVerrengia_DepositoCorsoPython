--Primo esercizio
-- Si vogliono recuperare dal database "world" la lingua e la nazione di ogni città
SELECT city.name as Nome_Città, country.name as Nazione, countrylanguage.Language as Lingua
from city
INNER join country on  city.CountryCode = country.Code
INNER JOIN countrylanguage on countrylanguage.CountryCode = country.Code
WHERE countrylanguage.Percentage > 20
GROUP by city.Name

-- Secondo modo
-- Si vogliono recuperare dal database "world" la lingua e la nazione di ogni città
SELECT city.name as Nome_Città, country.name as Nazione, countrylanguage.Language as Lingua
from city
INNER join country on  city.CountryCode = country.Code
INNER JOIN countrylanguage on countrylanguage.CountryCode = country.Code
WHERE countrylanguage.IsOfficial = "T"
GROUP by city.Name


--Secondo esercizio
-- Si vuole recuperare il numero di città per nazione dal database "world "mostrando anche il nome della nazione e ordinarli in base al numero di città
SELECT country.Name as Nazione, COUNT(ID) as Numero_CittàxNazione
from city
RIGHT JOIN country on city.CountryCode = country.Code
GROUP by country.Name;

-- Terzo esercizio
-- la lista di repubbliche con aspettativa di vita maggiore dei 70 anni, inoltre si vuole visualizzare anche la lingua parlata
SELECT country.Name as Nazione, country.GovernmentForm as Forma_di_Governo, cl.Language as Lingua_Parlata
FROM country
INNER JOIN countrylanguage as cl on country.Code = cl.CountryCode
WHERE country.LifeExpectancy > 70 AND cl.IsOfficial = "T"
and country.GovernmentForm like "%Republic%"

-- Quarto Esercizio
-- Si vuole recuperare dal database WORLD le lingue parlate per nazione con la rispettiva percentuale di utilizzo
SELECT country.name as Nazione, countrylanguage.Language as Lingua, countrylanguage.Percentage as Percentuale_Lingua_Parlata
from country
INNER JOIN countrylanguage on countrylanguage.CountryCode = country.Code
ORDER by Nazione, Percentuale_Lingua_Parlata


-- Quinto esercizio
-- Si vuole recuperare dal database WORLD le nazioni e la lingua più parlata con percentuale;
SELECT country.name as Nazione, countrylanguage.Language as Lingua, countrylanguage.Percentage as Percentuale_Lingua_Parlata
from country
INNER JOIN countrylanguage on countrylanguage.CountryCode = country.Code
WHERE (countrylanguage.CountryCode, countrylanguage.Percentage) IN (
SELECT CountryCode, MAX(Percentage)
FROM countrylanguage
GROUP by CountryCode)
ORDER by Nazione, Percentuale_Lingua_Parlata

-- Sesto esercizio
-- Visualizzato il nome del paese, la lingua ufficiale parlata e il nome della capitale, includendo solo i paesi con una popolazione superiore a 50 milioni.
SELECT country.Name as Nazione, city.Name as Nome_Capitale, cl.Language as Lingua_Ufficiale
FROM country
INNER JOIN city on city.CountryCode = country.Code
INNER JOIN countrylanguage as cl on country.Code = cl.CountryCode
WHERE cl.IsOfficial = "T"
and country.Population > 50000000
AND city.ID = country.Capital
ORDER by Nazione

-- Settimo esercizio
-- Create una vista chiamata TopCountries che mostri il nome del paese e la sua popolazione per i paesi con una popolazione superiore a 50 milioni di abitanti;
CREATE VIEW TopCountries AS
SELECT country.Name as Nazione, country.Population as Popolazione
FROM country
WHERE country.Population > 50000000

-- Ottavo esercizio
-- Create una vista chiamata PopulationByContinent che mostri il nome del continente e la popolazione totale per ciascun continente.
CREATE VIEW PopulationByContinent as 
SELECT Continent, SUM(Population) as Popolazione_Continente
FROM country
GROUP BY Continent;
