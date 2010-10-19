-- Patch to upgrade a RELEASE_36 database to the RELEASE_37 schema.

BEGIN;
ALTER TABLE mambomsapp_gcmarecord ADD COLUMN "metabolite_class_id" integer NOT NULL REFERENCES "mambomsapp_metaboliteclass" ("id") DEFERRABLE INITIALLY DEFERRED DEFAULT 1;
COMMIT;
