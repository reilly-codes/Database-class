SELECT 
    machine, 
    AVG(spindle_load) AS avg_load
FROM readings
WHERE time(ts) >= '18:00:00'
GROUP BY machine
ORDER BY avg_load DESC;