-- Lists all bands with Glam rock as their main style,
-- ranked by their logevity

SELECT band_name, (IFNULL(split, 2020) - formed) AS life_span
    FROM metal_bands
    WHERE style LIKE '%Glam rock%'
    ORDER BY life_span DESC
