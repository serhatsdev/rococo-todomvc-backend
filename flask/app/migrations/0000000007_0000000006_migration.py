revision = "0000000007"
down_revision = "0000000006"


def upgrade(migration):
    migration.add_column(
        table_name="todo",
        column_name="created_on",
        datatype="timestamp DEFAULT CURRENT_TIMESTAMP",
    )

    # Add column to audit table as well
    migration.add_column(
        table_name="todo_audit",
        column_name="created_on",
        datatype="timestamp DEFAULT CURRENT_TIMESTAMP",
    )

    migration.update_version_table(version=revision)


def downgrade(migration):
    migration.drop_column(table_name="todo", column_name="created_on")
    migration.drop_column(table_name="todo_audit", column_name="created_on")

    migration.update_version_table(version=down_revision)