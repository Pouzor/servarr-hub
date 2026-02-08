-- Migration: Ajouter colonne torrent_info à library_items
-- Date: 2026-02-08

-- Étape 1 : Ajouter la colonne torrent_info
ALTER TABLE library_items 
ADD COLUMN torrent_info JSON DEFAULT NULL;

-- Étape 2 : Vérifier que la colonne a été ajoutée
SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME = 'library_items' 
AND COLUMN_NAME = 'torrent_info';

-- Étape 3 : Mettre à jour l'enum service_type (si nécessaire)
-- Vérifier si qbittorrent existe déjà
SELECT DISTINCT service_name 
FROM service_configurations;

-- Si besoin de recréer l'enum (MariaDB/MySQL ne supporte pas ALTER TYPE directement)
-- Cette commande sera à adapter selon ta version de MySQL/MariaDB
