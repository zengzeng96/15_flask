"""empty message

Revision ID: f9d2b6671fcb
Revises: 
Create Date: 2020-03-12 18:10:50.362000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f9d2b6671fcb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('email', table_name='tbl_users')
    op.drop_index('name', table_name='tbl_users')
    op.drop_table('tbl_users')
    op.drop_index('name', table_name='tbl_roles')
    op.drop_table('tbl_roles')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tbl_roles',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset=u'utf8',
    mysql_engine=u'InnoDB'
    )
    op.create_index('name', 'tbl_roles', ['name'], unique=True)
    op.create_table('tbl_users',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=64), nullable=True),
    sa.Column('email', mysql.VARCHAR(length=128), nullable=True),
    sa.Column('password', mysql.VARCHAR(length=128), nullable=True),
    sa.Column('role_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['role_id'], [u'tbl_roles.id'], name=u'tbl_users_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset=u'utf8',
    mysql_engine=u'InnoDB'
    )
    op.create_index('name', 'tbl_users', ['name'], unique=True)
    op.create_index('email', 'tbl_users', ['email'], unique=True)
    # ### end Alembic commands ###
