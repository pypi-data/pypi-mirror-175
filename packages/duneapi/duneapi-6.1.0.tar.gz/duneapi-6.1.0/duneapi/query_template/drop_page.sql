-- In order to drop a page, must drop any view or table which depending on it (i.e. cascade)
DROP VIEW IF EXISTS dune_user_generated.{{TableName}}_page_{{Page}} CASCADE;