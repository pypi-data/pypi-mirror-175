from nanoydb import Ydb

query="SELECT 30.0 as query_result"

ydb=Ydb(
    ydb_endpoint='...',
    ydb_database='...'
)

result=ydb.doquery(query)
val=result.get_single_value('query_result')

print(val)
#>30.0
