"""Rename user_name to username

Revision ID: c112b5cb277e
Revises: 
Create Date: 2024-08-20 16:28:09.116107

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c112b5cb277e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('blog_post', schema=None) as batch_op:
        batch_op.alter_column('title',
               existing_type=sa.TEXT(length=250),
               type_=sa.String(length=250),
               existing_nullable=False)
        batch_op.alter_column('subtitle',
               existing_type=sa.TEXT(length=250),
               type_=sa.String(length=250),
               existing_nullable=False)
        batch_op.alter_column('date',
               existing_type=sa.TEXT(length=250),
               type_=sa.String(length=250),
               existing_nullable=False)
        batch_op.alter_column('author',
               existing_type=sa.TEXT(length=250),
               type_=sa.String(length=250),
               existing_nullable=False)
        batch_op.alter_column('img_url',
               existing_type=sa.TEXT(length=250),
               type_=sa.String(length=250),
               existing_nullable=False)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=100), nullable=False))
        batch_op.drop_column('user_name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_name', sa.VARCHAR(length=1000), nullable=False))
        batch_op.drop_column('username')

    with op.batch_alter_table('blog_post', schema=None) as batch_op:
        batch_op.alter_column('img_url',
               existing_type=sa.String(length=250),
               type_=sa.TEXT(length=250),
               existing_nullable=False)
        batch_op.alter_column('author',
               existing_type=sa.String(length=250),
               type_=sa.TEXT(length=250),
               existing_nullable=False)
        batch_op.alter_column('date',
               existing_type=sa.String(length=250),
               type_=sa.TEXT(length=250),
               existing_nullable=False)
        batch_op.alter_column('subtitle',
               existing_type=sa.String(length=250),
               type_=sa.TEXT(length=250),
               existing_nullable=False)
        batch_op.alter_column('title',
               existing_type=sa.String(length=250),
               type_=sa.TEXT(length=250),
               existing_nullable=False)

    # ### end Alembic commands ###
