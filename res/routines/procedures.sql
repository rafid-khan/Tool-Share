-- noinspection SqlWithoutWhereForFile

drop procedure if exists delete_test_data();

-- Deletes all data from tables
create procedure delete_test_data()
    language plpgsql as
$$
begin
    delete from ts_test_catalog.ts_user;
end
$$;
