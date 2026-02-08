-- Migration: Ajouter username/password pour qBittorrent
-- Date: 2026-02-09

-- Étape 1 : Modifier api_key pour qu'elle soit nullable
ALTER TABLE service_configurations 
MODIFY COLUMN api_key TEXT NULL;

-- Étape 2 : Ajouter username
ALTER TABLE service_configurations 
ADD COLUMN IF NOT EXISTS username TEXT NULL;

-- Étape 3 : Ajouter password
ALTER TABLE service_configurations 
ADD COLUMN IF NOT EXISTS password TEXT NULL;

-- Vérification
SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME = 'service_configurations' 
AND COLUMN_NAME IN ('api_key', 'username', 'password');
