-- Patch to upgrade a RELEASE_37 database to the RELEASE_38 schema.

BEGIN;
ALTER TABLE mambomsapp_lcmarecord ADD COLUMN "ionized_species_id" integer NULL REFERENCES "mambomsapp_lcmodification" ("id");
COMMIT;
