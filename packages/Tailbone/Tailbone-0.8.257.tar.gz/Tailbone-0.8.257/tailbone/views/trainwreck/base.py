# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2022 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Trainwreck views
"""

from __future__ import unicode_literals, absolute_import

import six

from rattail.time import localtime

from webhelpers2.html import HTML, tags

from tailbone.db import Session, TrainwreckSession, ExtraTrainwreckSessions
from tailbone.views import MasterView


class TransactionView(MasterView):
    """
    Master view for Trainwreck transactions
    """
    # model_class = trainwreck.Transaction
    model_title = "Trainwreck Transaction"
    model_title_plural = "Trainwreck Transactions"
    route_prefix = 'trainwreck.transactions'
    url_prefix = '/trainwreck/transactions'
    creatable = False
    editable = False
    deletable = False

    supports_multiple_engines = True
    engine_type_key = 'trainwreck'
    SessionDefault = TrainwreckSession
    SessionExtras = ExtraTrainwreckSessions

    configurable = True

    labels = {
        'store_id': "Store",
        'cashback': "Cash Back",
    }

    grid_columns = [
        'start_time',
        'end_time',
        'system',
        'store_id',
        'terminal_id',
        'receipt_number',
        'cashier_name',
        'customer_id',
        'customer_name',
        'total',
    ]

    form_fields = [
        'system',
        'system_id',
        'store_id',
        'terminal_id',
        'receipt_number',
        'effective_date',
        'start_time',
        'end_time',
        'upload_time',
        'cashier_id',
        'cashier_name',
        'customer_id',
        'customer_name',
        'shopper_id',
        'shopper_name',
        'shopper_level_number',
        'custorder_xref_markers',
        'subtotal',
        'discounted_subtotal',
        'tax',
        'cashback',
        'total',
        'patronage',
        'equity_current',
        'self_updated',
        'void',
    ]

    has_rows = True
    # model_row_class = trainwreck.TransactionItem
    rows_default_pagesize = 100

    row_labels = {
        'item_id': "Item ID",
        'department_number': "Dept. No.",
        'subdepartment_number': "Subdept. No.",
    }

    row_grid_columns = [
        'sequence',
        'item_type',
        'item_scancode',
        'department_number',
        'subdepartment_number',
        'description',
        'unit_quantity',
        'subtotal',
        'tax',
        'total',
        'void',
    ]

    row_form_fields = [
        'transaction',
        'sequence',
        'item_type',
        'item_scancode',
        'item_id',
        'department_number',
        'department_name',
        'subdepartment_number',
        'subdepartment_name',
        'description',
        'custorder_item_xref',
        'unit_quantity',
        'subtotal',
        'discounts',
        'discounted_subtotal',
        'tax',
        'total',
        'exempt_from_gross_sales',
        'net_sales',
        'gross_sales',
        'void',
    ]

    def get_db_engines(self):
        app = self.get_rattail_app()
        trainwreck_handler = app.get_trainwreck_handler()
        return trainwreck_handler.get_trainwreck_engines(include_hidden=False)

    def configure_grid(self, g):
        super(TransactionView, self).configure_grid(g)
        g.filters['receipt_number'].default_active = True
        g.filters['receipt_number'].default_verb = 'equal'

        g.filters['end_time'].default_active = True
        g.filters['end_time'].default_verb = 'equal'
        g.filters['end_time'].default_value = six.text_type(localtime(self.rattail_config).date())
        g.set_sort_defaults('end_time', 'desc')

        g.set_enum('system', self.enum.TRAINWRECK_SYSTEM)
        g.set_type('total', 'currency')
        g.set_type('patronage', 'currency')
        g.set_label('terminal_id', "Terminal")
        g.set_label('receipt_number', "Receipt No.")
        g.set_label('customer_id', "Customer ID")

        g.set_link('start_time')
        g.set_link('end_time')
        g.set_link('upload_time')
        g.set_link('receipt_number')
        g.set_link('customer_id')
        g.set_link('customer_name')
        g.set_link('total')

    def grid_extra_class(self, transaction, i):
        if transaction.void:
            return 'warning'

    def configure_form(self, f):
        super(TransactionView, self).configure_form(f)

        # system
        f.set_enum('system', self.enum.TRAINWRECK_SYSTEM)

        # currency fields
        f.set_type('subtotal', 'currency')
        f.set_type('discounted_subtotal', 'currency')
        f.set_type('tax', 'currency')
        f.set_type('cashback', 'currency')
        f.set_type('total', 'currency')
        f.set_type('patronage', 'currency')

        # custorder_xref_markers
        f.set_renderer('custorder_xref_markers', self.render_custorder_xref_markers)

        # label overrides
        f.set_label('system_id', "System ID")
        f.set_label('terminal_id', "Terminal")
        f.set_label('cashier_id', "Cashier ID")
        f.set_label('customer_id', "Customer ID")
        f.set_label('shopper_id', "Shopper ID")

    def render_custorder_xref_markers(self, txn, field):
        markers = getattr(txn, field)
        if not markers:
            return

        route_prefix = self.get_route_prefix()
        factory = self.get_grid_factory()
        use_buefy = self.get_use_buefy()

        g = factory(
            key='{}.custorder_xref_markers'.format(route_prefix),
            data=[] if use_buefy else txn.custorder_xref_markers,
            columns=['custorder_xref', 'custorder_item_xref'],
            request=self.request)

        if use_buefy:
            return HTML.literal(
                g.render_buefy_table_element(data_prop='custorderXrefMarkersData'))
        else:
            return HTML.literal(g.render_grid())

    def template_kwargs_view(self, **kwargs):
        kwargs = super(TransactionView, self).template_kwargs_view(**kwargs)

        use_buefy = self.get_use_buefy()
        if use_buefy:
            form = kwargs['form']
            if 'custorder_xref_markers' in form:
                txn = kwargs['instance']
                markers = []
                for marker in txn.custorder_xref_markers:
                    markers.append({
                        'custorder_xref': marker.custorder_xref,
                        'custorder_item_xref': marker.custorder_item_xref,
                    })
                kwargs['custorder_xref_markers_data'] = markers

        return kwargs

    def get_row_data(self, transaction):
        return self.Session.query(self.model_row_class)\
                           .filter(self.model_row_class.transaction == transaction)

    def get_parent(self, item):
        return item.transaction

    def configure_row_grid(self, g):
        super(TransactionView, self).configure_row_grid(g)
        g.set_sort_defaults('sequence')

        g.set_type('unit_quantity', 'quantity')
        g.set_type('subtotal', 'currency')
        g.set_type('discounted_subtotal', 'currency')
        g.set_type('tax', 'currency')
        g.set_type('total', 'currency')

        g.set_link('item_scancode')
        g.set_link('description')

    def row_grid_extra_class(self, row, i):
        if row.void:
            return 'warning'

    def get_row_instance_title(self, instance):
        return "Trainwreck Line Item"

    def configure_row_form(self, f):
        super(TransactionView, self).configure_row_form(f)

        # transaction
        f.set_renderer('transaction', self.render_transaction)

        # quantity fields
        f.set_type('unit_quantity', 'quantity')

        # currency fields
        f.set_type('unit_price', 'currency')
        f.set_type('subtotal', 'currency')
        f.set_type('discounted_subtotal', 'currency')
        f.set_type('tax', 'currency')
        f.set_type('total', 'currency')

        # discounts
        f.set_renderer('discounts', self.render_discounts)

    def render_transaction(self, item, field):
        txn = getattr(item, field)
        text = six.text_type(txn)
        url = self.get_action_url('view', txn)
        return tags.link_to(text, url)

    def render_discounts(self, item, field):
        if not item.discounts:
            return

        route_prefix = self.get_route_prefix()
        factory = self.get_grid_factory()
        use_buefy = self.get_use_buefy()

        g = factory(
            key='{}.discounts'.format(route_prefix),
            data=[] if use_buefy else item.discounts,
            columns=['discount_type', 'description', 'amount'],
            labels={'discount_type': "Type"},
            request=self.request)

        if use_buefy:
            return HTML.literal(
                g.render_buefy_table_element(data_prop='discountsData'))
        else:
            g.set_type('amount', 'currency')
            return HTML.literal(g.render_grid())

    def template_kwargs_view_row(self, **kwargs):
        use_buefy = self.get_use_buefy()
        if use_buefy:
            form = kwargs['form']
            if 'discounts' in form:

                app = self.get_rattail_app()
                item = kwargs['instance']
                discounts_data = []
                for discount in item.discounts:
                    discounts_data.append({
                        'discount_type': discount.discount_type,
                        'description': discount.description,
                        'amount': app.render_currency(discount.amount),
                    })
                kwargs['discounts_data'] = discounts_data

        return kwargs

    def rollover(self):
        """
        View for performing yearly rollover functions.
        """
        app = self.get_rattail_app()
        trainwreck_handler = app.get_trainwreck_handler()
        trainwreck_engines = trainwreck_handler.get_trainwreck_engines()
        current_year = app.localtime().year

        # find oldest and newest dates for each database
        engines_data = []
        for key, engine in six.iteritems(trainwreck_engines):

            if key == 'default':
                session = self.Session()
            else:
                session = ExtraTrainwreckSessions[key]()

            error = False
            oldest = None
            newest = None
            try:
                oldest = trainwreck_handler.get_oldest_transaction_date(session)
                newest = trainwreck_handler.get_newest_transaction_date(session)
            except:
                error = True

            engines_data.append({
                'key': key,
                'oldest_date': app.render_date(oldest) if oldest else None,
                'newest_date': app.render_date(newest) if newest else None,
                'error': error,
            })

        return self.render_to_response('rollover', {
            'instance_title': "Yearly Rollover",
            'trainwreck_handler': trainwreck_handler,
            'current_year': current_year,
            'next_year': current_year + 1,
            'trainwreck_engines': trainwreck_engines,
            'engines_data': engines_data,
        })

    def configure_get_context(self):
        context = super(TransactionView, self).configure_get_context()

        app = self.get_rattail_app()
        trainwreck_handler = app.get_trainwreck_handler()
        trainwreck_engines = trainwreck_handler.get_trainwreck_engines()

        context['trainwreck_engines'] = trainwreck_engines
        context['hidden_databases'] = dict([
            (key, trainwreck_handler.engine_is_hidden(key))
            for key in trainwreck_engines])

        return context

    def configure_gather_settings(self, data):
        settings = super(TransactionView, self).configure_gather_settings(data)

        app = self.get_rattail_app()
        trainwreck_handler = app.get_trainwreck_handler()
        trainwreck_engines = trainwreck_handler.get_trainwreck_engines()

        hidden = []
        for key in trainwreck_engines:
            name = 'hidedb_{}'.format(key)
            if data.get(name) == 'true':
                hidden.append(key)
        settings.append({'name': 'trainwreck.db.hide',
                         'value': ', '.join(hidden)})

        return settings

    def configure_remove_settings(self):
        super(TransactionView, self).configure_remove_settings()
        app = self.get_rattail_app()

        names = [
            'trainwreck.db.hide',
            'tailbone.engines.trainwreck.hidden', # deprecated
        ]

        # nb. using thread-local session here; we do not use
        # self.Session b/c it may not point to Rattail
        session = Session()
        for name in names:
            app.delete_setting(session, name)

    @classmethod
    def defaults(cls, config):
        cls._trainwreck_defaults(config)
        cls._defaults(config)

    @classmethod
    def _trainwreck_defaults(cls, config):
        route_prefix = cls.get_route_prefix()
        url_prefix = cls.get_url_prefix()
        permission_prefix = cls.get_permission_prefix()
        model_title_plural = cls.get_model_title_plural()

        # fix perm group title
        config.add_tailbone_permission_group(permission_prefix,
                                             model_title_plural)

        # rollover
        config.add_tailbone_permission(permission_prefix,
                                       '{}.rollover'.format(permission_prefix),
                                       label="Perform yearly rollover for Trainwreck")
        config.add_route('{}.rollover'.format(route_prefix),
                         '{}/rollover'.format(url_prefix))
        config.add_view(cls, attr='rollover',
                        route_name='{}.rollover'.format(route_prefix),
                        permission='{}.rollover'.format(permission_prefix))
