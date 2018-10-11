# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AccountBankStatementLineReconciliationWizard(models.TransientModel):
    _name = "account.bank.statement.line.reconciliation.wizard"

    def _account_move_ids_and_journal_id(self):
        ids = self._context.get('active_ids')
        account_move_ids = self.env['account.move']
        account_move_line_ids = self.env['account.move.line']
        journal_id = self.env['account.journal']
        if ids:
            account_move_ids = account_move_ids.browse(ids)

            journal_ids = account_move_ids.mapped('journal_id')

            if len(account_move_ids) > 1 and len(journal_ids) > 1:
                msg = _("Please only select Journal entries "
                        "that belongs to the same bank journal")
                raise ValidationError(msg)
            account_move_line_ids = account_move_ids.mapped('line_ids')
            journal_id = journal_ids[0]

        return account_move_ids, journal_id, account_move_line_ids

    def _default_statement_line_ids(self):
        account_move_ids, __, __ = self._account_move_ids_and_journal_id()
        return account_move_ids.mapped('statement_line_id')

    def _domain_new_statement_line_id(self):
        __, journal_id, __ = self._account_move_ids_and_journal_id()

        if journal_id:
            self.env.cr.execute("""
            SELECT absl.id from account_bank_statement_line as absl
            JOIN account_bank_statement as acbs on acbs.id = absl.statement_id
            WHERE acbs.journal_id = %s;""", [journal_id.id])
            statement_line_ids = [r[0] for r in self.env.cr.fetchall()]

            return "[('id','in',{ids})]".format(ids=statement_line_ids)
        return "[]"

    statement_line_ids = fields.One2many(
        'account.bank.statement.line',
        string=_('Current values'),
        default=_default_statement_line_ids,
        compute='_default_statement_line_ids'
    )

    new_statement_line_id = fields.Many2one(
        'account.bank.statement.line',
        string=_('New value'),
        domain=_domain_new_statement_line_id
    )

    @api.multi
    def set_new_statement_line_value(self):
        account_move_ids, __, account_move_line_ids = \
            self._account_move_ids_and_journal_id()
        account_move_ids.write({
            'statement_line_id': self.new_statement_line_id.id,
        })
        account_move_line_ids.write({
            'statement_id': self.new_statement_line_id.statement_id.id,
        })
        return {}
