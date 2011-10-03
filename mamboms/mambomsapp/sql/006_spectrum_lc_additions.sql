BEGIN;

ALTER TABLE "mambomsapp_spectrum"
    ADD COLUMN "precursor_mass" numeric(18, 10) DEFAULT 0.0 NOT NULL;
ALTER TABLE "mambomsapp_spectrum"
    ADD COLUMN "precursor_ion" varchar(20);
ALTER TABLE "mambomsapp_spectrum"
    ADD COLUMN "product_ion" varchar(20);
ALTER TABLE "mambomsapp_spectrum"
    ADD COLUMN "fragment_type" varchar(255);


COMMIT;
