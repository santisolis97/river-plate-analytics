-- Borramos la tabla si existe para empezar de cero (ideal en desarrollo)
DROP TABLE IF EXISTS partidos_river;

CREATE TABLE partidos_river (
    id SERIAL PRIMARY KEY,
    fecha DATE,
    local VARCHAR(100),
    visitante VARCHAR(100),
    goles_river FLOAT, -- Usamos FLOAT por los NaNs que Pandas maneja así
    goles_rival FLOAT,
    resultado_final VARCHAR(20)
);