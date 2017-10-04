"""Introduce package specifict flows

Revision ID: 245b57b274c2
Revises: be06b06767de
Create Date: 2017-06-05 06:54:01.582926

"""

# revision identifiers, used by Alembic.
revision = '245b57b274c2'
down_revision = 'be06b06767de'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('monitored_upstreams',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('package_id', sa.Integer(), nullable=True),
                    sa.Column('url', sa.String(length=255), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.Column('added_at', sa.DateTime(), nullable=False),
                    sa.Column('deactivated_at', sa.DateTime(), nullable=True),
                    sa.Column('active', sa.Boolean(), nullable=False),
                    sa.ForeignKeyConstraint(['package_id'], ['packages.id'], ),
                    sa.PrimaryKeyConstraint('id'))
    op.create_index(op.f('ix_monitored_upstreams_package_id'), 'monitored_upstreams',
                    ['package_id'], unique=False)
    op.create_table('package_analyses',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('package_id', sa.Integer(), nullable=True),
                    sa.Column('started_at', sa.DateTime(), nullable=True),
                    sa.Column('finished_at', sa.DateTime(), nullable=True),
                    sa.ForeignKeyConstraint(['package_id'], ['packages.id'], ),
                    sa.PrimaryKeyConstraint('id'))
    op.create_index(op.f('ix_package_analyses_package_id'), 'package_analyses', ['package_id'],
                    unique=False)
    op.create_table('package_worker_results',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('package_analysis_id', sa.Integer(), nullable=True),
                    sa.Column('worker', sa.String(length=255), nullable=True),
                    sa.Column('worker_id', sa.String(length=64), nullable=True),
                    sa.Column('external_request_id', sa.String(length=64), nullable=True),
                    sa.Column('task_result', postgresql.JSONB(astext_type=sa.Text()),
                              nullable=True),
                    sa.Column('error', sa.Boolean(), nullable=False),
                    sa.ForeignKeyConstraint(['package_analysis_id'], ['package_analyses.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('worker_id'))
    op.create_index(op.f('ix_package_worker_results_package_analysis_id'),
                    'package_worker_results', ['package_analysis_id'], unique=False)
    op.create_index(op.f('ix_package_worker_results_worker'), 'package_worker_results',
                    ['worker'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_package_worker_results_worker'), table_name='package_worker_results')
    op.drop_index(op.f('ix_package_worker_results_package_analysis_id'),
                  table_name='package_worker_results')
    op.drop_table('package_worker_results')
    op.drop_index(op.f('ix_package_analyses_package_id'), table_name='package_analyses')
    op.drop_table('package_analyses')
    op.drop_index(op.f('ix_monitored_upstreams_package_id'), table_name='monitored_upstreams')
    op.drop_table('monitored_upstreams')
    # ### end Alembic commands ###
