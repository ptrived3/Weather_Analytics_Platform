-- QUERY 1: Highest recorded temperature per city (need to check the historical data)
SELECT city_name as city, MAX(max_temp) as temperature
FROM weather_analytics.weather w
JOIN weather_analytics.cities c ON c.city_id = w.city_id
GROUP BY city_name
ORDER BY temperature DESC;


-- QUERY 2: Hottest month of the year per city
SELECT c.city_name, TO_CHAR(w.weather_date, 'YYYY-MM') as month, ROUND(AVG(w.max_temp), 1) as highest_temp
FROM weather_analytics.weather w
JOIN weather_analytics.cities c ON c.city_id = w.city_id
GROUP BY c.city_name, c.city_id, TO_CHAR(w.weather_date, 'YYYY-MM')
HAVING AVG(w.max_temp) = (
    SELECT MAX(monthly_avg)
    FROM (
        SELECT AVG(w2.max_temp) AS monthly_avg
        FROM weather_analytics.weather w2
        WHERE w2.city_id = c.city_id
        GROUP BY TO_CHAR(w2.weather_date, 'YYYY-MM')
    ) AS city_months
)
ORDER BY highest_temp DESC;


-- QUERY 3: Total monthly precipitation by city
SELECT c.city_name, TO_CHAR(w.weather_date, 'YYYY-MM') as month, SUM(w.precipitation) as total_rainfall
FROM weather_analytics.weather w
JOIN weather_analytics.cities c ON c.city_id = w.city_id
GROUP BY c.city_name, TO_CHAR(w.weather_date, 'YYYY-MM')
ORDER BY TO_CHAR(w.weather_date, 'YYYY-MM'), total_rainfall;


-- QUERY 4: Windiest week of the year
SELECT TO_CHAR(weather_date, 'IYYY-IW') AS week, MIN(weather_date) AS week_start, MAX(weather_date) AS week_end, ROUND(AVG(max_wind_speed), 3) as avg_wind
FROM weather_analytics.weather
GROUP BY TO_CHAR(weather_date, 'IYYY-IW')
ORDER BY avg_wind DESC
LIMIT 1;


-- QUERY 5: Average rainfall by city
SELECT c.city_name, ROUND(AVG(w.precipitation), 3) as rainfall_inches
FROM weather_analytics.weather w
JOIN weather_analytics.cities c ON c.city_id = w.city_id
WHERE w.precipitation > 0
GROUP BY c.city_name
ORDER BY rainfall_inches;


-- QUERY 6: Frequency of extreme temperature days per city (temp > 90)
SELECT c.city_name, COUNT(*) FILTER (WHERE w.max_temp > 90) AS extreme_heat_days, COUNT(*) FILTER (WHERE w.min_temp < 24) AS extreme_freeze_days
FROM weather_analytics.weather w
JOIN weather_analytics.cities c ON c.city_id = w.city_id
GROUP BY c.city_name
ORDER BY extreme_heat_days DESC;


-- QUERY 7: Daylight length per city (using sunrise/sunset)
SELECT c.city_name, TO_CHAR(AVG(w.sunset - w.sunrise), 'HH24:MI') as daylight
FROM weather_analytics.weather w
JOIN weather_analytics.cities c ON c.city_id = w.city_id
GROUP BY c.city_name
ORDER BY daylight DESC;



-- QUERY 8: Get all the forecast for the next 7 days
SELECT c.city_name, f.max_temp, f.min_temp, f.sunrise, f.sunset
FROM weather_analytics.forecast f
JOIN weather_analytics.cities c on c.city_id = f.city_id;
