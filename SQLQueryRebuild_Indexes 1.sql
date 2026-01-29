DECLARE @SchemaName NVARCHAR(128)
DECLARE @TableName NVARCHAR(128)
DECLARE @IndexName NVARCHAR(128)
DECLARE @SQL NVARCHAR(MAX)

DECLARE IndexCursor CURSOR FOR
SELECT 
    OBJECT_SCHEMA_NAME(ix.object_id) AS SchemaName,
    OBJECT_NAME(ix.object_id) AS TableName,
    ix.name AS IndexName
FROM sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, 'LIMITED') ips
JOIN sys.indexes ix ON ips.object_id = ix.object_id AND ips.index_id = ix.index_id
WHERE ips.avg_fragmentation_in_percent > 5
      AND ips.fragment_count > 5000         
      AND ix.name IS NOT NULL       

OPEN IndexCursor
FETCH NEXT FROM IndexCursor INTO @SchemaName, @TableName, @IndexName

WHILE @@FETCH_STATUS = 0
BEGIN
    SET @SQL = 'ALTER INDEX [' + @IndexName + '] ON [' + @SchemaName + '].[' + @TableName + '] REBUILD;'
    PRINT @SQL  -- Optional: Prints the generated SQL command
    EXEC sp_executesql @SQL
    
    FETCH NEXT FROM IndexCursor INTO @SchemaName, @TableName, @IndexName
END

CLOSE IndexCursor
DEALLOCATE IndexCursor
