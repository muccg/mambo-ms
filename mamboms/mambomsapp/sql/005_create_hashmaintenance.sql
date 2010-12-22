CREATE TABLE "mambomsapp_hashmaintenance" (
    "id" serial NOT NULL PRIMARY KEY,
    "spectrum_id" integer NOT NULL REFERENCES "mambomsapp_spectrum" ("id") DEFERRABLE INITIALLY DEFERRED,
    "last_updated" date NOT NULL
)
;COMMIT;
