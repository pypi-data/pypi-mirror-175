-- Table aggregating all the pages must be dropped in order to replace the pages.
DROP VIEW IF EXISTS dune_user_generated.{{TableName}};
-- This is only temporary because of schema change.
-- DROP VIEW IF EXISTS dune_user_generated.{{TableName}};
CREATE OR REPLACE VIEW dune_user_generated.{{TableName}}_{{Page}} AS (
    {{SelectValuesQuery}}
);