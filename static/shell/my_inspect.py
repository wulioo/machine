import keyword
import re
from collections import defaultdict

from django.core.management.commands import inspectdb
from django.db import connections
from django.db.models.constants import LOOKUP_SEP


class Assets:
    future = 'future'
    option = 'option'
    equity = 'equity'
    others = 'others'


class DataType:
    c = 'c'
    v = 'v'
    others = 'others'


class Command(inspectdb.Command):
    '''
    在官方库inspectdb.Command的基础上，对视图View的字段名进行去敏处理，视图的字段是累计增加的，要确保所有的视图都在要dump的数据库中，
    表名排序了，字段是按description来的，即结构没改的话，是可以保证生成的因子序号不会因增加字段而改变

    此类提供给model_compare脚本使用
    '''

    _assets2type2fields = defaultdict(dict)

    def _get_assets(self, view_name: str):
        if view_name.startswith('v_future'):
            return Assets.future
        if view_name.startswith('v_equity'):
            return Assets.equity
        if view_name.startswith('v_option'):
            return Assets.option
        return Assets.others

    def _get_type(self, view_name: str):
        types = view_name.split('_')[-1]
        if types.startswith('wc'):  # v_future_wc
            return DataType.c
        if types.startswith('type'):  # v_future_type1
            return DataType.v
        return DataType.others

    def is_pks_columns(self, col: str):
        cols = [
            'trading_date',
            'trading_datetime',
            'wind_code',
            'type_name',
            'type_name_ab',
        ]
        return col in cols

    def normalize_col_name(self, col_name, used_column_names, is_relation, table_name, is_view):
        """
        Modify the column name to make it Python-compatible as a field name
        """
        field_params = {}
        field_notes = []

        new_name = col_name.lower()
        if new_name != col_name:
            field_notes.append('Field name made lowercase.')

        if is_view and (not self.is_pks_columns(new_name)):
            new_name = self.get_field_number(table_name, new_name)
            field_notes.append(f"{table_name}.{col_name}")

        if is_relation:
            if new_name.endswith('_id'):
                new_name = new_name[:-3]
            else:
                field_params['db_column'] = col_name

        new_name, num_repl = re.subn(r'\W', '_', new_name)
        if num_repl > 0:
            field_notes.append('Field renamed to remove unsuitable characters.')

        if new_name.find(LOOKUP_SEP) >= 0:
            while new_name.find(LOOKUP_SEP) >= 0:
                new_name = new_name.replace(LOOKUP_SEP, '_')
            if col_name.lower().find(LOOKUP_SEP) >= 0:
                # Only add the comment if the double underscore was in the original name
                field_notes.append("Field renamed because it contained more than one '_' in a row.")

        if new_name.startswith('_'):
            new_name = 'field%s' % new_name
            field_notes.append("Field renamed because it started with '_'.")

        if new_name.endswith('_'):
            new_name = '%sfield' % new_name
            field_notes.append("Field renamed because it ended with '_'.")

        if keyword.iskeyword(new_name):
            new_name += '_field'
            field_notes.append('Field renamed because it was a Python reserved word.')

        if new_name[0].isdigit():
            new_name = 'number_%s' % new_name
            field_notes.append("Field renamed because it wasn't a valid Python identifier.")

        if new_name in used_column_names:
            num = 0
            while '%s_%d' % (new_name, num) in used_column_names:
                num += 1
            new_name = '%s_%d' % (new_name, num)
            field_notes.append('Field renamed because of name conflict.')

        if col_name != new_name and field_notes:
            field_params['db_column'] = col_name

        return new_name, field_params, field_notes

    def get_field_number(self, table_name: str, field: str) -> str:
        k = f"{table_name}.{field}"

        assets = self._get_assets(table_name)
        data_type = self._get_type(table_name)
        if data_type not in self._assets2type2fields[assets]:
            self._assets2type2fields[assets][data_type] = []
            v = 1
        else:
            v = len(self._assets2type2fields[assets][data_type]) + 1

        self._assets2type2fields[assets][data_type].append(k)

        new_col = f"f{v}"
        return new_col

    def handle_inspection(self, options):
        connection = connections[options['database']]
        # 'table_name_filter' is a stealth option
        table_name_filter = options.get('table_name_filter')

        def table2model(table_name):
            return re.sub(r'[^a-zA-Z0-9]', '', table_name.title())

        with connection.cursor() as cursor:
            yield "# This is an auto-generated Django model module."
            yield "# You'll have to do the following manually to clean this up:"
            yield "#   * Rearrange models' order"
            yield "#   * Make sure each model has one field with primary_key=True"
            yield "#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior"
            yield (
                "#   * Remove `managed = False` lines if you wish to allow "
                "Django to create, modify, and delete the table"
            )
            yield "# Feel free to rename the models, but don't rename db_table values or field names."
            yield 'from %s import models' % self.db_module
            known_models = []
            table_info = connection.introspection.get_table_list(cursor)

            # Determine types of tables and/or views to be introspected.
            types = {'t'}
            if options['include_partitions']:
                types.add('p')
            if options['include_views']:
                types.add('v')

            for table_name in (options['table'] or sorted(info.name for info in table_info if info.type in types)):
                is_view = any(info.name == table_name and info.type == 'v' for info in table_info)

                if table_name_filter is not None and callable(table_name_filter):
                    if not table_name_filter(table_name):
                        continue
                try:
                    try:
                        relations = connection.introspection.get_relations(cursor, table_name)
                    except NotImplementedError:
                        relations = {}
                    try:
                        constraints = connection.introspection.get_constraints(cursor, table_name)
                    except NotImplementedError:
                        constraints = {}
                    primary_key_column = connection.introspection.get_primary_key_column(cursor, table_name)
                    unique_columns = [
                        c['columns'][0] for c in constraints.values()
                        if c['unique'] and len(c['columns']) == 1
                    ]
                    table_description = connection.introspection.get_table_description(cursor, table_name)
                except Exception as e:
                    yield "# Unable to inspect table '%s'" % table_name
                    yield "# The error was: %s" % e
                    continue

                yield ''
                yield ''
                yield 'class %s(models.Model):' % table2model(table_name)
                known_models.append(table2model(table_name))
                used_column_names = []  # Holds column names used in the table so far
                column_to_field_name = {}  # Maps column names to names of model fields
                for row in table_description:
                    comment_notes = []  # Holds Field notes, to be displayed in a Python comment.
                    extra_params = {}  # Holds Field parameters such as 'db_column'.
                    column_name = row.name
                    is_relation = column_name in relations

                    att_name, params, notes = self.normalize_col_name(
                        column_name, used_column_names, is_relation, table_name, is_view)
                    extra_params.update(params)
                    comment_notes.extend(notes)

                    used_column_names.append(att_name)
                    column_to_field_name[column_name] = att_name

                    # Add primary_key and unique, if necessary.
                    if column_name == primary_key_column:
                        extra_params['primary_key'] = True
                    elif column_name in unique_columns:
                        extra_params['unique'] = True

                    if is_relation:
                        if extra_params.pop('unique', False) or extra_params.get('primary_key'):
                            rel_type = 'OneToOneField'
                        else:
                            rel_type = 'ForeignKey'
                        rel_to = (
                            "self" if relations[column_name][1] == table_name
                            else table2model(relations[column_name][1])
                        )
                        if rel_to in known_models:
                            field_type = '%s(%s' % (rel_type, rel_to)
                        else:
                            field_type = "%s('%s'" % (rel_type, rel_to)
                    else:
                        # Calling `get_field_type` to get the field type string and any
                        # additional parameters and notes.
                        field_type, field_params, field_notes = self.get_field_type(connection, table_name, row)
                        extra_params.update(field_params)
                        comment_notes.extend(field_notes)

                        field_type += '('

                    # Don't output 'id = meta.AutoField(primary_key=True)', because
                    # that's assumed if it doesn't exist.
                    if att_name == 'id' and extra_params == {'primary_key': True}:
                        if field_type == 'AutoField(':
                            continue
                        elif field_type == 'IntegerField(' and not connection.features.can_introspect_autofield:
                            comment_notes.append('AutoField?')

                    # Add 'null' and 'blank', if the 'null_ok' flag was present in the
                    # table description.
                    if row.null_ok:  # If it's NULL...
                        extra_params['blank'] = True
                        extra_params['null'] = True

                    field_desc = '%s = %s%s' % (
                        att_name,
                        # Custom fields will have a dotted path
                        '' if '.' in field_type else 'models.',
                        field_type,
                    )
                    if field_type.startswith(('ForeignKey(', 'OneToOneField(')):
                        field_desc += ', models.DO_NOTHING'

                    if extra_params:
                        if not field_desc.endswith('('):
                            field_desc += ', '
                        field_desc += ', '.join('%s=%r' % (k, v) for k, v in extra_params.items())
                    field_desc += ')'
                    if comment_notes:
                        field_desc += '  # ' + ' '.join(comment_notes)
                    yield '    %s' % field_desc

                is_partition = any(info.name == table_name and info.type == 'p' for info in table_info)
                yield from self.get_meta(table_name, constraints, column_to_field_name, is_view, is_partition)


if __name__ == '__main__':
    res = Command.get_field_number('amount')
    print(res)
