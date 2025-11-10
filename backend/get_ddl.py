"""
Script to extract DDL (CREATE TABLE) statements from PostgreSQL database
Run this to get the exact table structure for your documentation
"""

import asyncio
from sqlalchemy import text
from app.database import engine

async def get_table_ddl():
    """Get CREATE TABLE statements for all tables."""
    
    tables = ['buildings', 'units', 'tenants', 'staff', 'requests']
    
    print("=" * 80)
    print("DATABASE DDL STATEMENTS - For Documentation")
    print("=" * 80)
    print()
    
    async with engine.connect() as conn:
        for table in tables:
            print(f"\n--- {table.upper()} TABLE ---\n")
            
            # Get table definition
            query = text(f"""
                SELECT 
                    'CREATE TABLE ' || table_name || ' (' || 
                    string_agg(
                        column_name || ' ' || 
                        CASE 
                            WHEN data_type = 'USER-DEFINED' THEN udt_name
                            WHEN character_maximum_length IS NOT NULL 
                                THEN data_type || '(' || character_maximum_length || ')'
                            WHEN numeric_precision IS NOT NULL 
                                THEN data_type || '(' || numeric_precision || ',' || numeric_scale || ')'
                            ELSE data_type
                        END ||
                        CASE WHEN is_nullable = 'NO' THEN ' NOT NULL' ELSE '' END ||
                        CASE WHEN column_default IS NOT NULL THEN ' DEFAULT ' || column_default ELSE '' END,
                        ', '
                    ) || ');' as ddl
                FROM information_schema.columns
                WHERE table_name = '{table}'
                GROUP BY table_name;
            """)
            
            result = await conn.execute(query)
            row = result.fetchone()
            if row:
                print(row[0])
            
            # Get primary key
            pk_query = text(f"""
                SELECT 'PRIMARY KEY (' || string_agg(kcu.column_name, ', ') || ');'
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu 
                    ON tc.constraint_name = kcu.constraint_name
                WHERE tc.table_name = '{table}' AND tc.constraint_type = 'PRIMARY KEY';
            """)
            
            result = await conn.execute(pk_query)
            row = result.fetchone()
            if row:
                print(row[0])
            
            # Get foreign keys
            fk_query = text(f"""
                SELECT 
                    'FOREIGN KEY (' || kcu.column_name || ') REFERENCES ' || 
                    ccu.table_name || '(' || ccu.column_name || ')' ||
                    CASE 
                        WHEN rc.delete_rule IS NOT NULL 
                        THEN ' ON DELETE ' || rc.delete_rule 
                        ELSE '' 
                    END || ';'
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu 
                    ON tc.constraint_name = kcu.constraint_name
                JOIN information_schema.constraint_column_usage ccu 
                    ON ccu.constraint_name = tc.constraint_name
                JOIN information_schema.referential_constraints rc
                    ON rc.constraint_name = tc.constraint_name
                WHERE tc.table_name = '{table}' AND tc.constraint_type = 'FOREIGN KEY';
            """)
            
            result = await conn.execute(fk_query)
            rows = result.fetchall()
            for row in rows:
                print(row[0])
            
            # Get unique constraints
            uq_query = text(f"""
                SELECT 'UNIQUE (' || string_agg(kcu.column_name, ', ') || ');'
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu 
                    ON tc.constraint_name = kcu.constraint_name
                WHERE tc.table_name = '{table}' AND tc.constraint_type = 'UNIQUE'
                GROUP BY tc.constraint_name;
            """)
            
            result = await conn.execute(uq_query)
            rows = result.fetchall()
            for row in rows:
                print(row[0])
            
            print()
    
    print("\n" + "=" * 80)
    print("ENUM TYPES")
    print("=" * 80)
    
    async with engine.connect() as conn:
        enum_query = text("""
            SELECT 
                t.typname as enum_name,
                string_agg(e.enumlabel, ', ' ORDER BY e.enumsortorder) as enum_values
            FROM pg_type t 
            JOIN pg_enum e ON t.oid = e.enumtypid  
            JOIN pg_catalog.pg_namespace n ON n.oid = t.typnamespace
            WHERE n.nspname = 'public'
            GROUP BY t.typname;
        """)
        
        result = await conn.execute(enum_query)
        rows = result.fetchall()
        
        for row in rows:
            enum_values = "', '".join(row[1].split(', '))
            print(f"\nCREATE TYPE {row[0]} AS ENUM ('{enum_values}');")
    
    print("\n" + "=" * 80)
    print("TABLE STATISTICS")
    print("=" * 80)
    
    async with engine.connect() as conn:
        for table in tables:
            count_query = text(f"SELECT COUNT(*) FROM {table};")
            result = await conn.execute(count_query)
            count = result.scalar()
            print(f"{table.ljust(20)}: {count} records")

if __name__ == "__main__":
    asyncio.run(get_table_ddl())
