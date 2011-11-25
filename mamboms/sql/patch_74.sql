BEGIN;

ALTER TABLE "mambomsuser_mambomsldapprofile"
    ADD COLUMN "password_reset_token" VARCHAR(50);

CREATE INDEX "mambomsuser_mambomsldapprofile_password_reset_token" ON "mambomsuser_mambomsldapprofile" ("password_reset_token");
CREATE INDEX "mambomsuser_mambomsldapprofile_password_reset_token_like" ON "mambomsuser_mambomsldapprofile" ("password_reset_token" varchar_pattern_ops);

COMMIT;
