--As per Mambo-MS Google Code ticket #50
--Script to create a link table between LCModification (refered to as ionized species) and
--Spectrum, so that we can have a many to many relationship between them.
--Then we drop the ionized species column from LCMA record, since it is now a property of the Spectrum.
BEGIN;
CREATE TABLE "mambomsapp_spectrum_ionized_species" (
    "id" serial NOT NULL PRIMARY KEY,
    "spectrum_id" integer NOT NULL REFERENCES "mambomsapp_spectrum" ("id") DEFERRABLE INITIALLY DEFERRED,
    "lcmodification_id" integer NOT NULL REFERENCES "mambomsapp_lcmodification" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("spectrum_id", "lcmodification_id")
)
;
ALTER TABLE mambomsapp_lcmarecord DROP COLUMN ionized_species_id;
END;
