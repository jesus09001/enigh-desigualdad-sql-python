USE enigh_db;



-- Agrupamos la población en 10 deciles de ingreso equivalente para observar la brecha de ingresos a nivel nacional:
WITH deciles_hogar AS (
    SELECT
        folioviv,
        foliohog,
        ing_cor,
        gasto_mon,
        factor,
        NTILE(10) OVER(ORDER BY ing_cor ASC) AS decil_ingreso
    FROM concentradohogar
)
SELECT 
	decil_ingreso,
    COUNT(*) AS muestra_hogares,
    SUM(factor) AS hogares_representativos,
    ROUND(MAX(ing_cor),2) AS ingreso_maximo,
    ROUND(MIN(ing_cor),2) AS ingreso_minimo,
    ROUND(SUM(ing_cor * factor) / SUM(factor),2) AS ingreso_promedio_ponderado,
    ROUND(SUM(gasto_mon * factor) / SUM(factor), 2) AS gasto_promedio_ponderado
FROM deciles_hogar
GROUP BY decil_ingresoc
ORDER BY decil_ingreso ASC;


-- Evaluamos qué porcentaje del gasto total destina cada decil a alimentos básicos frente a educación y esparcimiento:
WITH deciles_hogar AS (
    SELECT 
        ing_cor,
        gasto_mon,
        alimentos,
        transporte,
        salud,
        educa_espa,
        factor,
        NTILE(10) OVER (ORDER BY ing_cor ASC) AS decil_ingreso
    FROM concentradohogar
)
SELECT 
    decil_ingreso,
    ROUND(SUM(alimentos * factor) / SUM(gasto_mon * factor) * 100, 2) AS pct_gasto_alimentos,
    ROUND(SUM(transporte * factor) / SUM(gasto_mon * factor) * 100, 2) AS pct_gasto_transporte,
    ROUND(SUM(salud * factor) / SUM(gasto_mon * factor) * 100, 2) AS pct_gasto_salud,
    ROUND(SUM(educa_espa * factor) / SUM(gasto_mon * factor) * 100, 2) AS pct_gasto_educa_esparcimiento
FROM deciles_hogar
GROUP BY decil_ingreso
ORDER BY decil_ingreso ASC;
-- Identificamos la diferencia de ingresos y gasto en alimentos entre Jalisco (`entidad = 14`) y el resto del país:

SELECT 
    CASE 
        WHEN FLOOR(ubica_geo / 1000) = 14 THEN 'Jalisco'
        ELSE 'Resto del País' 
    END AS region,
    COUNT(*) AS muestra_hogares,
    SUM(factor) AS hogares_representados,
    ROUND(SUM(ing_cor * factor) / SUM(factor), 2) AS ingreso_promedio_trimestral,
    ROUND(SUM(gasto_mon * factor) / SUM(factor), 2) AS gasto_promedio_trimestral,
    ROUND(SUM(alimentos * factor) / SUM(gasto_mon * factor) * 100, 2) AS pct_gasto_alimentos
FROM concentradohogar
GROUP BY region;

-- Unimos relacionalmente `concentradohogar` con `poblacion`para analizar el impacto del nivel 
-- educativo del jefe o jefa de familia (`parentesco = 101` / `numren = 1`) en el ingreso del hogar:

SELECT 
    p.nivelaprob AS nivel_educativo_jefe,
    COUNT(DISTINCT c.folioviv) AS muestra_hogares,
    SUM(c.factor) AS hogares_representados,
    ROUND(SUM(c.ing_cor * c.factor) / SUM(c.factor), 2) AS ingreso_promedio_hogar
FROM concentradohogar c
INNER JOIN poblacion p 
    ON c.folioviv = p.folioviv 
   AND c.foliohog = p.foliohog
WHERE p.parentesco = 101 -- Identificador de Jefe(a) de hogar
GROUP BY p.nivelaprob
ORDER BY ingreso_promedio_hogar DESC;
